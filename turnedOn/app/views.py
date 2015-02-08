"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime
from random import randint
from twilio.rest import TwilioRestClient

def home(request):
    """Renders the home page."""
    import twilio.rest
    return JsonResponse({"text":"hi"})

def checkWhetherSmsVerificationCodeIsValidAndReturnAToken(request, userPhoneNumberToVerify, verificationCode):
	# TODO: need to check the provided code against the value stored in the database for that phone number.
	isValidCode = true
	
	# TODO: this code should be stored in the database with an expiration time.
	newMagicTokenForThisUser = "{0:09d}".format(randint(0,999999999))

	if isValidCode:
		return JsonResponse({"authToken": newMagicTokenForThisUser})
	else:
		response = HttpResponse()
		response.status_code = 401
		return response

def sendSmsVerificationCode(request, userPhoneNumberToVerify):
	# This should be the "master number" for our Twilio account.
	fromNumber = "+14012065509"

	ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5"
	AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# TODO: this code should be stored in the database as a valid code for this user.
	verificationCode = "{0:04d}".format(randint(0,9999))

	# userPhoneNumberToVerify = "2063838296"

	client.messages.create(
		to=userPhoneNumberToVerify,
		from_=fromNumber,
		body="Here is your TurnedOn verification code: " + verificationCode,
	)

	response = HttpResponse()
	response.status_code = 200
	return response

def contact(request):
    """Renders the contact page."""

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
