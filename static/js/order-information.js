$(document).ready(function () {

    let data;
    let delivery_amount = 0;
    let subtotal_amount = 0;

    function render_order() {

        subtotal_amount = data.product_total + delivery_amount;

        $('#delivery_amount').text(`${delivery_amount} ৳`);
        $('#subtotal_amount').text(`${subtotal_amount} ৳`);
        $('#taxes_amount').text('0.0 ৳');
        $('#total_amount').text(`${subtotal_amount} ৳`);
    }

    $('input[name="delivery_method"]').on('click', function () {
        var selectedDeliveryPrice = $(this).attr('data_price');
        delivery_amount = parseFloat(selectedDeliveryPrice);
        render_order();
    });

    function onload() {

        let json_data = $('#json_data').val();
        data = JSON.parse(json_data);
        console.log('data', data);

        var selectedDeliveryInput = $('input[name="delivery_method"]:checked');

        if (selectedDeliveryInput.length) {
            var selectedDeliveryPrice = selectedDeliveryInput.attr('data_price');
            delivery_amount = parseFloat(selectedDeliveryPrice);
            render_order();
        }

    }

    onload();

    console.log('Loaded 2')

    // submit
    $('#order_form').submit(function (e) {

        /**
         * Validates a Bangladeshi phone number string based on the following rules:
         * 1. Must be between 11 and 14 characters long.
         * 2. Must only contain digits (0-9).
         * 3. The '+' symbol is allowed only as the very first character.
         *
         * Valid examples: '01731001895' (11 chars), '+8801731001895' (14 chars)
         * Invalid examples: '0173100189', '01731001895a', '8801731001895+', '017-31001895'
         *
         * @param {string} phoneNumber The phone number string to validate.
         * @returns {boolean} True if the phone number is valid, false otherwise.
         */
        function isValidBdPhoneNumber(phoneNumber) {
            if (!phoneNumber || typeof phoneNumber !== 'string') {
                return false;
            }

            // The regex ensures the string matches one of two patterns:
            // 1. Starts with a '+' followed by 10 to 13 digits (Total 11 to 14 characters). -> ^\+\d{10,13}$
            // 2. Contains 11 to 14 digits only (Total 11 to 14 characters). -> ^\d{11,14}$
            // The '|' (OR) operator combines them.
            const bdPhoneRegex = /^(\+\d{10,13}|\d{11,14})$/;

            return bdPhoneRegex.test(phoneNumber);
        }

        let mobile = $('#mobile').val();
        let error = false;
        if (!isValidBdPhoneNumber(mobile)) {
            error = true;
        }

        if (error) {
            e.preventDefault();
            alert('অনুগ্রহ করে একটি সঠিক মোবাইল নম্বর ব্যবহার করুন।');
        }

    })

});