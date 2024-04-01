$('.cart13').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:'GET',
        URL:'/plus',
        data:{
            pro_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
        }

    })
})