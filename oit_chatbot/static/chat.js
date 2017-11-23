$(document).ready(function(){
    
   });

$("#submitmsg").click(function(){	
    var clientmsg = $("#boxmsg").val();
    console.log(clientmsg);
    $("#chatbox").append("<p id=usermsg>" + clientmsg + "</p>");
    $.post("/process_message", {text: clientmsg}, function(responseText) {
        console.log(responseText);
        $("#chatbox").append("<p id=botmsg>"+responseText+"</p>");
    });	
    $("#boxmsg").attr("value", "");
    return false;
});
