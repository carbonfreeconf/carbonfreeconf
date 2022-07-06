from .models import Post, CreateConf, UserLink, RegisterConf
from django.db.models import Q
from datetime import datetime, timedelta, date
from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from django.conf import settings



def add_news_to_context(request):
    queryset = Post.objects.filter(status=1).order_by('-created_on')[:3]
    stuff_for_frontend = {
        'post_list': queryset,
    }
    return stuff_for_frontend

def add_confs_to_context(request):
    queryset2 = CreateConf.objects.filter(Q(start_date__gte=date.today()) | Q(start_date=None)).exclude(status=0).order_by('start_date')[:3]
    #print('query',len(queryset2),queryset2)
    #queryset3=queryset2[0:3]
    #print('q',queryset3)
    stuff_for_frontend = {
        'conf_list': queryset2
    }
    return stuff_for_frontend


def token(request):
    if not request.user.is_authenticated:
        stuff_for_frontend = {
            'resumetoken': None
        }
        return stuff_for_frontend
    else:
        if request.session.get('tokenrc', ''):
            restoken=request.session['tokenrc']
        else:
            try:
                with sessions.Session() as session:
                    rocket = RocketChat('carbonfreeconf', settings.SECRETROCK, server_url='https://chat.carbonfreeconf.com',
                                        session=session)

                    tok = rocket.users_create_token(username=request.user.username).json()
                    #print(tok)
                    key = tok['data']['authToken']
                    #print('key', key)
                    restoken = key
                    request.session['tokenrc'] = restoken

                    rocket.logout()
            except:
                restoken = ''


        stuff_for_frontend = {
            'resumetoken': restoken
        }
        return stuff_for_frontend