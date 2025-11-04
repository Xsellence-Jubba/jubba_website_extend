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

});