// static/js/save_routine.js

function collectRoutineData() {
    // Initialize data structure
    const routineData = {
        routine_steps: [],
        selected_products: {},
        alternative_products: {},
        special_recommendations: {}
    };

    // Helper function to clean text content
    function cleanText(text) {
        return text ? text.trim().replace(/\s+/g, ' ') : '';
    }

    // Get all routine steps (from the list items in the routine steps card)
    const stepElements = document.querySelectorAll('.category-container, ol li');
    stepElements.forEach((stepElement, index) => {
        // Get step name (try different selectors to handle various HTML structures)
        let stepName = '';
        const stepNameElement = stepElement.querySelector('.category-name') ||
                               stepElement.querySelector('div[style*="font-weight: bold"]') ||
                               stepElement.querySelector('div:first-child');

        if (stepNameElement) {
            stepName = cleanText(stepNameElement.textContent);
        } else if (stepElement.textContent.includes(':')) {
            // Try to get name from text content if it has a colon format
            stepName = cleanText(stepElement.textContent.split(':')[0]);
        } else {
            // Fallback
            stepName = `Step ${index + 1}`;
        }

        // If we got a valid step name, add it to our data
        if (stepName) {
            routineData.routine_steps.push(stepName);

            // Get selected product
            const selectElement = stepElement.querySelector('select');
            if (selectElement && selectElement.options.length > 0) {
                const selectedIndex = selectElement.selectedIndex;
                if (selectedIndex >= 0 && selectedIndex < selectElement.options.length &&
                    !selectElement.options[selectedIndex].text.includes('No products')) {

                    // Parse product info from option text
                    const optionText = cleanText(selectElement.options[selectedIndex].text);
                    let productInfo = {
                        name: optionText
                    };

                    // Try to extract brand if it follows "Brand - Product Name" format
                    if (optionText.includes(' - ')) {
                        const parts = optionText.split(' - ');
                        productInfo.brand = parts[0];
                        productInfo.name = parts.slice(1).join(' - ');
                    }

                    routineData.selected_products[stepName] = productInfo;

                    // Collect all alternative products (all non-selected options)
                    routineData.alternative_products[stepName] = [];
                    for (let i = 0; i < selectElement.options.length; i++) {
                        if (i !== selectedIndex && !selectElement.options[i].text.includes('No products')) {
                            const altText = cleanText(selectElement.options[i].text);
                            let altInfo = {
                                name: altText
                            };

                            // Extract brand if present
                            if (altText.includes(' - ')) {
                                const parts = altText.split(' - ');
                                altInfo.brand = parts[0];
                                altInfo.name = parts.slice(1).join(' - ');
                            }

                            routineData.alternative_products[stepName].push(altInfo);
                        }
                    }
                }
            }
        }
    });

    // Collect special recommendations if present
    const specialRecsSection = document.querySelector('div[style*="background-color: #A35F85"]') ||
                              document.querySelector('.special-recommendations') ||
                              document.querySelector('h3[style*="color: #A35F85"]');

    if (specialRecsSection) {
        const parentSection = specialRecsSection.closest('div[style*="background-color: white"]') ||
                             specialRecsSection.parentElement;

        // Look for category headers
        const categoryHeaders = parentSection.querySelectorAll('h3') ||
                               parentSection.querySelectorAll('[style*="color: #A35F85"]');

        categoryHeaders.forEach(categoryElem => {
            const categoryName = cleanText(categoryElem.textContent);
            if (categoryName) {
                routineData.special_recommendations[categoryName] = [];

                // Get products for this category
                // Try to find the nearest UL or product list
                let productList = categoryElem.nextElementSibling;

                // If we found a list
                if (productList && (productList.tagName === 'UL' || productList.classList.contains('product-list'))) {
                    // Get all list items
                    const items = productList.querySelectorAll('li');
                    items.forEach(item => {
                        const productText = cleanText(item.textContent);
                        let productInfo = {
                            name: productText
                        };

                        // Try to extract brand if it follows "Brand - Product Name" format
                        if (productText.includes(' - ')) {
                            const parts = productText.split(' - ');
                            productInfo.brand = parts[0];
                            productInfo.name = parts.slice(1).join(' - ');
                        }

                        routineData.special_recommendations[categoryName].push(productInfo);
                    });
                }
            }
        });
    }

    console.log("Collected routine data:", routineData);
    return routineData;
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("saveRoutineBtn");

    if (!saveButton) {
        console.error("Save button not found");
        return;
    }

    saveButton.addEventListener("click", function () {
        console.log("Save button clicked");
        
        // Try to get CSRF token from either form field or cookie
        let csrfToken;
        const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
        
        if (csrfElement) {
            csrfToken = csrfElement.value;
        } else {
            csrfToken = getCookie('csrftoken');
            
            if (!csrfToken) {
                console.warn("CSRF token not found. Request may fail.");
            }
        }
        
        // Display loading state
        const originalText = saveButton.textContent;
        saveButton.textContent = "Generating PDF...";
        saveButton.disabled = true;
        
        // Collect data using the collectRoutineData function
        const routineData = collectRoutineData();
        
        // Create form data
        const formData = new FormData();
        formData.append("routine_data", JSON.stringify(routineData));
        
        // Set up headers
        const headers = {
            "X-Requested-With": "XMLHttpRequest"
        };
        
        // Add CSRF token if we found one
        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        }
        
        fetch("/save-routine-pdf/", {
            method: "POST",
            body: formData,
            headers: headers,
            credentials: "same-origin" // Include cookies in the request
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}: ${response.statusText}`);
            }
            return response.blob();
        })
        .then(blob => {
            // Create download
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "curl_routine.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            // Reset button
            saveButton.textContent = originalText;
            saveButton.disabled = false;
        })
        .catch(error => {
            console.error("Error saving PDF:", error);
            alert("Could not save your routine. Please try again.");
            saveButton.textContent = originalText;
            saveButton.disabled = false;
        });
    });
});
