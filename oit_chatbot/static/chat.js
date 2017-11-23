$(document).ready(function(){
    
   });

$("#submitmsg").click(function(){	
    var clientmsg = $("#usermsg").val();
    $.post("/process_message", {text: clientmsg}, function(responseText) {
        console.log(responseText);
    });	
    $("#usermsg").attr("value", "");
    return false;
});