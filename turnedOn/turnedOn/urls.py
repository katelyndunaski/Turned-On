from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turnedOn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sendSmsVerificationCode', 'backendStuffs.views.sendSmsVerificationCode', name='sendSmsVerificationCode'),
    url(r'^checkWhetherSmsVerificationCodeIsValidAndReturnAToken', 'backendStuffs.views.checkWhetherSmsVerificationCodeIsValidAndReturnAToken', name='checkWhetherSmsVerificationCodeIsValidAndReturnAToken'),
    url(r'^getUserInfo', 'backendStuffs.views.getUserInfo', name='getUserInfo'),
)
