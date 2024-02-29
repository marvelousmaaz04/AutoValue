let menu = document.querySelector("#menu-btn")
let navbar = document.querySelector(".navbar")
// let profile = document.querySelector("#profile")
// let logoutBtn = document.querySelector("#logout-btn .btn")



menu.onclick = () => {
    menu.classList.toggle('fa-times')
    navbar.classList.toggle('active')
}

document.querySelector('#profile-btn').onclick = () => {
    document.querySelector('.profile-form-container').classList.toggle('active')
}
document.querySelector('#close-profile-form').onclick = () => {
    document.querySelector('.profile-form-container').classList.remove('active')
}


window.onscroll = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active')
    } else {
        document.querySelector('.header').classList.remove('active')
    }
    menu.classList.remove('fa-times')
    navbar.classList.remove('active')
}
window.onload = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active')
    } else {
        document.querySelector('.header').classList.remove('active')
    }

}

// profile.addEventListener("click",() =>{
//     logoutBtn.classList.toggle('active')
// })

document.querySelector(".home").onmousemove = (e) => {
    document.querySelectorAll('.home-parallax').forEach(elm => {
        let speed = elm.getAttribute('data-speed');

        let x = (window.innerWidth - e.pageX * speed) / 90;
        let y = (window.innerHeight - e.pageY * speed) / 90;

        elm.style.transform = `translateX(${x}px) translateY(${y}px)`;
    });
};

document.querySelector(".home").onmouseleave = () => {
    document.querySelectorAll('.home-parallax').forEach(elm => {

        elm.style.transform = `translateX(0px) translateY(0px)`;
    });
};





var swiper = new Swiper(".vehicles-slider", {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    grabCursor: true,
    centeredSlides: true,
    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,

        },
        768: {
            slidesPerView: 2,

        },
        1024: {
            slidesPerView: 3,

        },
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

var swiper1 = new Swiper(".featured-slider", {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    grabCursor: true,
    centeredSlides: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,

        },
        800: {
            slidesPerView: 2,

        },
        810: {
            slidesPerView: 3,

        },
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});
var swiper2 = new Swiper(".reviews-slider", {
    slidesPerView: 1,
    spaceBetween: 0,
    loop: true,
    grabCursor: true,
    centeredSlides: true,
    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,

        },
        768: {
            slidesPerView: 1,

        },
        991: {
            slidesPerView: 3,

        },
    },
});


function loadCarModels(id, car_model_id) {

    var company = document.getElementById(id).value;
    var car_model = document.getElementById(car_model_id);
    car_model.value = "";
    car_model.innerHTML = "";
    // var defaultOption = document.createElement("option");
    
    // defaultOption.innerHTML = "Select Car Model";
    // car_model.appendChild(defaultOption);
    console.log("function called!");
    fetch("/home/get-car-models", {
    method: "POST",
    body: JSON.stringify({ "company": company }),
    headers: {
        'Content-Type': 'application/json'
    }
}).then((response) => {
    console.log("response received success");
    return response.json(); // return the promise here
}).then((data) => {
    console.log(data.models); // access the "models" key
    for (var i = 0; i < data.models.length; i++) {
        console.log(data.models[i]);
        var newOption = document.createElement("option");
        newOption.value = data.models[i];
        newOption.innerHTML = data.models[i];
        car_model.options.add(newOption);
    }
});
    
}

function loadCarModelsPredictionPage(id, car_model_id) {

    var company = document.getElementById(id).value;
    var car_model = document.getElementById(car_model_id);
    console.log(company)
    console.log(car_model_id)
    car_model.value = "";
    car_model.innerHTML = "";
    // var defaultOption = document.createElement("option");
    
    // defaultOption.innerHTML = "Select Car Model";
    // car_model.appendChild(defaultOption);
    console.log("function called!");
    fetch("/home/get-car-models-prediction-page", {
    method: "POST",
    body: JSON.stringify({ "select-company": company }),
    headers: {
        'Content-Type': 'application/json'
    }
}).then((response) => {
    console.log("response received success");
    return response.json(); // return the promise here
}).then((data) => {
    console.log(data.models); // access the "models" key
    for (var i = 0; i < data.models.length; i++) {
        console.log(data.models[i]);
        var newOption = document.createElement("option");
        newOption.value = data.models[i];
        newOption.innerHTML = data.models[i];
        car_model.options.add(newOption);
    }
});}

