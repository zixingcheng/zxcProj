//ajaxIndex.js
 
$(document).ready(function () {
    $('#btn').on('click',function () {
        //此时使用的是post方式，get方式直接换成get就行
        $.post('/ajax_post', {name:$('#namevalue').val()}, function(data){
            $('#result').text(data);
        })
    })
})
