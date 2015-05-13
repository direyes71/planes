$(document).ready(function(e){

	//alert("hola");


 		// INTERFAZ ACTIONS ******************************************************
		// actiones stage()

		var flag_stage = 0;

 		$("#buttom_add_stage").click(function(e){ 			

 			if (flag_stage == 0){
 				//$("#add_block").css("display","block");
 				$("#add_block").slideDown("slow");
 				flag_stage = 1;
 			}else{
 				$("#add_block").slideUp("slow");
 				flag_stage = 0;
 			}

 		});


 		$.post("ajax/test.php",data,function(reques){
 			console.log("done 1");

 			

 		}).done(function(reques){
 			console.log("done 2");

 		});


 		// END INTERFAZ ACTIONS ******************************************************


});