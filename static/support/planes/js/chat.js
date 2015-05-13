/* $(document).ready(function(e){
	
// see more options
var site_height = $(document).height();
// mask config 

$(".mask").css("height",site_height);
//--
//  modal config//

var modal_height = "500px";
var modal_width = "700px";

// ---

$("#chat_content, #publicationsproject").on("click",".see_more_chat",function(e){
	e.preventDefault();
	$(".mask").fadeIn("slow");	
	idPublication =  $(this).attr("href");

	var idProject = $("#project").val(); 
	var valCookie = getCookie("sessionid");

	//alert(valCookie);
	console.log("cookie",valCookie);
	$(".modal_chat").html("cargando...");
	setParamsModal(".modal_chat");

	$.post("/inverboy/home/ajax/commentspublishedproject/"+idPublication+"/"+idProject+"/",{"sessionid":valCookie},function(result){
		//alert("si");
		//if (typeof result == "string") console.log("string");
		//var result2 =  jQuery.parseJSON(result);
		console.log(result);		
		$(".modal_chat").html(result.data.html);
		var sly2 = new Sly("#modal_frame",{
                            scrollBar : $("#modal_scrollbar"),
                            dragHandle : 10
                        });
		sly2.init();

		
	});
});

$(".mask, .btn_exit").click(function(e){
	$(this).fadeOut("slow");	
	mask_exit(".modal_chat");
});

$(".modal_chat").on("click",".btn_exit",function(e){
	$(".mask").fadeOut("slow");	
	mask_exit(".modal_chat");
});


$(".modal_chat").hide();

function mask_exit(modal){
	modal = modal || "";
	 	
	if (modal !== "" || typeof modal !== "undefined"){		
		$(modal).fadeOut("slow");	
	}else {console.log("no modal");}
	 
}


function setParamsModal(modal){
	var modal = $(modal);
	var window_pos_top = $(window).scrollTop();
	var window_height = $(window).height();
	var window_width = $(window).width();

	var modal_pos_y = (window_pos_top + (window_height/2)) - modal.height()/2;
	var modal_pos_x = (window_width/2) - (modal.width()/2);

	modal.css("margin-top",modal_pos_y);
	modal.css("margin-left",modal_pos_x);
	modal.fadeIn("slow");


	console.log(window_pos_top + " altura ventana" +window_height);
	console.log(" pos_y: "+modal_pos_y + " pos_x" +modal_pos_x);
	console.log(" modal width: "+modal.width());
	//$()
}

});

*/

function getCookie(cname)
{
var name = cname + "=";
var ca = document.cookie.split(';');
for(var i=0; i<ca.length; i++) 
  {
  var c = ca[i].trim();
  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
return "";
}