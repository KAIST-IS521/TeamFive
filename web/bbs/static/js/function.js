// Closes the Responsive Menu on Menu Item Click
var test;
$('.navbar li').click(function(e) {
    $('.navbar li.active').removeClass('active');
    var $this = $(this);
    if (!$this.hasClass('active')) {
        $this.addClass('active');
    }
	if(e.target.innerText.toLowerCase() != "Home"){
		$("#siteloader").load('/bbs/'+e.target.innerText.toLowerCase());
	}
});

$(document).ready(function(e){
    var $url= $(document)[0].URL;
    //If challenge Page, Don't Move
    if ($url.search("auth/chal") >= 0){
        $("#navauth").addClass('active');
        return;
    }

    if( $url.indexOf('#') > 0){
        var $hash = $url.substring($url.indexOf('#')+1).toLowerCase();
    	$("#siteloader").load('/bbs/'+$hash);
        $("#nav"+$hash).addClass('active');
    }
    else{
	    $("#siteloader").load('/bbs/home');
        $("#navhome").addClass('active');
    }
});


// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    if($(this).attr("data-toggle") != "dropdown"){
        $('.navbar-toggle:visible').click();
    }
});
