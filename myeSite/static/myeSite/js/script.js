const header = document.querySelector("header");

window.addEventListener("scroll", function(){
    header.classList.toggle("sticky", this.window.scrollY > 0);
});


// PASSWORD HIDE SHOW
function togglePassword() {
    var passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}


const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
const slider = document.querySelector('.slider');

let slideIndex = 0;

prevButton.addEventListener('click', () => {
    slideIndex = Math.max(slideIndex - 1, 0);
    updateSliderPosition();
});

nextButton.addEventListener('click', () => {
    slideIndex = Math.min(slideIndex + 1, slider.children.length - 5);
    updateSliderPosition();
});

function updateSliderPosition() {
    const slideWidth = slider.scrollWidth / slider.children.length;
    const offset = -slideIndex * slideWidth;
    slider.style.transform = `translateX(${offset}px)`;
}




// heart icon
document.getElementById('heart').addEventListener("click", function () {
    this.classList.toggle('red');
});

document.getElementById('heart-icon').addEventListener("click", function () {
    this.classList.toggle('red');
});


// timer 
 // Set the date we're counting down to
 var countDownDate = new Date().getTime() + (12 * 60 * 60 * 1000); // 1 hour from now

 // Update the count down every 1 second
 var countdownFunction = setInterval(function() {

     // Get today's date and time
     var now = new Date().getTime();

     // Find the distance between now and the count down date
     var distance = countDownDate - now;

     // Time calculations for hours, minutes and seconds
     var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
     var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
     var seconds = Math.floor((distance % (1000 * 60)) / 1000);

     // Output the result in an element with id="countdown"
     document.getElementById("countdown").innerHTML = hours + " : " 
     + minutes + " : " + seconds + "s ";

     // If the count down is over, write some text 
     if (distance < 0) {
         clearInterval(countdownFunction);
         document.getElementById("countdown").innerHTML = "EXPIRED";
     }
 }, 1000);



// featuredProducts slider
 const products = document.getElementById('products');
 let scrollAmount = 0;

 function slideLeft() {
    const cardWidth = document.querySelector('.product-card').offsetWidth + 20; // 20 is the margin-right
    scrollAmount += cardWidth * 3; // Adjust this number to control how many cards to slide
    products.style.transform = `translateX(${scrollAmount}px)`;
 }

 function slideRight() {
     const cardWidth = document.querySelector('.product-card').offsetWidth + 20; // 20 is the margin-right
     scrollAmount -= cardWidth * 3; // Adjust this number to control how many cards to slide
     products.style.transform = `translateX(${scrollAmount}px)`;
 }


//  const products = document.getElementById('products');
// const cardWidth = document.querySelector('.product-card').offsetWidth + 20; // 20 is the margin-right
// const visibleCards = 5;
// const totalCards = document.querySelectorAll('.product-card').length;
// const maxScroll = (totalCards - visibleCards) * cardWidth;
// let scrollAmount = 0;

// function slideLeft() {
//     if (scrollAmount > 0) {
//         scrollAmount -= cardWidth * visibleCards;
//         if (scrollAmount < 0) {
//             scrollAmount = 0;
//         }
//         products.style.transform = `translateX(-${scrollAmount}px)`;
//     }
// }

// function slideRight() {
//     if (scrollAmount < maxScroll) {
//         scrollAmount += cardWidth * visibleCards;
//         if (scrollAmount > maxScroll) {
//             scrollAmount = maxScroll;
//         }
//         products.style.transform = `translateX(-${scrollAmount}px)`;
//     }
// }



// search bar hide show on toggle
document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('searchIcon');
    const searchBar = document.getElementById('search');

    searchIcon.addEventListener('click', function() {
        if (searchBar.style.display === 'none' || searchBar.style.display === '') {
            searchBar.style.display = 'block';
        } else {
            searchBar.style.display = 'none';
        }
    });
});



function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.tab-content');
    sections.forEach(section => section.style.display = 'none');

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';

    // Add active class to the clicked button
    event.target.classList.add('active');
}

// Display the default section (Featured)
document.addEventListener('DOMContentLoaded', function() {
    showSection('featured');
});


//product Quantity increase decrease
function increaseQuantity() {
    var quantityInput = document.getElementById('quantity-input');
    var currentValue = parseInt(quantityInput.value) || 0;
    if (currentValue < 10) {
        quantityInput.value = currentValue + 1;
    } else {
        showExceedPopup();
    }
}

function decreaseQuantity() {
    var quantityInput = document.getElementById('quantity-input');
    var currentValue = parseInt(quantityInput.value) || 1;
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}

function showExceedPopup() {
    var popup = document.getElementById('popup-stockExceedMsg');
    popup.classList.add('active');
}

function closeExceedPopup() {
    var popup = document.getElementById('popup-stockExceedMsg');
    popup.classList.remove('active');
}


// updateImage
function updateMainImage(imgElement) {
    const mainImage = document.getElementById('main-image');
    mainImage.src = imgElement.src;
}

// JavaScript code to show a popup when an icon is clicked

// Function to show the popup
function showPopup() {
    // Get the popup element
    const popup = document.getElementById('popup');
    overlayforPopup.style.display = 'block';
    // Display the popup
    popup.style.display = 'block';
}

// Function to hide the popup (optional, if you want to close the popup)
function closePopup() {
    // Get the popup element
    const popup = document.getElementById('popup');
    // Hide the popup
    popup.style.display = 'none';
    overlayforPopup.style.display = "none";
}

//toggle heart fill unfill wishlist
function toggleHeart() {
    // Get the icon element
    const heartIcon = document.getElementById('heart-icon');
    
    // Toggle the class between 'bx-heart' and 'bxs-heart'
    if (heartIcon.classList.contains('bx-heart')) {
        heartIcon.classList.remove('bx-heart');
        heartIcon.classList.add('bxs-heart');
    } else {
        heartIcon.classList.remove('bxs-heart');
        heartIcon.classList.add('bx-heart');
    }
}

function showContactform() {
    const contactImage = document.getElementById("contact-image");
    contactImage.addEventListener("click", function(){
        const mycontactForm = document.getElementById("contactForm");
        mycontactForm.style.display = "block";
    });

}