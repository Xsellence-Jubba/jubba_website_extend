$(document).ready(function () {
    // Select all radio buttons with the name 'delivery_method'
    $('input[name="delivery_method"]').on('click', function () {

        // 'this' refers to the radio button that was just clicked
        var selectedDeliveryId = $(this).attr('id');
        var selectedDeliveryPrice = $(this).attr('data_price');
        var deliveryAreaText = $(this).siblings('label').text().trim().split('\n')[0].trim(); // Extract the 'Inside Dhaka' or 'Outside Dhaka' text

        // Log the details to the console (you can replace this with your actual logic)
        console.log('--- Delivery Method Clicked ---');
        console.log('ID:', selectedDeliveryId);
        console.log('Delivery Area:', deliveryAreaText);
        console.log('Price (as string from data_price attribute):', selectedDeliveryPrice);

        // Example: Convert the price to a number (float)
        var numericPrice = parseFloat(selectedDeliveryPrice);
        console.log('Price (as number):', numericPrice);

        // --- Your custom logic goes here ---
        // For example, you might want to:
        // 1. Update a "Total Cost" field on the page
        // 2. Make an AJAX call to update the cart/order details
        // ------------------------------------

    });
});