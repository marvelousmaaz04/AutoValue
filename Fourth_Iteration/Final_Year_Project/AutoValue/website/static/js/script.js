let menu = document.querySelector("#menu-btn")
let navbar = document.querySelector(".navbar")
// let profile = document.querySelector("#profile")
// let logoutBtn = document.querySelector("#logout-btn .btn")



menu.onclick = () => {
    menu.classList.toggle('fa-times')
    navbar.classList.toggle('active')
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
});

var swiper1 = new Swiper(".featured-slider", {
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
        800: {
            slidesPerView: 2,

        },
        810: {
            slidesPerView: 3,

        },
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
});
    
}
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
            
            
            document.getElementById("predicted-price").innerHTML = "Predicted Price: Rs." + xhr.responseText;
    
        }
    }

    xhr.onload = function () { }
    xhr.send(fd);
}