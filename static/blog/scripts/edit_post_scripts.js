'use strict';

// when form of page is submitted (by #save_button being clicked/enter pressed)
$("#edit_post_form").submit(function(event) {
	var url, data, success_msg;
	// set up submitting div
	$("#submitting_cover").html("Saving post...");
	$("#submitting_cover").show();
	// send form info to ajax manager page
	url = "/blog/manage/ajax_manager";
	data = $("#edit_post_form").serialize();
	$.ajax({
		type: 'POST',
		url: url,
		data: data,
		success: function(data) {
			if(data === "UPDATE SUCCESSFUL") {
				success_msg = "Saved. &#10003;";
			} else {
				success_msg = "Save failed. &#10007;";
			}
			$("#submitting_cover").html(success_msg);
			setTimeout(function() {
				$("#submitting_cover").fadeOut(500, function() {
					$("#submitting_cover").hide(); // set display to none
				});
			}, 750);
		}
	});
	return false;
});

$("#view_button").click(function() {
	alert("View Draft button clicked.");
});
