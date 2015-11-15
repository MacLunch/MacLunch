$(function(){
	$('button#request-btn').on('click', function(){
		var json_data = {
			message : $('textarea#message').val(),
			email : $('input#email-address').val(),
		}

		// Ajax
		$.ajax({
			type:'POST',
			url:'/request',
			encoding:'utf-8',
			contentType:'application/json; charset=UTF-8',
			data: JSON.stringify(json_data),
			dataType: "json",
			success:function(dataFromServer){
				$('#success-modal').modal('show');
				$('#request-modal').modal('hide');
			}
		});
		
		return false;
	});
});