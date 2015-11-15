function initButtonClick(){
	$('button#recog-submit').on('click', function(){
		var json_data = {
			pk: $('#pk-input').val(),
			text: $('#text-input').val(),
		}

		$.ajax({
			type:'POST',
			url:'/api/recognize',
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

	$('button#enroll-submit').on('click', function(){
		var json_data = {
			id: $('#pk-enroll').val(),
			text: $('#text-enroll').val(),
			is_spam: $('#label-enroll').val(),
			api_key: $('#apikey-enroll').val()
		}

		$.ajax({
			type:'POST',
			url:'/api/enroll',
			encoding:'utf-8',
			contentType:'application/json; charset=UTF-8',
			data: JSON.stringify(json_data),
			dataType: "json",
			success:function(dataFromServer){
				console.log("success");
			}
		});
		return false;
	});
}

$(function(){
	initButtonClick();
});

