var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.

var token;
var authencookie;

function getcode(data){
		alert("verfication number sent successfully");
		return true;
}


function validate(){
	var num = document.getElementById("phoneNumber").value;	
	if(num.length == 0 ){
		alert("please enter your phone number!");
	}
	$.get("http://www.yosephradding.com:8000/sendSmsVerificationCode/"+num, getcode);
/**
	$.ajax({
    type: 'GET',
    url: "http://www.yosephradding.com:8000/sendSmsVerificationCode/"+num,
    success: function(data){
        alert("phone worked");
    },
    statusCode: {
    401: function() {
       alert('bad request');
   	}}});
**/

}

$("#signinform").submit(function (e) {
    login();
    e.preventDefault();
    return false;
})


function login(){
	var code = document.getElementById("verify").value;
	var num = document.getElementById("phoneNumber").value;
    login_screen();
    return;

	if(code.length == 0 ){
		alert("please enter your verifation number");
		return;
	}
	
	$.ajax({
    type: 'GET',
    url: "http://http://www.yosephradding.com:8000/checkWhetherSmsVerificationCodeIsValidAndReturnAToken/forPhoneNumber/"
    			+document.getElementById("phoneNumber")+"/withCode/"+code,
    success: function(data){
        token= data.authToken;
        alert('horray! 200 status code! token = '+ token);
        login_screen();
    },

    statusCode: {
    401: function() {
       alert('bad request');
   	}}});
	
	return;	
}

function login_screen(){
	// alert("adfasdfs");
	$("#tobereplaced").html("<p style= ' color:white; font-size : 20px; position:absolute; left:800px; top:15px'> Welcome, </p> ");
	$("#tobereplaced").html("<p style= ' color:white; font-size : 20px; position:relative; left:500px; top:15px'> Welcome, " + "INSTERT TOKEN" + "</p> ");
    $("#replaceAfterLogin1").empty();

}

function create_account(){
    window.scrollBy(0,700); // horizontal and vertical scroll increments
}

function signupAccount(){
    $ajax({
        type:"POST",
        data:{"userPhoneNumber":"2063838296", "firstName":"Adam", "regionCode":"SCA"},
        url: "http://www.yosephradding.com:8000/create",
        success: function(data){
        alert('horray! 200 status code! token = '+ token);
        authencookie= data.authToken;
        login_screen();
    },

    statusCode: {
    401: function() {
       alert('bad request');
    }}});
}

function getver(){
    var num = document.getElementById("getVerNum").value; 
    var name = document.getElementById("fistname").value;
    if(num.length == 0 ){
        alert("please enter your phone number!");
    }else if(name.length==0){
        alert("please enter your name!");
    }else{
        $.get("http://www.yosephradding.com:8000/sendSmsVerificationCode/"+num, getcode);    
    }
}
