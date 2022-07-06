from re import sub
from django.conf import settings
from django.http import HttpResponseRedirect
import os
from conf.settings import DEFAULT_REDIRECT_URL
from django.apps import apps

if not 'ON_HEROKU' in os.environ:
    DEFAULT_REDIRECT_URL = ""
else:
    DEFAULT_REDIRECT_URL = getattr(settings,"DEFAULT_REDIRECT_URL","https://www.carbonfreeconf.com")


def wildcard_redirect(request, pathe=None):

    join=0
    new_url = DEFAULT_REDIRECT_URL
    http_host = str(request.META.get('HTTP_HOST'))
    subdomain = http_host.split('.')[0]
    if pathe:
        if pathe.startswith("join"):
            join=1
            if pathe.startswith("join/"):
                pathe = pathe.replace("join/","")
            else:
                pathe = pathe.replace("join","")
            print('join1',pathe)

    print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',DEFAULT_REDIRECT_URL)

    if not 'ON_HEROKU' in os.environ:
        print('split',request.get_full_path().split('/'))#.split('/'))
        pathe = request.get_full_path().split('/')[0]
        print('path1:',pathe)


    print('subdomains',subdomain)
    print('host',http_host)

    if subdomain:
        
        Website = apps.get_model(app_label='my_app', model_name='Website')
        searchifurlexists = Website.objects.filter(titleurl=subdomain)
        print('searchifurlexists',searchifurlexists)

        if searchifurlexists:
            print('searchifurlexists2',searchifurlexists[0].conference.id)
            if pathe:
                if join==0:
                    print('path:',pathe)
                    new_url = DEFAULT_REDIRECT_URL + "/website/" + str(searchifurlexists[0].conference.id) + "/" + pathe
                else:
                    new_url = DEFAULT_REDIRECT_URL + "/join-conference/" + str(searchifurlexists[0].conference.id) + "/" + pathe

            else:
                if join==0:
                    new_url = DEFAULT_REDIRECT_URL + "/website/" + str(searchifurlexists[0].conference.id) + "/home"
                else:
                    new_url = DEFAULT_REDIRECT_URL + "/join-conference/" + str(searchifurlexists[0].conference.id) + "/"


        else:
            print('no corresponding subdomain')

    print('new_url',new_url)
    return HttpResponseRedirect(new_url)