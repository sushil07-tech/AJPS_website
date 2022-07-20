$(document).ready(function () {

    $('.opmt').click(function () {
        console.log("click");
        // e.preventDefault();
        var cid=$("input[name=custadd]:checked").val();
        var token=$("[name='csrfmiddlewaretoken']").val();
        console.log(cid);
        $.ajax({
            type: "GET",
            url: "/proceed-to-payment/", 
            success: function (response) {
                console.log(response.total_price)
                var options = {
                    "key": "rzp_test_kEeGQKSYn34WqE", // Enter the Key ID generated from the Dashboard
                    "amount": (response.total_price)*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR", 
                    
                    "name": "AJPS",
                    "description": "ThankYou for Shopping with us.Please visit again.",
                    "image": "https://example.com/your_logo",
                    // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (response1) {
                        alert(response1.razorpay_payment_id);
                        data={
                            "custadd":cid,
                            "payment_mode":"Paid Online",
                            "payment_id":response1.razorpay_payment_id,
                            csrfmiddlewaretoken:token,
                        }
                        $.ajax({
                            type: "POST",
                            url: "/place/",
                            data: data,
                            success: function (p) { 
                                swal("Congratulations!",p.status,"success")
                                .then((value) => {
                                    window.location.href='/myorders/'
                                  });
                                
                                
                            }
            
            
                        })

                    },
                    // "prefill": {
                    //     "name": "",
                    //     "email":"",
                    //     "contact": ""
                    // },
                    "theme": {
                        "color": "#3399cc"
                    }


                };
                var rzp1 = new Razorpay(options);
                rzp1.open();




            }


        });


    });
});