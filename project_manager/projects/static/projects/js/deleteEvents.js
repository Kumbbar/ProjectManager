var elements = document.querySelectorAll(".delete-event");
for (var i = 0; i < elements.length; i++) {
    let eventId = elements[i].id
    elements[i].onclick = function(){
        $.ajax({
            url: BASE_URL + 'tasks/' + taskId +'/events/delete/' + eventId,
            type: 'POST',
            async: false,
            success: function (data) {
            document.getElementById(eventId + '-table').remove();
            },
            beforeSend:function(){
             return confirm("Вы действительно хотите удалить событие?");
            }
        })
    };
}