// Function to set the display of error divs to "none" when corresponding form elements are changed
// Function to set the display of error divs to "none" when corresponding form elements are changed
function hideErrorOnInputOrChange(fieldId, errorId) {
    var field = document.getElementById(fieldId);
    var errorDiv = document.getElementById(errorId);

    // Add input or change event listener based on the field type
    if (field.tagName.toLowerCase() === "select") {
        field.addEventListener("change", function() {
            // Hide the error message when the field value changes
            errorDiv.style.display = "none";
        });
    } else if (field.tagName.toLowerCase() === "input") {
        field.addEventListener("input", function() {
            // Hide the error message when the input value changes
            errorDiv.style.display = "none";
        });
    }
}

// Call the function for each form element and corresponding error div
hideErrorOnInputOrChange("select-company", "select-company-error");
hideErrorOnInputOrChange("select-model", "select-model-error");

hideErrorOnInputOrChange("select-location", "select-location-error");

hideErrorOnInputOrChange("select-fuel-type", "select-fuel-type-error");

// Repeat the process for input fields
hideErrorOnInputOrChange("kms-driven", "kms-driven-error");
hideErrorOnInputOrChange("year", "year-error");


function selectCompany(id){
    var selectModelError = document.querySelector(id);
    selectModelError.style.display = "none";
}

function validateCarSearchForm() {
    var isValid = true;

    // Validate select company
    var selectCompany = document.getElementById("select-company");
    var selectCompanyError = document.querySelector("#select-company-error");
    if (selectCompany.value === "Select Car Company") {
        selectCompanyError.textContent = "Please select a car company.";
        selectCompanyError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectCompanyError.textContent = "";
        selectCompanyError.style.display = "none"; // Hide the error message
    }

    // Validate select model
    var selectModel = document.getElementById("select-model");
    var selectModelError = document.querySelector("#select-model-error");
    if (selectModel.value === "Select Car Model") {
        selectModelError.textContent = "Please select a car model.";
        selectModelError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectModelError.textContent = "";
        selectModelError.style.display = "none"; // Hide the error message
    }

    // Validate kilometers driven
    var kmsDriven = document.getElementById("kms-driven");
    var kmsDrivenError = document.querySelector("#kms-driven-error");
    if (kmsDriven.value.trim() === "" || isNaN(kmsDriven.value)) {
        kmsDrivenError.textContent = "Please enter a valid number of kilometers driven.";
        kmsDrivenError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        kmsDrivenError.textContent = "";
        kmsDrivenError.style.display = "none"; // Hide the error message
    }

    // Validate select location
    var selectLocation = document.getElementById("select-location");
    var selectLocationError = document.querySelector("#select-location-error");
    if (selectLocation.value === "Select Car Location") {
        selectLocationError.textContent = "Please select a car location.";
        selectLocationError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectLocationError.textContent = "";
        selectLocationError.style.display = "none"; // Hide the error message
    }

    // Validate year
    var year = document.getElementById("year");
    var yearError = document.querySelector("#year-error");
    if (year.value.trim() === "" || isNaN(year.value)) {
        yearError.textContent = "Please enter a valid year.";
        yearError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        yearError.textContent = "";
        yearError.style.display = "none"; // Hide the error message
    }

    // Validate select fuel type
    var selectFuelType = document.getElementById("select-fuel-type");
    var selectFuelTypeError = document.querySelector("#select-fuel-type-error");
    if (selectFuelType.value === "Select Fuel Type") {
        selectFuelTypeError.textContent = "Please select a fuel type.";
        selectFuelTypeError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectFuelTypeError.textContent = "";
        selectFuelTypeError.style.display = "none"; // Hide the error message
    }

    // If form is valid, submit the form
    return isValid;
}
function submitPriceForm(event) {
    event.preventDefault();
    isValid = validateCarPriceForm()
    if(isValid){
        getCarPrice();
    }
}

