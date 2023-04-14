var elements = document.querySelectorAll(".delete-file-button");
for (var i = 0; i < elements.length; i++) {
    let fileId = elements[i].id
    elements[i].onclick = function(){
        $.ajax({
            url: BASE_URL + 'tasks/' + taskId +'/files/delete/' + fileId,
            type: 'POST',
            async: false,
            success: function (data) {
            document.getElementById(fileId + '-tr').remove();
            },
            beforeSend:function(){
             return confirm("Вы действительно хотите удалить файл?");
            }
        })
    };
}