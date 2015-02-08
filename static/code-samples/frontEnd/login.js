var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.
var num;
var token;
var authencookie;

function getcode(data){
		alert("verification number sent successfully");
		return true;
}


function validate(){
	num = $("#phoneNumber").val();	
	if(num.length == 0 ){
		alert("please enter your phone number!");
	}
    console.log(num);
	$.ajax({
    type: "POST",
    data:{"userPhoneNumber":num},
    url: "http://www.yosephradding.com:8000/sendSmsVerificationCode",
    success: function(){
        alert('horray! 200 status code!');
    },

    statusCode: {
    401: function() {
       alert('bad request');
    }}});
}

$("#signinform").submit(function (e) {
    login();
    e.preventDefault();
    return false;
});


function login(){
    num = $("#phoneNumber").val();
    var code = document.getElementById("verify").value;
	if(code.length == 0 ){
		alert("please enter your verifation number");
		return;
    }
	console.log(num);

    $.ajax({
    type: 'POST',
    data:{"number":$("#phoneNumber").val(),"verificationCode":code},
    url: "http://www.yosephradding.com:8000/checkWhetherSmsVerificationCodeIsValidAndReturnAToken",
    success: function(data){
        alert('1111111111111horray! 200 status code!');
        token = data.authToken;
        $.ajax({
            type: 'POST',
            data:{"number":num,"securityToken":token},
            url: "http://www.yosephradding.com:8000/getUserInfo",
            success: function(data){
                alert('22222222222222horray! 200 status code!');
                login_screen(data);
            }
        })

    },
    statusCode: {
    401: function() {
       alert('bad request');
    }}});

    console.log(window.token);

	return;	
}

function login_screen(data){
	// alert("adfasdfs");
    x = $("nav");
    $("body").empty();
    $("body").append(x);
	$("#tobereplaced").html("<p style= ' color:white; font-size : 20px; position:absolute; left:800px; top:15px'> Welcome, </p> ");
	$("#tobereplaced").html("<p style= ' color:white; font-size : 20px; position:relative; left:500px; top:15px'> Welcome, " + data.firstName + "</p> ");
    // $("#signscreen").empty();
    // $("#container3").empty();
    // $("jumbotron")
    
}

function create_account(){
    window.scrollBy(0,4000); // horizontal and vertical scroll increments
}

function signupAccount(){
    console.log($("#phone").val());
    $.ajax({
        type:"POST",
        data:{"verificationCode":$("#ver").val(),"number":$("#phone").val()},
        url: "http://www.yosephradding.com:8000/checkWhetherSmsVerificationCodeIsValidAndReturnAToken",
        success: function(data){
        authencookie= data.authToken;
        localstorage.setItem("turnedOnCookie",authencookie)
        // alert('horray! 200 status code! token = '+ authencookie);
        login_screen();
    },

    statusCode: {
    401: function() {
       alert('bad request');
    }}});
}

function getver(){
    num = $("#phone").val(); 
    name = $("#firstname").val();
    region = $("#region").val();
    if(num.length == 0 ){
        alert("please enter your phone number!");
    }else if(name.length==0){
        alert("please enter your name!");
    }else{
        $.ajax({
            type: 'POST',
            data:{"userPhoneNumber":num,"firstName":name,"regionCode":region},
            url: "http://www.yosephradding.com:8000/createUser",
            success: function(data){
                token= data.authToken;
                alert('horray! 200 status code! token = '+ token);
                login_screen();
            }
        // $.get("http://www.yosephradding.com:8000/sendSmsVerificationCode/"+num, getcode);    
        });
    }
}

function handleGroupOnOff(theGroupCheckbox)
{
	var urlToHit = theGroupCheckbox.checked ? "http://yosephradding.com:8000/subscribeUserToGroup" : "http://yosephradding.com:8000/unsubscribeUserFromGroup";
	
	if (num == null)
	{
    	num = $("#phoneNumber").val();
    }
    
	// The user just turned this group on or off.
	$.ajax({
		type: 'POST',
	    url: urlToHit,
	    data: { userPhoneNumber: num, groupName: theGroupCheckbox.value, securityToken: token },
	    success: function(data)
	    {
			// Nothing to do except celebrate.
	    },
	    statusCode:
	    {
	    	401: function()
	    	{
	    	   alert('not authorized');
	    	}
		}
	});
}

function onCityWasChanged(cityDropdown)
{
	var selectedCityCode = $(cityDropdown).val();
	
	if (num == null)
	{
    	num = $("#phoneNumber").val();
    }
	
	// The user just turned this group on or off.
	$.ajax({
		type: "GET",
	    url: "http://yosephradding.com:8000/getGroupsInArea",
	    data: { phoneNumber: num, region: selectedCityCode, securityToken: token },
	    success: function(data)
	    {
			$('#divOfAllGroups').html(data);
	    },
	    statusCode:
	    {
	    	401: function()
	    	{
	    	   alert('not authorized');
	    	}
		}
	});
}