function validateCarPriceForm() {
    var isValid = true;

    // Validate select company
    var selectCompany = document.getElementById("select-company-price");
    var selectCompanyError = document.querySelector("#select-company-error-price");
    if (selectCompany.value === "Select Car Company") {
        selectCompanyError.textContent = "Please select a car company.";
        selectCompanyError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectCompanyError.textContent = "";
        selectCompanyError.style.display = "none"; // Hide the error message
    }

    // Validate select model
    var selectModel = document.getElementById("select-model-price");
    var selectModelError = document.querySelector("#select-model-error-price");
    if (selectModel.value === "Select Car Model") {
        selectModelError.textContent = "Please select a car model.";
        selectModelError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectModelError.textContent = "";
        selectModelError.style.display = "none"; // Hide the error message
    }

    // Validate kilometers driven
    var kmsDriven = document.getElementById("kms-driven-price");
    var kmsDrivenError = document.querySelector("#kms-driven-error-price");
    if (kmsDriven.value.trim() === "" || isNaN(kmsDriven.value)) {
        kmsDrivenError.textContent = "Please enter a valid number of kilometers driven.";
        kmsDrivenError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        kmsDrivenError.textContent = "";
        kmsDrivenError.style.display = "none"; // Hide the error message
    }

    // Validate select location
    var selectLocation = document.getElementById("select-location-price");
    var selectLocationError = document.querySelector("#select-location-error-price");
    if (selectLocation.value === "Select Car Location") {
        selectLocationError.textContent = "Please select a car location.";
        selectLocationError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectLocationError.textContent = "";
        selectLocationError.style.display = "none"; // Hide the error message
    }

    // Validate year
    var year = document.getElementById("year-price");
    var yearError = document.querySelector("#year-error-price");
    if (year.value.trim() === "" || isNaN(year.value)) {
        yearError.textContent = "Please enter a valid year.";
        yearError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        yearError.textContent = "";
        yearError.style.display = "none"; // Hide the error message
    }

    // Validate select fuel type
    var selectFuelType = document.getElementById("select-fuel-type-price");
    var selectFuelTypeError = document.querySelector("#select-fuel-type-error-price");
    if (selectFuelType.value === "Select Fuel Type") {
        selectFuelTypeError.textContent = "Please select a fuel type.";
        selectFuelTypeError.style.display = "block"; // Set display to block
        isValid = false;
    } else {
        selectFuelTypeError.textContent = "";
        selectFuelTypeError.style.display = "none"; // Hide the error message
    }

    // If form is valid, submit the form
    // if (isValid){
    //     getCarPrice();
    // }
    return isValid;
}
// Call the function for each form element and corresponding error div
hideErrorOnInputOrChange("select-company-price", "select-company-error-price");
hideErrorOnInputOrChange("select-model-price", "select-model-error-price");

hideErrorOnInputOrChange("select-location-price", "select-location-error-price");

hideErrorOnInputOrChange("select-fuel-type-price", "select-fuel-type-error-price");

// Repeat the process for input fields
hideErrorOnInputOrChange("kms-driven-price", "kms-driven-error-price");
hideErrorOnInputOrChange("year-price", "year-error-price");

function form_handler(event) {
    event.preventDefault();
}
// document.getElementById("price-prediction-form").addEventListener("submit", form_handler)
var predictedPriceSpan = document.getElementById('predicted-price');

    // Add a class to the heading when the text is displayed
    predictedPriceSpan.addEventListener('transitionend', function () {
        document.querySelector('h2.heading').classList.add('show-shape');
        
    });


function getCarPrice() {
    // document.getElementById("prediction-form").addEventListener("submit",form_handler)
   
    document.getElementById("predicted-price").innerHTML = "Wait! Predicting Price...";
    

    var fd = new FormData(document.getElementById("price-prediction-form"))

    var xhr = new XMLHttpRequest;

    xhr.open("POST", "/home/get-price-prediction", true);

    document.getElementById("predicted-price").innerHTML = "Wait! Predicting Price...";

    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            
            
            document.getElementById("predicted-price").innerHTML = "Predicted Price: Rs. " + xhr.responseText;
            setTimeout(() => {
                document.getElementById('similar-car-listings').style.opacity = '1';
            },3000)
    
        }
    }

    xhr.onload = function () { }
    xhr.send(fd);
}
function submitFormAndGetListings() {
    var form = document.getElementById('price-prediction-form');
    form.method = 'POST';
    form.action = '/get-similar-car-listings';
    form.target = '_blank';
    form.submit();
}

