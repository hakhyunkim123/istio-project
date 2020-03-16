(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

/*
$(function (){ 
	$("#notice").click(function (){ 
		$("#message_content").hide();
		$("#chatroom_content").hide();
		$("#notice_content").show(); }); 
});

$(function (){ 
	$("#message").click(function (){ 
		$("#notice_content").hide();
		$("#chatroom_content").hide();
		$("#message_content").show(); }); 
});

$(function (){ 
	$("#chatroom").click(function (){ 
		$("#notice_content").hide();
		$("#message_content").hide();
		$("#chatroom_content").show(); }); 
});
*/
