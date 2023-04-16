var elements = document.querySelectorAll(".delete-file-button");


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


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
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                return confirm("Вы действительно хотите удалить файл?");
            }
        })
    };
}