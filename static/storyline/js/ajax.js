function send(url, data, fn_success) {
	$.ajax({
		type: "POST",
		url: url,
		data: data,
		success: fn_success,
		dataType: "html"
	});
}