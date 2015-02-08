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
    return render(request, 'backendStuffs/index.html', {})

@csrf_exempt
def createUser(request):
	userPhoneNumber = request.POST.get("userPhoneNumber")
	if len(UserPhone.objects.filter(phone_number = userPhoneNumber)) == 0 :
		firstName = request.POST.get("firstName")
		regionCode = request.POST.get("regionCode")

		newUser = UserPhone(phone_number=userPhoneNumber, name = firstName, region = regionCode)
		newUser.save()

		response = HttpResponse()
		sendSmsVerificationCode(request)
		response.status_code = 200
		response.__setitem__("Access-Control-Allow-Origin", "*")
		return response
	else:
		return sendSmsVerificationCode(request)

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
	response.__setitem__("Access-Control-Allow-Origin", "*")
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
		response = JsonResponse({"firstName": firstName, "groupsWithStatus": groupsWithStatus, "location": location})
		response.__setitem__("Access-Control-Allow-Origin", "*")
		return response
	else:
		response = HttpResponse()
		response.status_code = 401
		response.__setitem__("Access-Control-Allow-Origin", "*")
		return response

@csrf_exempt
def checkWhetherSmsVerificationCodeIsValidAndReturnAToken(request):
	userPhoneNumberToVerify = request.POST.get("number")
	verificationCode = request.POST.get("verificationCode")

	print userPhoneNumberToVerify
	user = UserPhone.objects.get(phone_number = userPhoneNumberToVerify)

	isValidCode = int(user.verificationNumber) == int(verificationCode)

    # TODO: This token should have an expiration time.
	newMagicTokenForThisUser = "{0:09d}".format(randint(0,999999999))
	user.token = newMagicTokenForThisUser
	user.save()

	if isValidCode:
		response = JsonResponse({"authToken": newMagicTokenForThisUser})
		response.__setitem__("Access-Control-Allow-Origin", "*")
		return response
	else:
		response = HttpResponse()
		response.status_code = 401
		return response

@csrf_exempt
def sendSmsVerificationCode(request):
	userPhoneNumberToVerify = request.POST.get("userPhoneNumber")
	print userPhoneNumberToVerify

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
	response.__setitem__("Access-Control-Allow-Origin", "*")
	return response

@csrf_exempt
def giveMeRegions(request):
	myResponse = JsonResponse([{"code":x[0], "name":x[1]} for x in regionChoices], safe = False)
	myResponse.__setitem__("Access-Control-Allow-Origin", "*")
	return myResponse

@csrf_exempt
def relayMessageToGroup(request):
	print request.POST.get("From")[2:]
	thing = request.POST.get("From")[2:]
	user = UserPhone.objects.get(phone_number = thing)
	print ""
	print "Hey"
	toNumber = request.POST.get("To")
	post = request.POST.get("Body")
	group = UserinGroup.objects.filter(region = user.region).get(user = user)
	groupList =[x.user for x in UserinGroup.objects.filter(region = group.region).filter(name = group.name).exclude(user = user)] 

	ACCOUNT_SID = "ACf3f0805e01bc0a3db41e7aae79bc96d5"
	AUTH_TOKEN = "acf544c7ffb70d7b888eabc81d75698a"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	for i in groupList:
		client.messages.create(
			to=i.phone_number,
			from_=toNumber,
			body=post,
		)

	response = HttpResponse()
	response.status_code = 200
	response.__setitem__("Access-Control-Allow-Origin", "*")
	return response

@csrf_exempt
def getGroupsInArea(request):
	area = request.GET.get("region")
	user = UserPhone.objects.get(phone_number = request.GET.get("phoneNumber"))
	print user

	# This is a public API, so no need for security check.
	# authToken = request.GET.get("securityToken")
	# if  int(user.token) != int(authToken):
	# 	response = HttpResponse()
	# 	response.status_code = 401
	# 	return response
	# response = []

	allUserGroups = list(UserinGroup.objects.filter(region = area).filter(user = user).filter(isOn = True).values("name","isOn","region").distinct())
	print allUserGroups
	for i in  UserinGroup.objects.filter(region = area).exclude(user = user).values("name","isOn","region").distinct():
		i["isOn"] = False
		allUserGroups.append(i)

	t = loader.get_template('backendStuffs/templatForTable.html')
	c = RequestContext(request, {"listi":allUserGroups})
	theRenderedContents = t.render(c)

	myResponse = HttpResponse()
	myResponse.__setitem__("Access-Control-Allow-Origin", "*")
	myResponse['content_type'] = "application/xhtml+xml"
	myResponse.content = theRenderedContents
	return myResponse

@csrf_exempt
def createGroup(request):
	token = request.POST.get("token")
	groupName = request.POST.get("name")
	user = UserPhone.objects.filter(token = token)[0]
	if(len(UserinGroup.objects.filter(region = user.region).filter(name = groupName) )> 0):
		return JsonResponse({"status":"fail", "Reason":"name taken"})
	newGroup = UserinGroup(region = user.region, user = user, name = groupName, description = "dfkjahfladkfa", twilioNumber = "14012065509")
