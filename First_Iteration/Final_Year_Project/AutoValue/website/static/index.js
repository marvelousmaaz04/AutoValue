function loginButton(){
    window.location.href = "/login";
};

function signUpButton(){
    window.location.href = "/sign-up";
};

function closeAlert(obj) {
    const alertContainer = document.getElementById('alert-container');
    alertContainer.style.display = 'none';
}

function closeSuccess(obj) {
    const successContainer = document.getElementById('success-container');
    successContainer.style.display = 'none';
}

function toggleNavbar() {
    var items = document.querySelector(".navbar .items");
    if (items.style.display === "block") {
        items.style.display = "none";
    } else {
        items.style.display = "block";
    }
}


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
    car_model.value = "";
    car_model.innerHTML = "";
    // var defaultOption = document.createElement("option");
    
    // defaultOption.innerHTML = "Select Car Model";
    // car_model.appendChild(defaultOption);
    console.log("function called!");
    fetch("/home/get-car-models-prediction-page", {
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



// function searchBlogs(id) {
//     var keyword = document.getElementById("search-input").value;

//     // Make a POST request to the server
//     fetch('/home/car-blogs/keyword=bmw', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         // body: 'keyword=' + encodeURIComponent(keyword),
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Handle the response data as needed

//         console.log(data);
//         document.open();
//         document.write(response);
//         document.close();
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }

// function searchBlogs(id) {
//     var keyword = document.getElementById("search-input").value;

//     var xhr = new XMLHttpRequest;
//     xhr.open("POST", "/home/car-blogs", true);
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//     xhr.onreadystatechange = function() {
//         // You can handle additional states here if needed
//         if (xhr.readyState == 4 && xhr.status == 200) {
//             handleSearchResponse(xhr.responseText);
//         }
//     };

//     xhr.onload = function() {
//         // handle response
//         handleSearchResponse(xhr.responseText);
//     };

//     xhr.send("keyword=" + encodeURIComponent(keyword));
// }

// function handleSearchResponse(response) {
//     // Assuming you have an element with the id "search-results" where you want to display the results
//     // document.getElementById("search-results").innerHTML = response; // we can either do this or the below one
//     console.log(response)
//     // document.open();
//     // document.write(response);
//     // document.close();
// }

// function searchBlogs(id) {
//     var keyword = document.getElementById("search-input").value;

//     // Redirect the user to the search results page
//     window.location.href = "/home/car-blogs?keyword=" + encodeURIComponent(keyword);
// }
