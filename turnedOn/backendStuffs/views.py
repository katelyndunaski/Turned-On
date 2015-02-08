"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime
from random import randint
from backendStuffs.models import *
from twilio.rest import TwilioRestClient
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    """Renders the home page."""
    import twilio.rest
    return JsonResponse({"text":"hi"})

@csrf_exempt
def createUser(request):
	userPhoneNumber = request.POST.get("userPhoneNumber")
	firstName = request.POST.get("firstName")
	regionCode = request.POST.get("regionCode")

	newUser = UserPhone(userPhoneNumber, firstName, regionCode)
	newUser.save()

	response = HttpResponse()
	response.status_code = 200
	return response

@csrf_exempt
def subscribeUserToGroup(request, userPhoneNumber, groupName, regionCode, securityToken):
	# TODO: validate the security token.

	# TODO: find a Twilio number that has not been used yet for this user for any groups.
	twilioNumber = '4012065509'

	UserinGroup.create(userPhoneNumber, groupName, regionCode, True, twilioNumber)

        response = HttpResponse()
        response.status_code = 200
        return response

@csrf_exempt
def getUserInfo(request, userPhoneNumberToVerify, securityToken):
	# TODO: Make sure it's not expired.
	user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)

	isValidToken = user.token == securityToken

	if isValidToken:
		groupsWithStatus = UserinGroup.objects.filter(user = userPhoneNumberToVerify)
		firstName = user.name
		location = user.region

		return JsonResponse({"firstName": firstName, "groupsWithStatus": groupsWithStatus, "location": location})
	else:
		response = HttpResponse()
		response.status_code = 401
		return response

@csrf_exempt
def checkWhetherSmsVerificationCodeIsValidAndReturnAToken(request, userPhoneNumberToVerify, verificationCode):
	# TODO: need to check the provided code against the value stored in the database for that phone number.
	isValidCode = True

	# This token should have an expiration time.
	newMagicTokenForThisUser = "{0:09d}".format(randint(0,999999999))
	user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)
	user.token = newMagicTokenForThisUser
	user.save()

	if isValidCode:
		return JsonResponse({"authToken": newMagicTokenForThisUser})
	else:
		response = HttpResponse()
		response.status_code = 401
		return response

@csrf_exempt
def sendSmsVerificationCode(request):
	userPhoneNumberToVerify = request.POST.get("userPhoneNumberToVerify")
	print userPhoneNumberToVerify
	# This should be the "master number" for our Twilio account.
	fromNumber = "+14012065509"

	ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5"
	AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	verificationCode = "{0:04d}".format(randint(0,9999))

	# Save the verification code in the database.
	userInfo = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)
	userInfo.verificationNumber = verificationCode
	userInfo.save()

	# userPhoneNumberToVerify = "2063838296"

	client.messages.create(
		to=userPhoneNumberToVerify,
		from_=fromNumber,
		body="Here is your TurnedOn verification code: " + verificationCode,
	)

	response = HttpResponse()
	response.status_code = 200
	return response

# def contact(request):
#     """Renders the contact page."""

#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         })
#     )

# def about(request):
#     """Renders the about page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/about.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'About',
#             'message':'Your application description page.',
#             'year':datetime.now().year,
#         })
#     )
