function verifyUserSignup(requestData) {
    $.ajax({
        url: '/user_signup',  
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(requestData),
        beforeSend: function () {
            console.log("Signing up user...");
            $("#signupButton").prop("disabled", true).text("Signing Up...");
        },
        success: function (data) {
            if (data.status === "Signup Successful") {
                console.log("User signed up successfully:", data);
                alert("Signup Successful! Redirecting...");
                window.location.href = '/login'; 
            } else {
                console.error("Signup failed:", data.message);
                alert("Signup Failed: " + data.message);
            }
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.error("Error during signup:", errorMsg);
            alert("An error occurred during signup: " + errorMsg);
        },
        complete: function () {
            $("#signupButton").prop("disabled", false).text("Sign Up");
        }
    });
}

$(document).on("click", "#signupButton", function (e) {
    e.preventDefault(); 

    const fullName = $("#name").val().trim();
    const email = $("#email").val().trim();
    const password = $("#password").val();
    const confirmPassword = $("#confirm-password").val();
    const role = $("#role").val();


    if (!fullName || !email || !password || !confirmPassword || !role) {
        alert("All fields are required!");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    // Prepare request data
    const requestData = {
        full_name: fullName,
        email: email,
        password: password,
        role: role
    };

    console.log("Sending signup request:", requestData);

    // Call signup fun..
    verifyUserSignup(requestData);
});

// Function user login
function verifyUserLogin(requestData) {
    $.ajax({
        url: '/user_login',  
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(requestData),
        beforeSend: function () {
            console.log("Logging in user...");
            $("#loginButton").prop("disabled", true).text("Logging in...");
        },
        success: function (data) {
            if (data.status === "Login Successful") {
                console.log("Login successful:", data);
                localStorage.setItem('email', data.email); // Store email
                alert("Login Successful! Redirecting...");
                window.location.href = '/plants';  
            } else {
                console.error("Login failed:", data.message);
                alert("Invalid credentials. Please try again.");
            }
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.error("Error during login:", errorMsg);
            alert("An error occurred during login. Please try again.");
        },
        complete: function () {
            $("#loginButton").prop("disabled", false).text("Login");
        }
    });
}

$(document).on("click", "#loginButton", function (e) {
    e.preventDefault(); 

    const email = $("#email").val().trim();
    const password = $("#password").val().trim();
    const role = $("#role").val();

    // Basic validation
    if (!email || !password || !role) {
        alert("All fields are required!");
        return;
    }

    // Prepare request data
    const requestData = {
        email: email,
        password: password,
        role: role
    };

    console.log("Sending login request:", requestData);

    // Call login func...
    verifyUserLogin(requestData);
});

function register_login_events(){
    $(document).on("change", "#role", function(e){
        var selectedsingup = $("#role option:selected").val();
    });

$(document).on("click", "#signupButton", function(e){
    var selectedsingup = $("#role option:selected").val();
    var name = $("#name").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var confirmpassword = $("#confirm-password").val();
    verifyUserSignup(selectedsingup,name,email, password,confirmpassword);
});

$(document).on("change", "#role", function(e){
    selectedlogin = $("#role option:selected").val();
if (selectedlogin == "user"){
    $(document).on("click", "#loginButton", function(e){
        var name = $("#name").val();
        var email = $("#email").val();
    
        var request_data = {
            "name" :name,
            "email" : email  
        }
        verifyUserLogin(request_data);
    });
}
else if(selectedlogin == "admin"){
    $(document).on("click", "#loginButton", function(e){
        var name = $("#name").val();
        var email = $("#email").val();

        var request_data = {
            "name" :name,
            "email" : email   
        }
        verifyUserLogin(request_data);
    });
}
});
}

function get_submit_contact_form_data(request_data){
    $.ajax({
        url: '/submit_contact_form',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function () {
            console.log("Submitting contact form...");
        },
        success: function (response) {
            if (response.status === "Success") {
                console.log("Contact form submitted successfully:", response);
                
                $("#response-message").text("Thank you for contacting us! Your message has been received.").show();
        
                // Wait for 5 seconds, then contactpage
                setTimeout(function () {
                    window.location.href = '/contactPage';
                }, 5000);
            } else {
                console.error("Submission failed:", response.message);
                alert("Failed to submit the form: " + response.message);
            }
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.error("Error during form submission:", errorMsg);
            alert("An error occurred during submission: " + errorMsg);
        }
    });
}

$(document).on("submit", "#contactForm", function (e) {
    e.preventDefault(); 

    const full_name = $("#name").val();
    const email = $("#email").val();
    const message = $("#message").val();

    const request_data = {
        full_name: full_name,
        email: email,
        message: message
    };
    get_submit_contact_form_data(request_data);
});

$(document).on("click", "#uploadbutton", function(e){
    event.preventDefault(); 
             
    var plantName = $("#plantName").val();
    var productType = $("#productType").val();
    var plantType = $("#plantType").val();
    var plantDescription = $("#plantDescription").val();
    var plantPrice = $("#plantPrice").val();

            var formData = new FormData();
            var plantImage = $("#plantImage")[0].files[0];
                 
            if(plantImage){
                formData.append("plantImage",plantImage);
                formData.append("plantName", plantName);
                formData.append("productType", productType);
                formData.append("plantType", plantType);
                formData.append("plantDescription", plantDescription);
                formData.append("plantPrice", plantPrice);
            
                console.log("Logging FormData contents:");
                for (let [key, value] of formData.entries()) {
                    console.log(key, value);
                }
               
                $.ajax({
                    url: "/upload_image", 
                    type: "POST",
                    data: formData,
                    processData: false, // Prevent jQuery from processing the data
                    contentType: false, // Prevent jQuery from setting a content-type header
                    success: function (response) {
                        alert("Image uploaded successfully!");
                    },
                    error: function (xhr, status, error) {
                        alert("An error occurred: " + error);
                    }
                });
            }       
});

$(document).ready(function () {
    // When the page loads, fetch all data by default
    get_plant_image_data({ selectPlantType: "", selectFertilizerandSeeds: "" });
    get_cart_details_data();
});
$(document).on("change", "#plant-type, #fertilizer-and-seeds", function () {
    const  selectPlantType = $("#plant-type").val();
    const  selectFertilizerandSeeds = $("#fertilizer-and-seeds").val(); 
    
    const request_data = {
        selectPlantType: selectPlantType,
        selectFertilizerandSeeds: selectFertilizerandSeeds
    };
    console.log(request_data)

    get_plant_image_data(request_data);
    get_cart_details_data();
});

function get_plant_image_data(request_data) {
    $.ajax({
        url: '/get_plant_image',  
        type: "POST",             
        dataType: "json",        
        contentType: "application/json", 
        data : JSON.stringify(request_data),
        beforeSend: function () {
            console.log("Fetching data with filter:");
        },
        success: function (data, status, xhr) {
            console.log("Success response from Flask:", data);
            var raw_plant_image_data = data;
            var plant_image_data = JSON.parse(raw_plant_image_data['data']);

            populate_plant_image_data(plant_image_data); 
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log("Error fetching data:", errorMsg);
        }
    });
}

function populate_plant_image_data(plant_image_data) {
    console.log("Received data to display:", plant_image_data); 
    let imageHtml = `<div class="plant-grid">`;

    // Dynamically create the image cards
    $.each(plant_image_data, function(index, row) {
        imageHtml += `
        <div class="imageSection">
    <img style="height:200px; width:200px;" alt="base64image" src="data:image/png;base64,${row['plant_images']}">
    <div><strong>Rs: </strong> ${row['price']}</div>
    <button class="action-btn add-to-cart-btn" id="ATC_Btn"
            data-name="${row['plant_name']}" 
            data-price="${row['price']}" 
            data-image="data:image/png;base64,${row['plant_images']}">
        Add To Cart
    </button>
    <a href="/buyNowPage">
        <button class="buy-now" id="BuyNow_Btn"
                data-name="${row['plant_name']}" 
                data-price="${row['price']}" 
                data-image="data:image/png;base64,${row['plant_images']}">
            Buy Now
        </button>
    </a>
</div>`;
    });

    imageHtml += `</div>`;
    $("#imageContainer").html(imageHtml);

    // $(document).on('click', '#BuyNow_Btn', function () {
    //     const price = $(this).data('price');
    //     localStorage.setItem('price', price);
    //     console.log('Stored price in localStorage:', price);
    // });

    $(document).on('click', '#ATC_Btn', function() {
        const email_id = localStorage.getItem('email');  
        0
        const plantData = {
            email_id: email_id,
            name: $(this).data('name'),
            price: $(this).data('price'),
            image: $(this).data('image'),
            quantity: 1, 
            total: $(this).data('price') // Total = price * quantity
        };
        console.log(plantData);

        // AJAX request to add the plant to the cart
        $.ajax({
            url: '/add_cart',  
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(plantData),
            success: function(response) {
                alert("Plant added to cart!");
                console.log(response.cart_items);
                updateCartCount(email_id);
            },
            error: function(err) {
                alert("Failed to add plant to cart.");
                console.error(err);
            }
        });
    });
}

$(document).ready(function () {
    get_cart_details_data();
});

function get_cart_details_data() {
    var email_id = localStorage.getItem('email');
    console.log(email_id)
    $.ajax({
        url: '/get_cart_details',  
        type: "POST",             
        dataType: "json",        
        contentType: "application/json", 
        data : JSON.stringify({email_id : email_id}),
        beforeSend: function () {
            console.log("Fetching data with filter:");
        },
        success: function (data, status, xhr) {
            console.log("Success response from Flask:", data);
            var raw_cart_details_data = data;
            var cart_details_data = JSON.parse(raw_cart_details_data['data']);

            populate_cart_details_data(cart_details_data); 
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log("Error fetching data:", errorMsg);
        }
    });
}

// function calculateSubtotal() {
//     let subtotal = 0;

//     $(".item-total").each(function () {
//         subtotal += parseFloat($(this).text().trim());
//     });

//     localStorage.setItem('total',subtotal);
//     $("#cart-subtotal").text(subtotal.toFixed(2)); 
// }

function populate_cart_details_data(cart_details_data) {
    console.log("Received data to display:", cart_details_data); 
    let cartHtml = `<div class="cart-container">`;
    let cartCount = 0; 
    
$.each(cart_details_data, function (index, row) {
    cartHtml += `
        <div class="cart-item" data-id="${row.id}">
            <img src="${row.plant_image}" alt="${row.plant_name}" style="width:100px; height:100px;">
            <div class="item-details">
                <h3>${row.plant_name}</h3>
                <p>Price: ${row.price}</p>
                <div class="quantity">
                    <button class="decrease-qty" data-id="${row.id}"data-price="${row.price}">-</button>
                    <input type="number" class="item-qty" value="${row.quantity}" data-id="${row.id}" readonly>
                    <button class="increase-qty" data-id="${row.id}" data-price="${row.price}">+</button>
                </div>
                <p>Subtotal:<span class="item-total" id = "item--total" data-id="${row.id}">${row.total_price}</span></p>
                <button class="remove-item" data-id="${row.id}">Remove</button>
                
            </div>    
        </div>`;
    cartCount++;
});

cartHtml += `</div>
        <div class="cart-summary">
            <p><span class="currency">Total: </span> <span id="cart-subtotal">0</span></p>
            <a href= "/buyNowPage"><button class="buynow" id="Checkout_Btn">Checkout</button></a>
        </div>`;
$(".cart-container").html(cartHtml);
$(".cart-icon span").text(cartCount); 
   
  calculateSubtotal();
}

// $(document).on("click", "#Checkout_Btn", function () {
//     let totalCartPrice = $("#cart-subtotal").text().trim(); 
//     localStorage.setItem("checkout_total", totalCartPrice); 
// });

// Increase or decrease item quantity
$(document).on('click', '.increase-qty, .decrease-qty', function() {
const isIncrease = $(this).hasClass("increase-qty");
const itemId = $(this).data("id");
console.log(itemId);
const price = $(this).data("price"); // Price per unit
const $quantityInput = $(`.item-qty[data-id="${itemId}"]`);
const $totalPriceElement = $(`.item-total[data-id="${itemId}"]`);
let currentQty = parseInt($quantityInput.val());
const newQty = isIncrease ? currentQty + 1 : Math.max(1, currentQty - 1);

// Update UI
$quantityInput.val(newQty);
const newTotalPrice = price * newQty;
$totalPriceElement.text(` ${newTotalPrice}`);
calculateSubtotal();
});

// Remove item from the cart
$(document).on("click", ".remove-item", function () {
    const itemId = $(this).data("id"); 
    if (itemId) {
        console.log("Clicked item's ID:", itemId); // Log the ID
    } else {
        console.error("ID not found on the clicked button!");
    }
$.ajax({
    url: '/get_remove_cart_item',
    type: 'POST',
    dataType: "json", 
    contentType: 'application/json',
    data: JSON.stringify({ itemId: itemId }),
    success: function() {
        $(`.cart-item[data-id="${itemId}"]`).remove(); // Remove from UI
        updateCartSummary();
        calculateSubtotal(); // Update subtotal after removing item
    },
    error: function(err) {
        console.error("Error removing item:", err);
    }
});
});

function updateCartSummary() {
const cartCount = $(".cart-item").length;
$(".cart-icon span").text(cartCount);
}

function get_submit_order_details_data(request_data){
    $.ajax({
        url: '/submit_order_details',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function () {
            console.log("Submitting order form...");
        },
        success: function (response) {
            if (response.status === "Success") {
                console.log("Order submitted successfully:", response);
                
                $("#response-message").text("Thank you for buy plants! Your order has been received.").show();
        
                setTimeout(function () {
                    window.location.href = '/buyNowPage';
                }, 5000);
            } else {
                console.error("Submission failed:", response.message);
                alert("Failed to submit the orderform: " + response.message);
            }
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.error("Error during form submission:", errorMsg);
            alert("An error occurred during submission: " + errorMsg);
        }
    });
}

$(document).on("submit", "#checkoutForm", function (e) {
    e.preventDefault(); 

    const email_or_phone = $("#email").val();
    const news_offers_subscription =  $("#newsOffers").is(":checked");
    const first_name =  $("#first_name").val();
    const last_name =  $("#last_name").val();
    const address =  $("#address").val();
    const apartment_details =  $("#apartmentDetails").val();
    const city = $("#city").val();
    const state =  $("#state").val();
    const pin_code = $("#pin_code").val();
    const phone_number = $("#phone").val();

    const request_data = {
        email_or_phone: email_or_phone,
        news_offers_subscription: news_offers_subscription,
        first_name: first_name,
        last_name: last_name,
        address: address,
        apartment_details : apartment_details,
        city: city,
        state: state,
        pin_code: pin_code,
        phone_number: phone_number,
    };
    console.log(request_data)
    get_submit_order_details_data(request_data);
});


function calculateSubtotal() {
    let subtotal = 0;

    $(".item-total").each(function () {
        let price = parseFloat($(this).text().trim()) || 0; 
        subtotal += price;
    });

    console.log("Calculated subtotal:", subtotal);

    localStorage.setItem('checkout_total', subtotal.toFixed(2)); 
    $("#cart-subtotal").text(subtotal.toFixed(2));
}


$(document).on('click', '#BuyNow_Btn', function (event) {
    event.preventDefault(); 

    const price = $(this).data('price');
    const plantName = $(this).data('name');
    const plantImage = $(this).data('image');

    localStorage.setItem('buy_now_price', price);
    localStorage.setItem('buy_now_plant_name', plantName);
    localStorage.setItem('buy_now_plant_image', plantImage);

    console.log(`Price for ${plantName}:`, price);

    $(".total").addClass("d-none");  
    $("#checkout-summary-container").empty();  
    
    const finalPriceDiv = `
        <div class="total" id="final-price-div">
            <p><span class="currency">Total for ${plantName}: </span><span class="cart_total" id="final-cart-total">${price}</span></p>
        </div>
    `;
    
    $("#checkout-summary-container").append(finalPriceDiv).removeClass("d-none");

    window.location.href = "/buyNowPage";  
});

$(document).ready(function () {
    const buyNowPrice = localStorage.getItem('buy_now_price') || '0';
    const plantName = localStorage.getItem('buy_now_plant_name') || 'Selected Plant';

    $("#final-price-display").text(`Total for ${plantName}: ${buyNowPrice}`);
});

$(document).on('click', '#Checkout_Btn', function (event) {
    event.preventDefault(); 

    const finalPrice = $("#cart-subtotal").text().trim() || '0';

    localStorage.setItem('final_price', finalPrice);

    console.log("Checkout Total:", finalPrice);

    $(".total").addClass("d-none"); 
    $("#checkout-summary-container").empty(); 

    const finalPriceDiv = `
        <div class="total" id="final-price-div">
            <p><span class="currency">Total: </span><span class="cart_total" id="final-cart-total">${finalPrice}</span></p>
        </div>
    `;

    $("#checkout-summary-container").append(finalPriceDiv).removeClass("d-none");

    window.location.href = "/buyNowPage";  
});

$(document).ready(function () {
    let final_price = localStorage.getItem('final_price') || '0';

    if (final_price !== '0') {
        console.log("Final Price:", final_price);

        $(".total").addClass("d-none");

        if (!$("#final-price-div").length) {
            const finalPriceDiv = `
                <div class="total" id="final-price-div">
                    <p><span class="currency">Total: </span><span class="cart_total" id="final-cart-total">${final_price}</span></p>
                </div>
            `;
        
            $("#checkout-summary-container").append(finalPriceDiv);
        }

        $("#checkout-summary-container").removeClass("d-none");
    }
});





// document.addEventListener('DOMContentLoaded', function() {
//     let total = localStorage.getItem('checkout_total') || '0';
//     let price = localStorage.getItem('price') || '0';

//     console.log('Checkout Total:', total);
//     console.log('Item Price:', price);

//     let cartTotalElement = document.getElementById('cart-total');
//     if (cartTotalElement) {
//         cartTotalElement.textContent = total;
//     }

//     let itemTotalElement = document.getElementById('itemtotal');
//     if (itemTotalElement) {
//         itemTotalElement.textContent = price;
//     }

//     let cartTotalElements = document.getElementsByClassName('cart_total');
//     for (let element of cartTotalElements) {
//         element.textContent = price;
//     }
// });



document.addEventListener("DOMContentLoaded", function () {
    // Array of seasonal tips by month
    const seasonalTips = [
        // January
        "🌱 January: \n- Watering : Reduce watering frequency for most indoor plants. Ensure soil is dry before the next watering. Look for signs of overwatering like yellow leaves.\n- Sunlight : Place plants near south-facing windows to maximize exposure to weak sunlight.\n- Fertilizing : Avoid fertilizing as most plants are dormant in winter.",
      
        // February
        "🌱 February: \n-  Watering : Slightly increase watering as plants start to wake up from dormancy.\n- Sunlight : Continue maximizing natural light exposure, and consider cleaning leaves to improve light absorption.\n- Fertilizing : Prepare for the growing season with a light dose of balanced fertilizer.",
      
        // March
        "🌱 March: \n- Watering : Gradually increase watering as the growing season begins.\n- Sunlight : Move plants to brighter spots. Watch for signs of sunburn as sunlight becomes stronger.\n- Fertilizing : Start fertilizing every 2-4 weeks with a balanced fertilizer for leafy plants.",
      
        // April
        "🌱 April: \n- Watering : Maintain regular watering but avoid overwatering as growth increases.\n- Sunlight : Give outdoor plants time to acclimate to spring sunlight by introducing them gradually.\n- Fertilizing : Apply a nitrogen-rich fertilizer to support foliage development.",
      
        // May
        "🌱 May: \n-  Watering : Increase watering frequency as temperatures rise. Morning watering is recommended.\n- Sunlight : Shield sensitive plants from intense midday sun while maximizing morning and evening light.\n- Fertilizing : Regular fertilization every 2-3 weeks supports active growth. Use phosphorus-rich fertilizer for flowering plants.",
      
        // June
        "🌱 June: \n- Watering : Water deeply but less frequently to promote strong root systems.\n- Sunlight : Provide partial shade for delicate plants during intense summer heat.\n- Fertilizing : Use general-purpose fertilizer but reduce intensity if growth slows due to heat stress.",
      
        // July
        "🌱 July: \n-  Watering : Monitor soil moisture levels and water plants early in the morning or late evening.\n- Sunlight : Protect plants from prolonged direct sunlight using shades or cloth.\n- Fertilizing : Apply a light dose of fertilizer every 4 weeks to sustain growth during summer.",
      
        // August
        "🌱 August: \n-  Watering : Consistently water but avoid waterlogging. Ensure good drainage to prevent root rot.\n-  Sunlight : Gradually reduce intense sunlight exposure as fall nears.\n- Fertilizing : Begin tapering off fertilizers, focusing on maintenance rather than growth stimulation.",
      
        // September
        "🌱 September: \n-  Watering : Slowly reduce watering as temperatures drop.\n-  Sunlight : Make the most of available sunlight by positioning plants near bright, unobstructed windows.\n- Fertilizing : Shift to a low-nitrogen fertilizer to support root strength and winter preparation.",
      
        // October
        "🌱 October: \n-  Watering : Keep soil slightly moist, especially for plants moving indoors for the colder months.\n- Sunlight : Transition plants near brighter windows as outdoor sunlight diminishes.\n- Fertilizing : Pause or reduce fertilizing to avoid stimulating growth during shorter days.",
      
        // November
        "🌱 November: \n-  Watering : Minimize watering and ensure good air circulation to prevent fungal issues.\n- Sunlight : Clean windows to maximize light exposure for indoor plants.\n- Fertilizing : Avoid fertilization as plants enter dormancy.",
      
        // December
        "🌱 December: \n-  Watering : Keep watering minimal but consistent for indoor plants. Use lukewarm water to avoid temperature shock.\n- Sunlight : Move plants closer to windows for the shortest daylight days. Use artificial lights if necessary.\n- Fertilizing : Do not fertilize as most plants are completely dormant."
      ];
      
    // Get current month (0-11, where 0 = January)
    const currentMonth = new Date().getMonth(); // 0 for January, 1 for February, etc.
    const tipContainer = document.getElementById("seasonal-tip");
    
    tipContainer.innerText = seasonalTips[currentMonth];
    
    document.getElementById("current-month").textContent = new Date()
      .toLocaleString("default", { month: "long" });
    document.getElementById("seasonal-tip-text").textContent = seasonalTips[currentMonth];
  });


  document.addEventListener("DOMContentLoaded", function () {
    let dropdownBtn = document.querySelector(".dropdown-btn");
    let dropdownContent = document.querySelector(".dropdown-content");

    if (dropdownBtn) {
        dropdownBtn.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdownContent.classList.toggle("show");
        });

        document.addEventListener("click", function () {
            dropdownContent.classList.remove("show");
        });
    }
});


  

  





























