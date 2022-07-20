// $(document).ready(function () {
//     console.log('working');
//     $('.plus-btn').click(function () {
//         console.log('clicked');
//         var id = $(this).attr("pid").toString();
//         var eml = this.parentNode.children[2]
//         // var sp=document.getElementById('tt');
//         $.ajax({
//             type: "GET",
//             url: "/pluscart/",
//             data: {
//                 p_id: id
//             },
//             success: function (data) {
//                 console.log('plus')
//                 console.log(data);
//                 document.getElementById('quantity').textContent = data.quantity
//                 document.getElementById('mrp').textContent = data.amount;
//                 document.getElementById('tamount').textContent = data.totalamount


//             }
//         })
//     })

//     $('.minus-btn').click(function () {
//         console.log('clicked');
//         var idm = $(this).attr("id").toString();
//         var eml = this.parentNode.children[2]
//         $.ajax({
//             type: "GET",
//             url: "/minuscart/",
//             data: {
//                 pid: idm,
//             },
//             success: function (data) {
//                 console.log(data);
//                 // eml.innerText = data.quantity;
//                 // $('#tt').text(data.quantity);
//                 // sp.innerText=data.quantity;
//                 document.getElementById('quantity').textContent = data.quantity
//                 document.getElementById('mrp').textContent = data.amount;
//                 document.getElementById('tamount').textContent = data.totalamount


//             }
//         })
//     })

//     $('.t-btn').click(function () {
//         console.log('clicked');
//         var id = $(this).attr("id").toString();
//         var rw = document.getElementById('cart_' + id)
//         $.ajax({
//             type: "GET",
//             url: "/removeproduct/",
//             data: {
//                 pid: id,
//             },
//             success: function (data) {
//                 console.log(data);
//                 document.getElementById('mrp').innerText = data.amount;
//                 document.getElementById('tamount').innerText = data.totalamount
//                 rw.remove()

//             }


//         })
//     })

// })

