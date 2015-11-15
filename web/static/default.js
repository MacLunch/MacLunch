function initButtonClick(){
	$('button#recog-submit').on('click', function(){
		var json_data = {
			id: $('#pk-input').val(),
			text: $('#text-input').val(),
		};
		var json_list = [];
		var url_with_key = "/api/recognize?api_key=" + $('#apikey-input').val();

		json_list[0] = json_data;

		$.ajax({
			type: 'POST',
			url: url_with_key,
			encoding: 'utf-8',
			contentType: 'application/json; charset=UTF-8',
			data: JSON.stringify(json_list),
			dataType: "json",
			success: function(response){
				console.log(response);
			}
		});
		return false;
	});

	$('button#enroll-submit').on('click', function(){
		var json_data = {
			id: $('#pk-enroll').val(),
			text: $('#text-enroll').val(),
			is_spam: $('#label-enroll').val(),
		};
		var data = [];
		var api_key = $('#apikey-enroll').val();
		data[0] = json_data;

        $.ajax({
			type: 'POST',
			url: '/api/enroll?api_key=' + api_key,
			encoding: 'utf-8',
			contentType: 'application/json; charset=UTF-8',
			data: JSON.stringify(data),
			dataType: "json",
			success: function(response){
				console.log(response);
			}
		});

		return false;
	});
}

$(function(){
	initButtonClick();
});

