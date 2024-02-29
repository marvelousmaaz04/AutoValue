$(document).ready(function(){
    $(".filter-item").click(function(){
        const value = $(this).attr("data-filter");
        if(value == "all"){
            $(".post-box").show("1000");

        }else{
            $(".post-box").not("."+value).hide("1000");
            $(".post-box").filter("."+value).show("1000");
        }
    })

    $(".filter-item").click(function(){
        $(this).addClass("active-filter").siblings().removeClass("active-filter")
    })
})

function validateSearchForm() {
    var inputField = document.getElementById('search-input');
    var inputValue = inputField.value.trim();

    if (inputValue === '') {
        // If input is empty, prevent form submission
        // alert('Please enter a value in the search field');
        inputField.placeholder = "Enter your search term!";
        inputField.focus()
        return false;
    } else {
        // Reset the placeholder if the input is not empty
        inputField.placeholder = "Search";
        return true;
    }
}

// Initialize Swiper
var swiper = new Swiper(".banner-slider", {
    slidesPerView: 1,
    spaceBetween: 0,
    loop: true,
    grabCursor: true,
    centeredSlides: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },

    breakpoints: {
        0: {
            slidesPerView: 1,

        },
        768: {
            slidesPerView: 1,

        },
        1024: {
            slidesPerView: 1,

        },
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});


