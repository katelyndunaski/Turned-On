from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turnedOn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'backendStuffs.views.home', name='home'),
    url(r'^sendSmsVerificationCode', 'backendStuffs.views.sendSmsVerificationCode', name='sendSmsVerificationCode'),
    url(r'^checkWhetherSmsVerificationCodeIsValidAndReturnAToken', 'backendStuffs.views.checkWhetherSmsVerificationCodeIsValidAndReturnAToken', name='checkWhetherSmsVerificationCodeIsValidAndReturnAToken'),
    url(r'^getUserInfo', 'backendStuffs.views.getUserInfo', name='getUserInfo'),
    url(r'^create', 'backendStuffs.views.createUser', name='create'),
    url(r'^subscribeUserToGroup', 'backendStuffs.views.subscribeUserToGroup', name='subscribeUserToGroup'),
    url(r'^giveMeRegions', 'backendStuffs.views.giveMeRegions', name='giveMeRegions'),
    url(r'^getGroupsInArea', 'backendStuffs.views.getGroupsInArea', name='getGroupsInArea'),
    url(r'^relay', 'backendStuffs.views.relayMessageToGroup', name='relayMessageToGroup'),
)

