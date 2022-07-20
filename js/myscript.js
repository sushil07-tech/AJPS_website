$('.plus').click(function(){
    var id=$(this).attr("id").toString();
    console.log(id)
    // $.ajax({
    //     type:"GET",
    //     url : "/pluscart",
    //     data:{
    //         pid=id
    //     },
    //     success:function(data){
    //         console.log(data)
    //     }
    // });
})