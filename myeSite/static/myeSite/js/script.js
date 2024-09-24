// const header = document.querySelector("header");

// window.addEventListener("scroll", function(){
//     header.classList.toggle("sticky", this.window.scrollY > 0);
// });


// PASSWORD HIDE SHOW
// function togglePassword() {
//     var passwordField = document.getElementById("password");
//     if (passwordField.type === "password") {
//         passwordField.type = "text";
//     } else {
//         passwordField.type = "password";
//     }
// }

document.addEventListener('DOMContentLoaded', function() {
    var popup = document.getElementById('popupMessage');
    if (popup) {
        popup.style.display = 'block'; // Show the popup
        setTimeout(function() {
            popup.style.display = 'none'; // Hide the popup after 3 seconds
        }, 2000);
    }

    document.querySelectorAll('.addToWishlist').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
});




//show short desc of cart
function showcart() {
    const bagicon = document.getElementById('bagicon');
    const mydropdown = document.getElementById('mydropdown_cart');
    bagicon.addEventListener('click', function() {
        mydropdown.style.display = 'block';
    })
}
const bagicon = document.getElementById('bagicon');
const mydropdown = document.getElementById('mydropdown_cart');
document.addEventListener('click', function (event) {
    if (!mydropdown.contains(event.target) && event.target !== bagicon) {
        mydropdown.style.display = 'none';
    }
});



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


// search bar hide show on toggle
document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('searchIcon');
    const searchBar = document.getElementById('searchBar');

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


function showTshirtPopup(){
    const tshirtEyeIcon = document.getElementById("tshirt-eye");
    const tshirtPopupdiv = document.getElementById("tshirt-popupdiv");

    tshirtEyeIcon.addEventListener("click", function(){
        tshirtPopupdiv.style.display = "block";
    });
}

function closeTshirtPopup() {
    const tshirtPopupdiv = document.getElementById("tshirt-popupdiv");
    tshirtPopupdiv.style.display = "none";
}

//function to select size (tshirt-detail page)
function selectSize(element) {
    const size = element.textContent.trim();
        
     // Update the hidden input field with the selected size
     document.getElementById('size-input').value = size;
     
     // Optional: Update styling to indicate selected size
     document.querySelectorAll('.circle1').forEach(el => el.classList.remove('selected'));
     element.classList.add('selected');
}

function showSection(section) {
    // Hide all content sections
    document.querySelectorAll('.content-section').forEach(function(content) {
        content.style.display = 'none';
    });

    // Show the selected section
    document.getElementById(section).style.display = 'block';
}
    
    
// responsive




