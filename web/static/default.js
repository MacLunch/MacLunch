function initButtonClick(){
	$('button#submit').on('click', function(){
		var json_data = {
			pk : $('input[name="pk"]').val(),
			author : $('input[name="author"]').val(),
			title : $('input[name="title"]').val(),
			forumid : $('input[name="forumid"]').val(),
			text : $('input[name="text"]').val(),
			url : $('input[name="url"]').val()
		}

		$.ajax({
			type:'POST',
			url:'/query',
			encoding:'utf-8',
			contentType:'application/json; charset=UTF-8',
			data: JSON.stringify(json_data),
			dataType: "json",
			success:function(dataFromServer){
				console.log("success");
				var is_troll = dataFromServer;
				console.log(is_troll);
			}
		});
		return false;
	});
}

$(function(){
	initButtonClick();
});

