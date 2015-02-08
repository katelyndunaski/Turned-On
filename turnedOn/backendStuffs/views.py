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
    # import twilio.rest
    return JsonResponse({"text":"hi"})

@csrf_exempt
def createUser(request):
	userPhoneNumber = request.POST.get("userPhoneNumber")
	firstName = request.POST.get("firstName")
	regionCode = request.POST.get("regionCode")

	newUser = UserPhone(phone_number=userPhoneNumber, name = firstName, region = regionCode)
	newUser.save()

	response = HttpResponse()
	response.status_code = 200
	return response

@csrf_exempt
def subscribeUserToGroup(request):
	userPhoneNumber = request.POST.get("userPhoneNumber")
	groupName = request.POST.get("groupName")
	securityToken = request.POST.get("securityToken")

	user = UserPhone.objects.get(phone_number = userPhoneNumber)

	isValidToken = int(user.token) == int(securityToken)

	if not isValidToken:
		response = HttpResponse()
		response.status_code = 401
		return response

	# TODO: dynamically find a Twilio number that has not been used yet for this user for any groups.
	twilioNumber = '4012164446'

	myGroupMembership = UserinGroup(user = user, name = groupName, region = user.region, isOn = True, twilioNumber = twilioNumber)
	myGroupMembership.save()

	ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5"
	AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a"
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	client.messages.create(
		to=userPhoneNumberToVerify,
		from_=fromNumber,
		body="Welcome to the {0} group! Here is where you will see all posts pertain to this group.Reply to create Post".format(groupName),
	)

	response = HttpResponse()
	response.status_code = 200
	return response

@csrf_exempt
def getUserInfo(request):
	userPhoneNumberToVerify = request.POST.get("number")
	securityToken = request.POST.get("securityToken")

	# TODO: Make sure the securityToken is not expired.

	user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)

	isValidToken = int(user.token) == int(securityToken)

	if isValidToken:
		groupsWithStatus = list(UserinGroup.objects.filter(user = userPhoneNumberToVerify))
		firstName = user.name
		location = user.region

		return JsonResponse({"firstName": firstName, "groupsWithStatus": groupsWithStatus, "location": location})
	else:
		response = HttpResponse()
		response.status_code = 401
		return response

@csrf_exempt
def checkWhetherSmsVerificationCodeIsValidAndReturnAToken(request):
	userPhoneNumberToVerify = request.POST.get("number")
	verificationCode = request.POST.get("verificationCode")

	user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)

	isValidCode = int(user.verificationNumber) == int(verificationCode)

    # TODO: This token should have an expiration time.
	newMagicTokenForThisUser = "{0:09d}".format(randint(0,999999999))
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

	# This should be the "master number" for our Twilio account.
	fromNumber = "+14012065509"

	ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5"
	AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	verificationCode = "{0:04d}".format(randint(0,9999))

        user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)
        user.verificationNumber = verificationCode
        user.save()

	client.messages.create(
		to=userPhoneNumberToVerify,
		from_=fromNumber,
		body="Here is your TurnedOn verification code: " + verificationCode,
	)

	response = HttpResponse()
	response.status_code = 200
	return response

@csrf_exempt
def giveMeRegions(request):
	return(JsonResponse([{"code":x[0], "name":x[1]} for x in regionChoices]))

@csrf_exempt
def relayMessageToGroup(request):
	user = UserPhone.objects.get(phone_number = request.POST.get("phoneNumber"))

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
