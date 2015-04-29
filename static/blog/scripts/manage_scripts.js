'use strict';

$('.hide_show_link').click(function(event) {
	var url, data, url_id;
	// get url_id of post
	url_id = $(event.target).closest("tr").children(".post_title_col").children("a").attr('href');
	url_id = url_id.substr(url_id.lastIndexOf('/') + 1);
	// handle AJAX request
	url = '/blog/manage/ajax_manager';
	data = 'request_type=hide_show_post&url_id=' + url_id;
	$.ajax({
		type: 'POST',
		url: url,
		data: data,
		success: function(data) {
			if(data === "POST HIDDEN") {
				$(event.target).html("Show");
			} else if(data === "POST SHOWN") {
				$(event.target).html("Hide");
			} else {
				console.log("Error while hiding/showing post.");
			}
		}
	});
	return false;
});
