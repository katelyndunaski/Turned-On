from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turnedOn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sendSmsVerificationCode/(?P<userPhoneNumberToVerify>\d{10})', 'backendStuffs.views.sendSmsVerificationCode', name='sendSmsVerificationCode'),
    url(r'^checkWhetherSmsVerificationCodeIsValidAndReturnAToken/forPhoneNumber/(?P<userPhoneNumberToVerify>\d{10})/withCode/(?P<verificationCode>\d{9})', 'backendStuffs.views.checkWhetherSmsVerificationCodeIsValidAndReturnAToken', name='checkWhetherSmsVerificationCodeIsValidAndReturnAToken'),
    url(r'^getUserInfo/forPhoneNumber/(?P<userPhoneNumberToVerify>\d{10})/withToken/(?P<securityToken>\d{9})', 'backendStuffs.views.getUserInfo', name='getUserInfo'),
)