function updateFullName() {
    var newName = document.getElementById('new-full-name').value;

    // Check if the length is less than or equal to 6
    if (newName.length <= 6) {
        var inputField = document.getElementById('new-full-name');
        inputField.value = ""
        inputField.style.border = '1px solid red';
        inputField.placeholder = "Cannot be less than 6 characters!";
        inputField.focus();
        return false; // Prevent form submission
    }

    // Check if there is a space in the full name
    if (newName.trim().indexOf(' ') === -1) {
        var inputField = document.getElementById('new-full-name');
        inputField.value = ""
        inputField.style.border = '1px solid red';
        inputField.placeholder = "Must contain a space!";
        inputField.focus();
        return false; // Prevent form submission
    }

    // If validation passes, proceed with the update
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update-profile", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                // Update the button text
                document.getElementById('profile-update-btn').textContent = "Profile Updated!";
                // Optionally, you can reset the input field and hide the edit name div here
                var inputField = document.getElementById('new-full-name');
                setTimeout(() => {
                    var inputField = document.getElementById('new-full-name');
                    inputField.value = "";
                    inputField.style.border = '';
                    inputField.placeholder = "Update Full Name";
                    document.getElementById('profile-update-btn').textContent = "Update Profile"
                },3000)
            } else {
                // Handle error response
                console.error("Failed to update profile");
            }
        }
    };
    var data = JSON.stringify({ full_name: newName });
    xhr.send(data);
}
// Assuming you're using jQuery for AJAX
// $('#subscribe-form').submit(function(event) {
//     event.preventDefault();
//     var formData = $(this).serialize();
//     $.post('/subscribe', formData, function(response) {
//         if (response.message === 'You have already subscribed!') {
//             $('#subscribe-button').text('Already Subscribed');
//         } else {
//             $('#subscribe-button').text('Subscribed Successfully');
//         }
//     });
// });

function subscribeNewsletter(event){
    var formData = new FormData(document.getElementById('subscribe-form'));
    fetch('/subscribe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var subscribeButton = document.getElementById('subscribe-button');
        var emailInput = document.getElementById('email-input');
        if (data.message === 'You have already subscribed!') {
            subscribeButton.value= 'Already Subscribed!';
            subscribeButton.style.fontSize = "1.2rem"
            
        } 
        else if(data.message === "Invalid Email Address!"){
            subscribeButton.value= 'Invalid Email!';
            subscribeButton.style.fontSize = "1.6rem";
            
        }
        else if(data.message === "You have successfully subscribed!"){
            subscribeButton.value= 'Subscribed!';
            
            
        }
        setTimeout(function() {
            subscribeButton.style.fontSize = "1.7rem";
            subscribeButton.value = 'Subscribe';
            emailInput.value = "";
        }, 5000);
    })
    .catch(error => console.error('Error:', error));
}
// document.getElementById("client-number").addEventListener("input", function(event) {
//     var clientNumber = event.target.value;
//     validatePhoneNumber(clientNumber);
// });

// Function to validate the phone number length
// function validatePhoneNumber(clientNumber) {
//     if (isNaN(clientNumber) || clientNumber.length !== 10) {
//         // If the phone number length is not 10, show an error message
//         document.getElementById("client-number").setCustomValidity("Phone number must be 10 digits.");
//     } else {
//         // If the phone number length is 10, clear any existing error message
//         document.getElementById("client-number").setCustomValidity("");
//     }
// }

function sendMessage(event) {
    var formData = new FormData(event.target);
    fetch('/contact', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle response, e.g., show success message to the user
        if(data.message == "Message sent successfully!"){
            contactButton = document.getElementById("contact-button");
            contactButton.value = "Message Sent!";
            setTimeout(() => {
                contactButton.value = "Send Message"
                document.getElementById("client-name").value = "";
                document.getElementById("client-email").value = "";
                
                document.getElementById("client-message").value = "";
            },5000)
        }
        else if(data.message == "Invalid Email Address!"){
            contactButton = document.getElementById("contact-button");
            contactButton.value = "Invalid Email!";
            setTimeout(() => {
                contactButton.value = "Send Message"
                document.getElementById("client-name").value = "";
                document.getElementById("client-email").value = "";
                
                document.getElementById("client-message").value = "";
            },5000)
        }
        else if(data.message == "Error occurred!"){
            contactButton = document.getElementById("contact-button");
            contactButton.value = "Try again";
            setTimeout(() => {
                contactButton.value = "Send Message"
                document.getElementById("client-name").value = "";
                document.getElementById("client-email").value = "";
                
                document.getElementById("client-message").value = "";
            },5000)
        }
        console.log(data.message);
    })
    .catch(error => console.error('Error:', error));
}

