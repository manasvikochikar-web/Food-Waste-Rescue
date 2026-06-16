// Add this in your script file to trigger the payment modal
function initiatePayment(amount) {
    var options = {
        "key": "YOUR_RAZORPAY_KEY_ID",
        "amount": amount * 100, // Amount in paise
        "currency": "INR",
        "name": "Project Name",
        "description": "Donation",
        "handler": function (response){
            alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
        }
    };
    var rzp1 = new Razorpay(options);
    rzp1.open();
}