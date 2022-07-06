import requests
import json
from datetime import datetime, timedelta, date
#from calendar import HTMLCalendar
#from .models import Event
import pytz
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import CreateConf, RegisterConf, People, Schedule, CreateVisio, UserLink, Post
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import os
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Search, Boolean, Integer, Keyword, Completion,analyzer, tokenizer#, fields
#from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
#from elasticsearch_dsl import Q
from urllib.parse import urlparse
from djmoney.contrib.exchange.backends import OpenExchangeRatesBackend
from django.conf import settings
from six.moves import urllib
from xhtml2pdf import pisa
import tweepy
import jwt
import hashlib
import hmac
import base64
import time
import http.client
import string
import secrets
import datetime
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from django.db.models import Q
from django.core.mail import EmailMessage
from django.utils.text import slugify
from pprint import pprint
from django.urls import reverse
from conf.celery import app
from conf.tasks import asynchronouschatsub

def starwarsplanets(intvalue):
    # 42 star wars planets
    starwarsplanets = ['Tatooine',
                       'Coruscant',
                       'Mustafar',
                       'Alderaan',
                       'Naboo',
                       'Jakku',
                       'Eadu',
                       'Kashyyyk',
                       'Geonosis',
                       'Kamino',
                       'Dagobah',
                       'Jedha',
                       'Hoth',
                       'Starkiller Base',
                       'Endor’s Forest Moon',
                       'Bespin',
                       'Scarif',
                       'Castilon',
                       'Chandrila',
                       'Corellia',
                       'Dathomir',
                        'Eriadu',
                        'Exegol',
                        'Felucia',
                        'Fondor',
                        'Kessel',
                        'Mortis',
                        'Rishi',
                        'Ruusan',
                        'Saleucami',
                        'Shili',
                        'Sorgan',
                        'Takodana',
                        'Umbara',
                        'Wobani',
                        'Wrea',
                        'Zeffo',
                        'Yavin',
                        'Zygerria',
                        'Sullust',
                        'Rugosa',
                       'Pillio',]

    return starwarsplanets[intvalue]

def updateratesautomatically():
    OpenExchangeRatesBackend().update_rates()#pas sur que ca marche car je peux pas importer...

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    #pdf = pisa.pisaDocument(BytesIO(template_src.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cross-Origin-Embedder-Policy"] = 'credentialless; report-to="default"'#'credentialless; report-to="default"'#'require-corp; report-to="default"'#cannot add for now as all external libraries do not have corp yet
        response["Cross-Origin-Opener-Policy"] = 'same-origin; report-to="default"'
        response["Cross-Origin-Resource-Policy"] = "same-origin"
        return response

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def process_request(request):
        #print('process')
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            #timezone.activate(pytz.timezone('UTC'))
            timezone.deactivate()
        return None

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        #print('call',tzname)

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            #timezone.activate(pytz.timezone('UTC'))
            timezone.deactivate()
        return self.get_response(request)

def connection(api_url_short):
    api_url_base = 'https://www.bigmarker.com/api/v1/'
    api_token = '9fb3515b37cd97c01905'
    headers = {'Content-Type': 'application/json',
               'API-KEY': '{0}'.format(api_token)}
    #print('heref',api_url_short,api_url_base+api_url_short)
    api_url = api_url_base+api_url_short
    return(api_url,headers)

def listconffunc():

    api_url,headers=connection('conferences')
    # print(api_url)
    response = requests.get(api_url, headers=headers)
    #print(response.status_code)

    #if response.status_code == 200:
     #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    elif response.status_code == 200:
        info = json.loads(response.content.decode('utf-8'))
        return info['conferences']#list(info['conferences'][0].values())[1]
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

    if info is not None:
        # print("Here's your info: ")
        #print(list(info['conferences'][1].values())[1])
        #print(len(info['conferences']))
        for j,details in enumerate(info['conferences']):
            #print('Conference number: '.format(j))
            for k, v in details.items():
                print('{0}:{1}'.format(k, v))
            print('yo',details.items())
        stuff_for_frontend = {
            'title': list(info['conferences'][0].values())[1],
        }
    else:
        print('[!] Request Failed')
        return None

def createconffunczoominstant(confnum,indiv):
    alphabet = string.ascii_letters + string.digits
    passwordzoom = ''.join(secrets.choice(alphabet) for ij in range(7))

    conftopass=CreateConf.objects.filter(id=confnum)[0]

    if indiv==0:
        title="Test room for " + conftopass.title
    elif indiv.startswith('0012'):
        title="Recording room for " +str(indiv[4:])
    else:
        title="One time test room for "+str(indiv)
        #print('indiv',indiv)

    start_time2=datetime.datetime.now(datetime.timezone.utc)

    start_time2_strz = start_time2.strftime("%Y-%m-%dT%H:%M:%SZ")

    #print('starttimezoom', start_time2, start_time2_strz, '2020-12-07T11:00:00Z')

    data = {"topic": title, "type": 2,
            "start_time": start_time2_strz, "duration": "40",
            "password": passwordzoom, "agenda": title, "timezone": "UTC",
            "settings": {"host_video": True, "participant_video": True,
                         "hd_video": True, "waiting_room": False, "join_before_host": True,
                         "mute_upon_entry": True, "watermark": False, "use_pmi": False,
                         "approval_type": 2, "audio": "both", "auto_recording": "none",
                         "meeting_authentification": True, "registrants_email_notification": False}}

    # data = {"title": createconff.title,
    #        "start_time": start_time2_str,
    #        "exit_url": "https://www.carbonfreeconf.com/exitpage",
    #        }

    data = json.dumps(data)

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}


    conn = http.client.HTTPSConnection("api.zoom.us")

    exit=0
    conn.request("GET", "/v2/users?page_size=300&status=active", headers=headers)
    resusers = conn.getresponse()
    datausers = resusers.read()
    #print('datausers',json.loads(datausers)['users'][0]['type'])
    #print('datausers',json.loads(datausers)['users'][1]['type'])
    nbhosts=json.loads(datausers)['total_records']
    #print('nbhosts',nbhosts)
    emailhosts = []
    for ij in range(nbhosts):
        if json.loads(datausers)['users'][ij]['type']==1:
            emailhosts.append(json.loads(datausers)['users'][ij]['email'])

    #could only use that if limited on API rates one day...
    #emailhosts=['quentin.kral@gmail.com','quenti@free.fr']
    #print('emailh',emailhosts)

    i=0
    host = ""
    while exit==0:

        conn.request("GET", "/v2/users/"+emailhosts[i]+"/meetings?page_size=300&type=live", headers=headers)

        resmeetings = conn.getresponse()
        datameetings = resmeetings.read()

        #print('datameetings',datameetings.decode("utf-8"))
        meet=json.loads(datameetings)
        if resmeetings.status==200:
            #print('i',i,emailhosts[i],meet["total_records"])

            if meet["total_records"]==0:
                host=emailhosts[i]
                exit=1
                #print('exit',i)
            if i+1 >= len(emailhosts) and exit == 0:
                exit=1
                host = ""
            i=i+1

    #for meetings
    #payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\":\"join_before_host\":\"boolean\"
    #payload = "{\"topic\":\"Test Meeting\",\"type\":2,\"start_time\":\"2020-12-07T11:00:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfghjk\",\"agenda\":\"Test Meeting\",\"settings\":{\"host_video\":\"true\",\"participant_video\":\"true\",\"hd_video\":\"true\",\"waiting_room\":\"false\",\"join_before_host\":\"true\",\"mute_upon_entry\":\"true\",\"watermark\":\"false\",\"use_pmi\":\"false\",\"approval_type\":\"2\",\"audio\":\"both\",\"auto_recording\":\"local\",\"auto_recording\":\"none\",\"meeting_authentification\":\"false\",\"registrants_email_notification\":\"false\"}}"

    if host:
        #conn.request("POST", "/v2/users/admin@carbonfreeconf.com/meetings", data, headers)
        conn.request("POST", "/v2/users/"+host+"/meetings", data, headers)

        #for webinars
        #payload = "{\"topic\":\"Test Webinar\",\"type\":5,\"start_time\":\"2020-12-06T15:25:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfgh\",\"agenda\":\"Test Webinar\",\"settings\":{\"host_video\":\"true\",\"panelists_video\":\"true\",\"practice_session\":\"true\",\"hd_video\":\"true\",\"approval_type\":2,\"audio\":\"both\",\"auto_recording\":\"none\",\"enforce_login\":\"false\",\"close_registration\":\"true\",\"show_share_button\":\"true\",\"allow_multiple_devices\":\"false\",\"registrants_email_notification\":\"false\"}}"
        #conn.request("POST", "/v2/users/admin@carbonfreeconf.com/webinars", payload, headers)

        res = conn.getresponse()
        #print('status',res.status)
        data2 = res.read()

        #print(data2.decode("utf-8"))

        if res.status == 201:
            info = json.loads(data2.decode('utf-8'))
            return info#['start_url']
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(res.status, data2))
            return None
    else:
        return None

def createconffunczoom(data):

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    conn = http.client.HTTPSConnection("api.zoom.us")

    #for meetings
    #payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\":\"join_before_host\":\"boolean\"
    #payload = "{\"topic\":\"Test Meeting\",\"type\":2,\"start_time\":\"2020-12-07T11:00:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfghjk\",\"agenda\":\"Test Meeting\",\"settings\":{\"host_video\":\"true\",\"participant_video\":\"true\",\"hd_video\":\"true\",\"waiting_room\":\"false\",\"join_before_host\":\"true\",\"mute_upon_entry\":\"true\",\"watermark\":\"false\",\"use_pmi\":\"false\",\"approval_type\":\"2\",\"audio\":\"both\",\"auto_recording\":\"local\",\"auto_recording\":\"none\",\"meeting_authentification\":\"false\",\"registrants_email_notification\":\"false\"}}"

    #conn.request("POST", "/v2/users/admin@carbonfreeconf.com/meetings", data, headers)
    conn.request("POST", "/v2/users/admin@carbonfreeconf.com/meetings", data, headers)


    #for webinars
    #payload = "{\"topic\":\"Test Webinar\",\"type\":5,\"start_time\":\"2020-12-06T15:25:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfgh\",\"agenda\":\"Test Webinar\",\"settings\":{\"host_video\":\"true\",\"panelists_video\":\"true\",\"practice_session\":\"true\",\"hd_video\":\"true\",\"approval_type\":2,\"audio\":\"both\",\"auto_recording\":\"none\",\"enforce_login\":\"false\",\"close_registration\":\"true\",\"show_share_button\":\"true\",\"allow_multiple_devices\":\"false\",\"registrants_email_notification\":\"false\"}}"
    #conn.request("POST", "/v2/users/admin@carbonfreeconf.com/webinars", payload, headers)

    res = conn.getresponse()
    #print('status',res.status)
    data2 = res.read()

    #print(data2.decode("utf-8"))

    if res.status == 201:
        info = json.loads(data2.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(res.status, data2))
        return None

def createconffunc(data):
    api_url, headers = connection('conferences')

    # api_url = '{0}channels'.format(api_url_base)

    #data = {"channel_id": "q425296", "title": "Conference title", "start_time": "2020-03-09 14:10"}

    #print(api_url)
    #print(data)
    #response = requests.post(api_url, headers=headers, json=data)
    response = requests.post(api_url, headers=headers, data=data)

    # response = requests.get(api_url, headers=headers)
    #print(response.status_code)
    #print('ina',response)
    #print('ina2',response['id'],response['channel_id'])

    #if response.status_code == 201:
     #   info = json.loads(response.content.decode('utf-8'))

      #  print(response)
       # print(info)
        #print(info['id'])
        #return info['id']
    # if response.status_code == 200:
    #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    #record channel_id and id
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        print(response.content)
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 201:
        info = json.loads(response.content.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

#inv=1 add
#inv=0 kick
def chatrock(conf,user,inv):
    with sessions.Session() as session2:
        # log-in

        try:
            rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                server_url='https://chat.carbonfreeconf.com', session=session2)
        except:
            #time.sleep(20)
            #rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                #server_url='https://chat.carbonfreeconf.com', session=session2)
            subject="Nooooooooo Rocket chat what????"
            message = "Oups <strong>Rocket chat</strong> fait de la merde!!!!"
            # message+="<img src='https://bucketeer-83011bf8-623d-4ad2-8e34-40829bae363d.s3.amazonaws.com/static/images/carbonfreeconf_logo_title.svg' width='200' height='60' alt='Make my own CarbonFreeConf workshop'>"

            emailto = []
            emailto.append("quentin.kral@gmail.com")
            emailto.append("carbonfreeconf@gmail.com")

            email = EmailMessage(
                subject,
                message,
                'CarbonFreeConf <communication@carbonfreeconf.com>',  # from
                emailto,  # to
                # getemails,  # bcc
                # reply_to=replylist,
                headers={'Message-From': 'www.carbonfreeconf.com'},
            )
            email.content_subtype = "html"

            #email.send(fail_silently=False)

        slugtitleconf = slugify(str('%s' % (conf.title)))
        #print('slug', slugtitleconf)
        list = rocket.groups_list_all().json()
        # print('l', list)
        # pprint(rocket.groups_info(room_name=slugtitleconf).json())
        contentroom = rocket.groups_info(room_name=slugtitleconf).json()
        #print('c', contentroom)
        if contentroom['success'] == True:
            keyroom = contentroom['group']['_id']

            contentuser = rocket.users_info(username=user.username).json()
            key = contentuser['user']['_id']
            # print('keyo',key,keyroom)

            if inv == 1:
                pprint(rocket.groups_invite(room_id=keyroom, user_id=key).json())
            if inv == 0:
                pprint(rocket.groups_kick(room_id=keyroom, user_id=key).json())

            slugtitleconfcafe = slugify(
                str('%s' % ('Coffee break for ' + conf.title)))

            contentroomcafe = rocket.groups_info(room_name=slugtitleconfcafe).json()
            if contentroomcafe['success']:
                #print('c', contentroomcafe)
                keyroomcafe = contentroomcafe['group']['_id']

                contentusercafe = rocket.users_info(username=user.username).json()
                keycafe = contentusercafe['user']['_id']
                # print('keyo',key,keyroom)

                if inv == 1:
                    pprint(rocket.groups_invite(room_id=keyroomcafe, user_id=keycafe).json())
                if inv == 0:
                    pprint(rocket.groups_kick(room_id=keyroomcafe, user_id=keycafe).json())

    return 0

def updateconffunczoom(data,idc,cb=None):

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    #r = requests.get('https://api.zoom.us/v2/users/', headers=headers)

    #print('fdsfdsf',r.text)

    #gangsta

    #print('idc',idc)
    conn = http.client.HTTPSConnection("api.zoom.us")

    conn.request("GET", "/v2/users?page_size=300&status=active", headers=headers)
    resusers = conn.getresponse()
    datausers = resusers.read()
    #print('datausers', json.loads(datausers)['users'][0]['type'])
    #print('datausers', json.loads(datausers)['users'][1]['type'])
    nbhosts = json.loads(datausers)['total_records']
    #print('nbhosts', nbhosts)
    emailhosts = []
    for ij in range(nbhosts):
        if json.loads(datausers)['users'][ij]['type'] == 2:
            emailhosts.append(json.loads(datausers)['users'][ij]['email'])

    print('emailh',emailhosts)
    #conn.request("GET", "/v2/users?page_size=30&status=active", headers=headers)

    #res = conn.getresponse()
    #data = res.read()

    #print('sd'+data.decode("utf-8"))

    #for meetings
    #payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\":\"join_before_host\":\"boolean\"
    #payload = "{\"topic\":\"Test Meeting\",\"type\":2,\"start_time\":\"2020-12-07T11:00:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfghjk\",\"agenda\":\"Test Meeting\",\"settings\":{\"host_video\":\"true\",\"participant_video\":\"true\",\"hd_video\":\"true\",\"waiting_room\":\"false\",\"join_before_host\":\"true\",\"mute_upon_entry\":\"true\",\"watermark\":\"false\",\"use_pmi\":\"false\",\"approval_type\":\"2\",\"audio\":\"both\",\"auto_recording\":\"local\",\"auto_recording\":\"none\",\"meeting_authentification\":\"false\",\"registrants_email_notification\":\"false\"}}"

    #add schedule_for with email or userID to data to put an available user
    #check idc de visio and what time and whether users still available
    if cb == True:
        print('cb')
        visio=CreateVisio.objects.filter(idconfcb=idc).exclude(testroom=True)[0]
    else:
        print('nocb')
        visio = CreateVisio.objects.filter(idconf=idc).exclude(testroom=True)[0]

    starttime = visio.date
    endtime = visio.date + timedelta(minutes=visio.duration)

    #print('start',starttime,endtime,visio)

    #get all visio at the same time
    endmax=visio.date + timedelta(minutes=10*60)
    startmin=visio.date - timedelta(minutes=10*60)
    #print('endmax',endmax)
    if cb == True and visio.conference.coffeebreak:
        print('okp')
        visiosametime=CreateVisio.objects.filter(Q(date__gte=startmin,date__lte=endmax,conference__status=1)|Q(idconfcb=idc)).exclude(testroom=True)
    else:
        visiosametime=CreateVisio.objects.filter(date__gte=startmin,date__lte=endmax,conference__status=1).exclude(testroom=True).exclude(id=visio.id)

    zoomuser=[]
    for v in visiosametime:
        #print('v',v)
        endtime2 = v.date + timedelta(minutes=v.duration)
        #print('endtime2',endtime2,v.date)
        if (v.date>=starttime and v.date<=endtime) or (v.date<=endtime2 and endtime2<=endtime) or (v.date<=starttime and endtime2>=endtime) or (v.date>=starttime and endtime2<=endtime):
            #don't use this zoom user
            zoomuser.append(v.zoomcreator)
            if v.conference.coffeebreak:
                zoomuser.append(v.zoomcreatorcb)

            print('vsame',v,v.zoomcreator)
            print('v.date,starttime,endtime,endtime2',v.date,starttime,endtime,endtime2)
            #8h 10h

            #treat that 7h 9h - 9h 11h - 7h 11h - 8h30 9h30

    #print('zoomuser',zoomuser)

    if visio.conference.size == '<10':
        size=10.
    elif visio.conference.size == '10-50':
        size=50.
    elif visio.conference.size == '50-100':
        size=100.
    elif visio.conference.size == '100-300':
        size=300.
    elif visio.conference.size == '300-500':
        size=500.
    elif visio.conference.size == '500-1000':
        size=1000.

    exit=0
    j=0
    goodemail=''
    if emailhosts:
        while exit==0:
            if emailhosts[j] not in zoomuser:
                print('notin',emailhosts[j],visio.id)
                conn.request("GET", "/v2/users/"+emailhosts[j]+"/settings", headers=headers)
                capacity = conn.getresponse()
                datausercapacity = capacity.read()
                #print('datauserscap', json.loads(datausercapacity))
                print('datauserscap2', json.loads(datausercapacity)['feature']['meeting_capacity'])
                usercapacity=json.loads(datausercapacity)['feature']['meeting_capacity']
                if size <= usercapacity:#should find a trick to not use too large a licence though 100-300-500-1000 but still use it if not used
                #if 1==1:
                    goodemail=emailhosts[j]
                    #CreateVisio.objects.filter(id=visio.id).update(zoomcreator=goodemail)

                    #p2 = CreateVisio.objects.get(id=visio.id)
                    #print('p2',p2.date,p2.conference.title)
                    if cb == True:
                        visio.zoomcreatorcb=goodemail
                    else:
                        visio.zoomcreator=goodemail
                    visio.save()
                    print('saved',j,goodemail)
                    exit=1
                    #print('saved2')
                #else:
                #    print('usercapacity not good',size,usercapacity)

            j=j+1

            if j>=len(emailhosts) and exit==0:
                exit=1


    if goodemail:
        dataup=json.loads(data)
        dataup.update({'schedule_for': goodemail})
        data=json.dumps(dataup)
        #print('dataup',data)

    else:
        #print('contact admin, not enough licences')
        subject = "Nooooooooo not enough licenses"
        message = "Oups <strong>not enough licenses</strong> for visio = "+idc+", title="+visio.conference.title+" size:"+str(size)+" !!!!"
        # message+="<img src='https://bucketeer-83011bf8-623d-4ad2-8e34-40829bae363d.s3.amazonaws.com/static/images/carbonfreeconf_logo_title.svg' width='200' height='60' alt='Make my own CarbonFreeConf workshop'>"

        emailto = []
        #emailto.append("quentin.kral@gmail.com")
        emailto.append("carbonfreeconf@gmail.com")

        email = EmailMessage(
            subject,
            message,
            'CarbonFreeConf <communication@carbonfreeconf.com>',  # from
            emailto,  # to
            # getemails,  # bcc
            # reply_to=replylist,
            headers={'Message-From': 'www.carbonfreeconf.com'},
        )
        email.content_subtype = "html"

        email.send(fail_silently=False)

    conn.request("PATCH", "/v2/meetings/"+idc, data, headers)

    #for webinars
    #payload = "{\"topic\":\"Test Webinar\",\"type\":5,\"start_time\":\"2020-12-06T15:25:00Z\",\"duration\":\"600\",\"timezone\":\"Europe/London\",\"password\":\"avfhfgh\",\"agenda\":\"Test Webinar\",\"settings\":{\"host_video\":\"true\",\"panelists_video\":\"true\",\"practice_session\":\"true\",\"hd_video\":\"true\",\"approval_type\":2,\"audio\":\"both\",\"auto_recording\":\"none\",\"enforce_login\":\"false\",\"close_registration\":\"true\",\"show_share_button\":\"true\",\"allow_multiple_devices\":\"false\",\"registrants_email_notification\":\"false\"}}"
    #conn.request("POST", "/v2/users/admin@carbonfreeconf.com/webinars", payload, headers)

    res = conn.getresponse()
    #print('status',res.status)
    data2f = res.read()

    print(data2f.decode("utf-8"))

    if res.status == 204:
        #info = json.loads(data2.decode('utf-8'))
        return 0
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(res.status))
        return None

def getchannelid():

    #ca ne marche qu'en Oauth pas en jwt, il faut attendre un peu c'est prevu d'etre ajouté à l'API
    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}


    conn.request("GET", "/v2/chat/users/"+"admin@carbonfreeconf.com"+"channels?page_size=10", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"),res.status)
    #info = json.loads(data.decode('utf-8'))

    #print('channels')
    return 0

def updateconffunc(data,idc):
    link='conferences/'+idc
    api_url, headers = connection(link)

    # api_url = '{0}channels'.format(api_url_base)

    #data = {"channel_id": "q425296", "title": "Conference title", "start_time": "2020-03-09 14:10"}

    #print(api_url)
    #print(data)
    #response = requests.post(api_url, headers=headers, json=data)
    response = requests.put(api_url, headers=headers, data=data)

    # response = requests.get(api_url, headers=headers)
    #print(response.status_code)
    #print('ina',response)
    #print('ina2',response['id'],response['channel_id'])

    #if response.status_code == 201:
     #   info = json.loads(response.content.decode('utf-8'))

      #  print(response)
       # print(info)
        #print(info['id'])
        #return info['id']
    # if response.status_code == 200:
    #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    #record channel_id and id
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        print(response.content)
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 200:
        info = json.loads(response.content.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

#WHOTO = (
 #       (0, "Super Users"),
  #      (1, "All"),
   #     (2, "Participants with accepted talks/review/discussion"),
    #    (3, "Participants presenting posters"),
     #   (4, "Participants with no talks/posters accepted who registered"),
      #  (5, "SOC"),
       # (6, "LOC"),
        #(7, "Participants you invited but did not register yet"),
        #(8, "Moderators"),
        #(9, "Those that are only attending but not presenting"),
        #(10, "Participants with invited talks"),
        #(11, "Participants with discussions"),
        #(12, "Participants with reviews"),
    #)

   #STATUS = (
       # (0, "Submitted"),
      # (1, "Accepted"),
     #   (2, "Other"),
    #)


    #TYPE = (
        #(6, "Talk"),
        #(1, "Invited Talk"),
        #(2, "Discussion"),
       # (3, "Review"),
      #  (4, "Poster"),
     #   (5, "Attendance only"),
    #)

#    ROLE = (
 #       (0, "Presenter"),
  #      (1, "Moderator"),
   #     (2, "Attendee"),
    #    (3, "Superuser")
    #)

#SOCLOC = (
 #       (0, "Not a SOC or LOC member"),
  #      (1, "SOC"),
   #     (2, "LOC"),
    #)


def delslidesfunc(data,idc):
    # https://www.bigmarker.com/api/v1/conferences/{:conference_id}/upload_file/delete_file/{:file_id}

    link='conferences/'+idc+'/delete_file/'+data
    api_url, headers = connection(link)

    # api_url = '{0}channels'.format(api_url_base)

    #data = {"channel_id": "q425296", "title": "Conference title", "start_time": "2020-03-09 14:10"}

    #print(api_url)
    #print(data)
    #response = requests.post(api_url, headers=headers, json=data)
    response = requests.put(api_url, headers=headers)

    # response = requests.get(api_url, headers=headers)
    #print(response.status_code)
    #print('ina',response)
    #print('ina2',response['id'],response['channel_id'])

    #if response.status_code == 201:
     #   info = json.loads(response.content.decode('utf-8'))

      #  print(response)
       # print(info)
        #print(info['id'])
        #return info['id']
    # if response.status_code == 200:
    #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    #record channel_id and id
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        print(response.content)
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 200:
        info = json.loads(response.content.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

def addslidesfunc(data,idc):
    #https: // www.bigmarker.com / api / v1 / conferences / {: conference_id} / upload_file

    link='conferences/'+idc+'/upload_file'
    api_url, headers = connection(link)

    # api_url = '{0}channels'.format(api_url_base)

    #data = {"channel_id": "q425296", "title": "Conference title", "start_time": "2020-03-09 14:10"}

    #print(api_url)
    #print(data)
    #response = requests.post(api_url, headers=headers, json=data)
    response = requests.put(api_url, headers=headers, data=data)

    # response = requests.get(api_url, headers=headers)
    #print(response.status_code)
    #print('ina',response)
    #print('ina2',response['id'],response['channel_id'])

    #if response.status_code == 201:
     #   info = json.loads(response.content.decode('utf-8'))

      #  print(response)
       # print(info)
        #print(info['id'])
        #return info['id']
    # if response.status_code == 200:
    #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    #record channel_id and id
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        print(response.content)
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 200:
        info = json.loads(response.content.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

def delconffunc(idc):
    # https://www.bigmarker.com/api/v1/conferences/{:conference_id}

    link='conferences/'+idc
    api_url, headers = connection(link)

    # api_url = '{0}channels'.format(api_url_base)

    #data = {"channel_id": "q425296", "title": "Conference title", "start_time": "2020-03-09 14:10"}

    #print(api_url)
    #response = requests.post(api_url, headers=headers, json=data)
    response = requests.delete(api_url, headers=headers)

    # response = requests.get(api_url, headers=headers)
    #print(response.status_code)
    #print('ina',response)
    #print('ina2',response['id'],response['channel_id'])

    #if response.status_code == 201:
     #   info = json.loads(response.content.decode('utf-8'))

      #  print(response)
       # print(info)
        #print(info['id'])
        #return info['id']
    # if response.status_code == 200:
    #   info = json.loads(response.content.decode('utf-8'))
    # else:
    #   return None

    #record channel_id and id
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        print(response.content)
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        print(response.content)
        return None
    elif response.status_code == 200:
        info = json.loads(response.content.decode('utf-8'))
        return info
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

def delconffunczoom(idc):
    # https://www.bigmarker.com/api/v1/conferences/{:conference_id}

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    conn.request("DELETE", "/v2/meetings/"+str(idc), headers=headers)

    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"),'delete',idc,res.status)

    if res.status == 204:
        #info = json.loads(data.decode('utf-8'))
        return 'ok'
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(res.status, data))
        return None


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

def startapi():

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=False,wait_on_rate_limit_notify=False)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api


def getemails(confnum,whoto,mast):#mast=1 si masterconf
    conftopass = CreateConf.objects.filter(id=confnum)[0]
    #conftopass = CreateConf.objects.filter(id=confnum)[0]
    if mast==1:
        confsid = CreateConf.objects.filter(masterconfpass=conftopass.masterconfpass, acceptconf=True).values_list('id',
                                                                                                               flat=True)

    #print('z',whoto,type(whoto),whoto.replace('[','').replace(']','').replace("'","").replace(" ","").split(','))
    whoto=[int(x) for x in whoto.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')]
    #print('z',whoto,type(whoto))

    emaillist=[]
    personlist=[]

    for i in range(len(whoto)):
        #print('whotooo',i,whoto[i])
        if whoto[i]==0:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,role=3)
            else:
                people=RegisterConf.objects.filter(conference=conftopass,role=3)
            #print('mez',people)

            if people:
                for peop in people:
                        emaillist.append(peop.user.email)
                        personlist.append(peop.user.first_name+' '+peop.user.last_name)

        elif whoto[i]==1:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True)
            else:
                people = RegisterConf.objects.filter(conference=conftopass)
            #print('me',people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

            if mast==1:
                peopleinv = People.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True)
            else:
                peopleinv = People.objects.filter(conference=conftopass)
            for peopinv in peopleinv:
                if not peopinv.email in emaillist:
                    emaillist.append(peopinv.email)
                    personlist.append(peopinv.firstname + ' ' + peopinv.lastname)

        elif whoto[i] == 2:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,status=1,type__in=[1,2,3,6])
            else:
                people = RegisterConf.objects.filter(conference=conftopass,status=1,type__in=[1,2,3,6])
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)
            #if mast==1:
            #    peopleinv = People.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True)
            #else:
            #    peopleinv = People.objects.filter(conference=conftopass)
            #for peopinv in peopleinv:
            #    people = RegisterConf.objects.filter(conference=conftopass, user__email=peopinv.email)
            #    if not people:
            #        emaillist.append(peopinv.email)
            #        personlist.append(peopinv.firstname + ' ' + peopinv.lastname)


        elif whoto[i] == 3:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,status=1,type=4)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,status=1,type=4)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 4:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,status=0)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,status=0)
            if people:
                for peop in people:
                    if not RegisterConf.objects.filter(conference=conftopass,user=peop.user,status=1):
                        emaillist.append(peop.user.email)
                        personlist.append(peop.user.first_name+' '+peop.user.last_name)


        elif whoto[i] == 5:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,socloc=1)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,socloc=1)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 6:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,socloc=2)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,socloc=2)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 7:#tbb
            if mast==1:
                peopleinv = People.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True)
            else:
                peopleinv = People.objects.filter(conference=conftopass)
            for peopinv in peopleinv:
                people = RegisterConf.objects.filter(conference=conftopass,user__email=peopinv.email)
                if not people:
                    emaillist.append(peopinv.email)
                    personlist.append(peopinv.firstname + ' ' + peopinv.lastname)


        elif whoto[i] == 8:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,role=1)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,role=1)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 9:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,type=5)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,type=5)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 10:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,type=1)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,type=1)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 11:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,type=2)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,type=2)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 12:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,type=3)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,type=3)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 13:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,haspaid=True)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,haspaid=True)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 14:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,haspaid=False)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,haspaid=False)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        elif whoto[i] == 15:
            if mast==1:
                people=RegisterConf.objects.filter(conference__masterconfpass=conftopass.masterconfpass,conference__acceptconf=True,free=True)
            else:
                people = RegisterConf.objects.filter(conference=conftopass,free=True)
            #print('me', people)
            if people:
                for peop in people:
                    emaillist.append(peop.user.email)
                    personlist.append(peop.user.first_name + ' ' + peop.user.last_name)

        else:
            return None

    #print('emailist', emaillist)
    #print('personlist', personlist)


    #remove duplicates
    if emaillist:
        emaillist = list(dict.fromkeys(emaillist))#list(set(emaillist))
        #print('emailist', emaillist)

    else:
        return None

    if personlist:
        personlist = list(dict.fromkeys(personlist))#list(set(personlist))
        #print('personlist', personlist)

    else:
        return None

    return [emaillist,personlist]

def price(confnum,help=None):
    #print('price')
    #Regler combien on paye en fonction de nombre de participants, video archive, YouTube,proceedings,
    #Mettre 40% en plus pour defrayment de carbonfreeconf.
    #Regler combien on paye en fonction de nombre de participants (size VERYSMALL,...), video archive (recording) whirecording(ANY,MEMB,PRIV), YouTube(youtuberecording),proceedings (proceedin),

        #(VERYSMALL, "<10 people"),
        #(SMALL, "10-50 people"),
        #(NORMAL, "50-100 people"),
        #(LARGE, "100-200 people"),
        #(VERYLARGE, "200-500 people"),
        #(VERYVERYLARGE, "500-1000 people"),

    conf=CreateConf.objects.get(id=confnum)
    #print('status',conf.size,conf.recording,conf.whorecording,conf.youtuberecording,conf.proceedin)
    #print('duration', abs(conf.end_date-conf.start_date).days+1)#            getnumberofdays=abs(end-start).days+1
    duration=abs(conf.end_date-conf.start_date).days+1
    climework1euro=1.#kg CO2 stocked underground
    peerreviewedShehabi=0.04/2.#0.114/4.#kg/hour Shehabi+14 see also https://www.carbonbrief.org/factcheck-what-is-the-carbon-footprint-of-streaming-video-on-netflix
    #divide by 4 because bigmarker is more like 1Mbps and Netflix averages at 4Mbps
    #8g/h in France but global mix gives
    #peerreviewedShehabi = peerreviewedShehabi*2.#to account for Shehabi and AIE and shift project larger values
    #cost by hour per person: peerreviewedShehabi/climework1euro=0.018euro
    costeurocarbonperpersonperhour = peerreviewedShehabi / climework1euro
    costeurocarbonperpersonperday = costeurocarbonperpersonperhour * 8.
    #duration=3.

    for i in range(6):
        if i==0:
            price = 10 * costeurocarbonperpersonperday * duration
        elif i==1:
            price = 50 * costeurocarbonperpersonperday * duration
        elif i==2:
            price = 100 * costeurocarbonperpersonperday * duration
        elif i==3:
            price = 300 * costeurocarbonperpersonperday * duration
        elif i==4:
            price = 500 * costeurocarbonperpersonperday * duration
        elif i==5:
            price = 1000 * costeurocarbonperpersonperday * duration

        pricerec = 0.
        if 1==1:
            if 1==1:#conf.whorecording == "Everyone":
                pricerec = costeurocarbonperpersonperhour / 2. * 1000  # in 3 yrs we estimate 1k views and mean video time = 1hr-->1000 hr
            elif 1==0:#conf.whorecording == "Only conference participants":
                pricerec = price / duration / 8. * 5. / 2. / 3.  # one third of particpants will look at the video
            else:  # private link
                pricerec = price / duration / 8. * 5. / 2. / 8.
            if 1==1:#conf.youtuberecording:
                pricerec = pricerec * 2.

        priceproc = 0.
        if 1==1:#conf.proceedin:
            priceproc = 0.12 * price  # add 12% for now

        offseteuro = price + pricerec + priceproc

        if price / costeurocarbonperpersonperday / duration < 300:
            prepeuro = 2.56 * offseteuro  # max(0.9 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.4))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)
        else:
            prepeuro = 1.85 * offseteuro  # max(0.7 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.475))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)

        #print('pricing',i,price/(costeurocarbonperpersonperday * duration),offseteuro,prepeuro,price,pricerec,priceproc)

    if conf.size == '<10':
        size=10.
        price=10*costeurocarbonperpersonperday*duration
    elif conf.size == '10-50':
        size=50.
        price=50*costeurocarbonperpersonperday*duration
    elif conf.size == '50-100':
        size=100.
        price=100*costeurocarbonperpersonperday*duration
    elif conf.size == '100-300':
        size=300.
        price=300*costeurocarbonperpersonperday*duration
    elif conf.size == '300-500':
        size=500.
        price=500*costeurocarbonperpersonperday*duration
    elif conf.size == '500-1000':
        size=1000.
        price=1000*costeurocarbonperpersonperday*duration

    pricerec = 0.
    if conf.recording:
        if conf.whorecording=="Everyone":
            pricerec=costeurocarbonperpersonperhour/2.*1000#in 3 yrs we estimate 1k views and mean video time = 5hr-->5000 hr
        elif conf.whorecording=="Only conference participants":
            pricerec=price/duration/8.*5./2./3.#one third of particpants will look at the video
        else:#private link
            pricerec=price/duration/8.*5./2./8.
        if conf.youtuberecording:
            pricerec=pricerec*2.

    priceproc = 0.
    if conf.proceedin:
        priceproc=0.12*price#add 12% for now

    offseteuro=price+pricerec+priceproc

    if price / costeurocarbonperpersonperday / duration < 300:
        prepeuro = 2.56 * offseteuro  # max(0.9 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.4))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)
    else:
        prepeuro = 1.85 * offseteuro  # max(0.7 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.475))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)

    #print('help',help)
    if help!=1:
        if not conf.masterconf and not conf.daughterconf:
            if duration<2 and size<51:
                prepeuro=0.

    if duration==1:
        prepeuro=prepeuro/2.

    return [prepeuro,offseteuro]

def pricebis(duration,size,rec,youtube,who,proc):
    #print('pricebis',duration,size)

        #(VERYSMALL, "<10 people"),
        #(SMALL, "10-50 people"),
        #(NORMAL, "50-100 people"),
        #(LARGE, "100-200 people"),
        #(VERYLARGE, "200-500 people"),
        #(VERYVERYLARGE, "500-1000 people"),


    climework1euro=1.#kg CO2 stocked underground/euro
    peerreviewedShehabi=0.04/2#0.114/4.#kg/hour Shehabi+14 see also https://www.carbonbrief.org/factcheck-what-is-the-carbon-footprint-of-streaming-video-on-netflix
    #divide by 4 because bigmarker is more like 4Mbps and Netflix averages at 4Mbps
    #8g/h in France but global mix gives
    #peerreviewedShehabi = peerreviewedShehabi#to account for Shehabi and AIE and shift project larger values
    #cost by hour per person: peerreviewedShehabi/climework1euro=0.018euro
    costeurocarbonperpersonperhour=peerreviewedShehabi/climework1euro
    costeurocarbonperpersonperday=costeurocarbonperpersonperhour*8.
    #duration=3.

    price = size * costeurocarbonperpersonperday * duration

    pricerec = 0.
    #print('who',who)
    if rec:
        if who == "Everyone":#conf.whorecording == "Everyone":
            pricerec = costeurocarbonperpersonperhour / 2. * 1000  # in 3 yrs we estimate 1k views and mean video time = 1hr-->1000 hr
        elif who == "participants":#conf.whorecording == "Only conference participants":
            pricerec = price / duration / 8. * 5. / 2. / 3.  # one third of participants will look at the video
        else:  # private link
            pricerec = price / duration / 8. * 5. / 2. / 8.
        if youtube:#conf.youtuberecording:
            pricerec = pricerec * 2.

    #print('pricerec',pricerec)

    priceproc = 0.
    if proc:#conf.proceedin:
        priceproc = 0.12 * price  # add 12% for now

    offseteuro = price + pricerec + priceproc

    #print('price / costeurocarbonperpersonperday / duration',7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.4))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05))
    if price / costeurocarbonperpersonperday / duration < 300:
        prepeuro = 2.56 * offseteuro#max(0.9 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.4))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)
    else:
        prepeuro = 1.85 * offseteuro#max(0.7 * offseteuro, 7. * (5.*price / costeurocarbonperpersonperday / duration)**(0.475))*(duration/5.)**(0.3)*((60.+pricerec+priceproc)/15.)**(0.05)

    if duration<2 and size<51:
        prepeuro=0.
        #print('pricing',i,price/(costeurocarbonperpersonperday * duration),offseteuro,prepeuro,price,pricerec,priceproc)

    if duration==1:
        prepeuro=prepeuro/2.

    return [prepeuro,offseteuro]


def delete_by_ids(index, ids):
    if not 'ON_HEROKU' in os.environ:
        url = urlparse(os.environ.get('SEARCHBOX_URL'))  # celui la en local
        connections.create_connection()  # celui la en local
    else:
        url = getattr(settings, "SEARCHBOX_URL", None)  # celui lasur heroku
        connections.create_connection(hosts=[os.environ.get('SEARCHBOX_URL')], timeout=20)  # celui la sur heroku
        #print('heroku')

    client = Elasticsearch()

    #for i in range(0,200):
     #   s2 = Search(index='conf-index').query('match', _id=i)
     #   res = s2.delete()#_by_query(index=index, body=query)
     #   s3 = Search(index='post-index').query('match', _id=i)
     #   res = s3.delete()#_by_query(index=index, body=query)


    s2 = Search(index='conf-index').query('match',_id=ids)
    #s2 = Search(index='conf-index')
    #FooDocument.update(obj, action="delete")

    #query = {"query": {"terms": {"_id": ids}}}
    res = s2.delete()#_by_query(index=index, body=query)
    #print('resssssssssssssssssssss',res)
    return 0

#privacy='nobody'
def uploadvidtovimeo(urlvideo,name,descr,privacy):

    site = urllib.request.urlopen(urlvideo)
    # meta = site.info()
    file_size = int(site.getheader('Content-Length'))

    # vidsize=meta.getheaders("Content-Length")
    # charset = meta.headers.get_content_charset()
    #print('filesize', file_size)

    # WHO_CHOICES = (
    #    (ANY, "Everyone"),
    #    (MEMB, "Only conference participants"),
    #    (PRIV, "Only through a private link"),
    # )

    # whorecording
    if privacy=="Everyone":
        privacyvim="anybody"
    elif privacy=="Only conference participants":
        privacyvim="nobody"
    else:
        privacyvim="nobody"

    url = 'https://api.vimeo.com/me/videos'
    # headers = {'Authorization': 'bearer %s' % settings.SECRETVIM, 'Content-Type': 'application/json','Accept': 'application/vnd.vimeo.*+json;version=3.4'}
    headers = {'Authorization': 'bearer %s' % settings.SECRETVIM, 'Content-Type': 'application/json',
               'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

    data = {'upload': {'approach': 'tus', 'size': file_size}, 'name': name, 'description': descr,
            'privacy': {'view': privacyvim, 'embed': 'public'}}

    r = requests.post(url, headers=headers, data=json.dumps(data))
    #print('r', r)
    #print('tt', json.loads(r.content.decode('utf-8')))

    if r.status_code == 200:
        #print('ro', r)

        uri = r.json()['uri']  # link to final video
        upload_link = r.json()['upload']['upload_link']
        approach = r.json()['upload']['approach']  # should be tus

        #print('r2', uri, upload_link, approach)

        if approach == 'tus':
            # first attempt to upload video

            headers = {'Tus-Resumable': '1.0.0', 'Upload-Offset': '0',
                       'Content-Type': 'application/offset+octet-stream',
                       'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

            # video_rb = video.open('rb')
            #videolink = 'https://d14c1kqvi6lpt9.cloudfront.net/03bdcde6e854-1591281300/bigmarker-recording.mp4'
            #recid=4c0342c6d4a6
            # video_rb = videolink.open('rb')

            #vid = urllib.request.urlopen(videolink)
            # fhand = open('cover3.jpg', 'wb')
            size = 0
            CHUNK = 1024 * 1024 * 2 #2Mb
            while True:
                info = site.read(CHUNK)
                if len(info) < 1: break
                size = size + len(info)
                r = requests.patch(upload_link, info, headers=headers)
                #print('rdf', size, r)
                headers = {'Tus-Resumable': '1.0.0', 'Upload-Offset': str(size),
                           'Content-Type': 'application/offset+octet-stream',
                           'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

            #print(size, 'video uploaded.')
            # fhand.close()

            # r = requests.patch(upload_link, video_rb, headers=headers)
            #r = requests.patch(upload_link, urlvideolink, headers=headers)
            #print('r3', r)
            #pprint(r)
            # Second attempt to upload video

            # Verify upload is complete

            headers = {'Tus-Resumable': '1.0.0', 'Accept': 'application/vnd.vimeo.*+json;version=3.4'}
            r = requests.head(upload_link, headers=headers)

            #print('r4', r)
            #pprint(r)

            #print('all good')

            return uri

        else:
            print('not tus???')

            return 0
    else:
        print('Problem with vimeo')

        return 0

def generateSignature(data):
    ts = int(round(time.time() * 1000)) - 30000;
    msg = data['apiKey'] + str(data['meetingNumber']) + str(ts) + str(data['role']);
    message = base64.b64encode(bytes(msg, 'utf-8'));
    # message = message.decode("utf-8");
    secret = bytes(data['apiSecret'], 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256);
    hash =  base64.b64encode(hash.digest());
    hash = hash.decode("utf-8");
    tmpString = "%s.%s.%s.%s.%s" % (data['apiKey'], str(data['meetingNumber']), str(ts), str(data['role']), hash);
    signature = base64.b64encode(bytes(tmpString, "utf-8"));
    signature = signature.decode("utf-8");
    print('signarole',str(data['role']))
    return signature.rstrip("=");


# create a function to generate a token using the pyjwt library
def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing API Key & expiration time
        {"iss": settings.APIKEYZOOM, "exp": time.time() + 5000},
        # Secret used to generate token signature
        settings.APISECRETZOOM,
        # Specify the hashing alg
        algorithm='HS256'
        # Convert token to utf-8
    ).decode('utf-8')

    return token

#def lt(strd):
#    data=strd.encode("latin-1","ignore")
#    return data
#    return strd.encode('utf-8').encode('latin-1', 'ignore')#.encode('iso-8859-1')


def createabstractbooklet(request,confnum):
    from fpdf import FPDF, HTMLMixin

    class MyFPDF(FPDF, HTMLMixin):

        #def header(self):
            # Logo
            #self.image('logo_pb.png', 10, 8, 33)
            # Arial bold 15
            #self.set_font('Arial', 'B', 7)
            # Move to the right
            #self.cell(80)
            # Title
            #self.cell(30, 10, 'Carbon-neutral conference powered by carbonfreeconf.com', 0, 0, 'C')
            # Line break
            #self.ln(20)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    tzloc = request.session.get('django_timezone', '')  # request.session['django_timezone']
    if tzloc:
        local = pytz.timezone(tzloc)
    else:
        local = pytz.timezone('UTC')

    now = datetime.datetime.utcnow()  # .replace(tzinfo=utc)
    shift = now.astimezone(local).replace(tzinfo=None) - now.replace(tzinfo=None)
    #print('shift',shift)

    conftopass2 = CreateConf.objects.filter(id=confnum)

    if conftopass2[0].masterconf:
        conftopass3=CreateConf.objects.filter(masterconfidfordaughter=confnum,acceptconf=True).order_by('title')
        from itertools import chain
        conftopass = list(chain(conftopass2,conftopass3))        #conftopass =conftopass2 | conftopass3
        #print('getall',conftopass)

    else:
        conftopass = conftopass2

    #print('conftopass',conftopass2)

    #print('confx',confnum)
    #from fpdf import FPDF, pdf.write_html(html)



    pdf = MyFPDF('P', 'mm', 'A4')

    #pdf = FPDF()
    pdf.add_page()
    #pdf.set_global('SYSTEM_TTFONTS', "my_app/font/")
    #FPDF_FONTPATH = 'my_app/font/'
    #pdf.add_font('Comic Sans', '', '/app/my_app/font/Comic_Sans_MS.ttf', uni=True)

    #print('path',os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed.ttf'))
    pdf.add_font('DejaVu', '', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed-Bold.ttf'), uni=True)
    pdf.add_font('DejaVu', 'I', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed-Oblique.ttf'), uni=True)

    #pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    #pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    #pdf.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
    #pdf.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)

    pdf.set_font('DejaVu', '', 14)

    #pdf.set_fill_color(32.0, 47.0, 250.0)  # color for outer rectangle
    #pdf.rect(5.0, 5.0, 200.0, 287.0, 'DF')
    #pdf.set_fill_color(255, 255, 255)  # color for inner rectangle
    #pdf.rect(8.0, 8.0, 194.0, 282.0, 'FD')

    #header
    # Set up a logo
    #pdf.image('fg', 10, 8, 33)
    pdf.set_font('DejaVu', 'B', 20)

    # Add an address
    #pdf.cell(100)

    pdf.multi_cell(0, 7, "Abstract book for the conference: "+conftopass2[0].title, 0, 'C')

    #pdf.cell(100)
    #pdf.cell(0, 5, '123 American Way', ln=1)
    #pdf.cell(100)
    #pdf.cell(0, 5, 'Any Town, USA', ln=1)

    if conftopass2[0].room_logo:
        if not conftopass2[0].room_logo.url.endswith('.jpg') and not conftopass2[0].room_logo.url.endswith('.jpeg'):
            pdf.ln(25)
            pdf.set_xy(80., 30.0)
            pdf.image(conftopass2[0].room_logo.url, link='', type='',w=60)

    # Line break
    pdf.ln(20)

    #pdf.line(10, 10, 10, 100)
    #pdf.set_line_width(1)
    #pdf.set_draw_color(255, 0, 0)
    #pdf.line(20, 20, 100, 20)

    #pdf.set_font('Times', 'B', 15)
    #pdf.cell(w=210, h=9, txt=title, border=0, ln=1, align='C', fill=0)
    #pdf.set_font('Times', 'B', 15)
    #pdf.cell(w=0, h=6, txt=heading, border=0, ln=1, align='L', fill=0)
    #pdf.set_font('Times', '', 12)
    #pdf.multi_cell(w=0, h=5, txt=text)
    #response.headers['Content-Type'] = 'application/pdf'
    #return pdf.output(dest='S')
    #from django.utils.safestring import SafeString



    for ic in range(len(conftopass)):
        if len(conftopass)>1:
            pdf.ln(10)
            pdf.set_font('DejaVu', 'B', 18)
            if ic==0:
                pdf.multi_cell(h=10, w=0, txt="Plenary session: "+conftopass[ic].title)
            else:
                pdf.multi_cell(h=10, w=0, txt="Session "+str(ic)+") "+conftopass[ic].title)
            pdf.ln(10)

        pdf.set_font('DejaVu', 'B', 15)
        if len(conftopass)>1:
            pdf.multi_cell(h=10, w=0, txt="Session Abstract")
        else:
            pdf.multi_cell(h=10, w=0, txt="Conference Abstract")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(h=10, w=0, txt=conftopass[ic].abstract)
        pdf.ln(20)

        talks = RegisterConf.objects.filter(conference=conftopass[ic], status=1, type__in=[1, 2, 3, 6]).order_by(
            'user__last_name')
        talksetal = RegisterConf.objects.filter(conference=conftopass[ic], status=1).order_by('user__last_name')

        schedule = Schedule.objects.filter(conference=conftopass[ic]).order_by('start_date')

        #print('talks', talks)

        uniqueusers = [talksetal.filter(user=item['user']).first() for item in
                       talksetal.values('user').distinct()]

        posters = RegisterConf.objects.filter(conference=conftopass[ic], status=1, type=4).order_by('user__last_name')

        soc = RegisterConf.objects.filter(conference=conftopass[ic], socloc=1).order_by('user__last_name')
        socu = [soc.filter(user=item['user']).first() for item in
                soc.values('user').distinct()]
        loc = RegisterConf.objects.filter(conference=conftopass[ic], socloc=2).order_by('user__last_name')
        locu = [loc.filter(user=item['user']).first() for item in
                loc.values('user').distinct()]
        invited = RegisterConf.objects.filter(conference=conftopass[ic], status=1, type=1).order_by('user__last_name')
        invu = [invited.filter(user=item['user']).first() for item in
                invited.values('user').distinct()]
        modo = RegisterConf.objects.filter(conference=conftopass[ic], role=1).order_by('user__last_name')
        modu = [modo.filter(user=item['user']).first() for item in
                modo.values('user').distinct()]


        #Invited speakers:
        if invu:
            pdf.set_font('DejaVu', 'B', 15)
            pdf.cell(h=3, w=0, txt="Invited speakers")
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            for inv in invu:
                pdf.cell(h=3, w=0, txt=inv.user.first_name+' '+inv.user.last_name)
                pdf.ln(7)

        #Virtual organizing committee:
        if locu:
            pdf.set_font('DejaVu', 'B', 15)
            pdf.cell(h=3, w=0, txt="Virtual Organizing committee")
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            for loca in locu:
                pdf.cell(h=3, w=0, txt=loca.user.first_name+' '+loca.user.last_name)
                pdf.ln(7)

        # Virtual organizing committee:
        if socu:
            pdf.set_font('DejaVu', 'B', 15)
            pdf.cell(h=3, w=0, txt="Program committee")
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            for soca in socu:
                pdf.cell(h=3, w=0,txt=soca.user.first_name + ' ' + soca.user.last_name)
                pdf.ln(7)

        pdf.set_font('DejaVu', 'B', 15)
        pdf.multi_cell(h=10, w=0, txt="Program Schedule")
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(h=3, w=0, txt="All times are in your timezone: "+str(local))

        change=1
        if schedule:
            prevdate = schedule[0].start_date+shift
            for sch in schedule:
                if (sch.start_date+shift).date() != prevdate.date():
                    #print('change')
                    change=1

                if change==1:
                    formatedDate = sch.start_date.strftime("%A %d")
                    pdf.ln(10)
                    pdf.cell(h=3, w=0, txt=formatedDate)
                    pdf.line(10, pdf.get_y()+5, 110, pdf.get_y()+5)
                    pdf.ln(10)
                    change=0

                if sch.type != 7:
                    #$pdf->MultiCell(100, 3, "We declare ", 1, 'L', false);

                    pdf.multi_cell(h=6, w=0, txt=(sch.start_date+shift).strftime("%H:%M")+"-"+(sch.end_date+shift).strftime("%H:%M")+"        "+sch.speaker+" -- "+sch.text,align='L')
                else:
                    pdf.multi_cell(h=6, w=0, txt=(sch.start_date+shift).strftime("%H:%M")+"-"+(sch.end_date+shift).strftime("%H:%M")+"        "+sch.text,align='L')


                    #pdf.cell(0, 5, sch.text, 0, 0, 'C')

                    #pdf.cell(0, 5, "Abstract book for the conference: " + conftopass.title, 0, 0, 'C')

                #pdf.cell(h=3, w=0, txt=str(sch.start_date)+str(sch.end_date)+sch.text+sch.abstract+sch.get_type_display()+sch.speaker)
                pdf.ln(7)

                prevdate = sch.start_date+shift

        if modu:
            pdf.ln(10)
            pdf.set_font('DejaVu', 'B', 15)
            pdf.cell(h=3, w=0, txt="Chairs")
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            for moda in modu:
                pdf.cell(h=3, w=0,txt=moda.user.first_name + ' ' + moda.user.last_name)
                pdf.ln(7)

        i=1
        pdf.set_font('DejaVu', 'B', 17)
        pdf.ln(10)
        pdf.cell(h=3, w=0, txt="Contributed talks")
        pdf.ln(15)
        for talk in talks:
            #print('safe',SafeString(talk.abstract))
            pdf.set_font('DejaVu', 'B', 13)
            pdf.cell(h=3, w=0, txt=str(i)+") "+talk.user.first_name+' '+talk.user.last_name)
            pdf.ln(7)
            pdf.set_font('DejaVu', 'B', 12)
            pdf.multi_cell(h=5, w=0, txt="Title: "+talk.title)
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            #pdf.multi_cell(h=10, w=0, txt=SafeString(talk.abstract))
            if talk.abstract:
                rep = talk.abstract
                # check for img tag
                if 'img' in talk.abstract:
                    #print('img')
                    # pdf.ln(25)
                    # pdf.set_xy(80., 30.0)
                    import re
                    match = re.search(r'src="(.*?)"', rep)
                    if '.jpg' in match[0] or '.jpeg' in match[0] or '.JPG' in match[0] or '.JPEG' in match[0]:
                        rep = talk.abstract.replace('img', 'span')  # .replace('src', 'href')
                        print('match', match[0])
                    else:
                        rep = talk.abstract.replace('img', 'img height="100"')

                    #rep = talk.abstract.replace('img', 'img height="100"')
                    #print('rep', rep)
                    # pdf.ln(25)
                    # pdf.set_xy(80., 30.0)
                print('nope')
                pdf.write_html("Abstract: " + rep.encode('latin-1', 'replace').decode('latin-1'))
                #pdf.write_html("Abstract: "+talk.abstract.encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(15)
            i+=1

        if conftopass[ic].poster:
            if posters:
                j = 1
                pdf.set_font('DejaVu', 'B', 17)
                pdf.ln(10)
                pdf.cell(h=3, w=0, txt="Posters")
                pdf.ln(15)
                for post in posters:
                    # print('safe',SafeString(talk.abstract))
                    pdf.set_font('DejaVu', 'B', 13)
                    pdf.cell(h=3, w=0, txt=str(j) + ") " + post.user.first_name + ' ' + post.user.last_name)
                    pdf.ln(7)
                    pdf.set_font('DejaVu', '', 12)
                    pdf.multi_cell(h=5, w=0, txt="Title: " + post.title)
                    pdf.ln(7)
                    pdf.set_font('DejaVu', '', 12)
                    # pdf.multi_cell(h=10, w=0, txt=SafeString(talk.abstract))
                    if post.abstract:
                        print('2035',post.abstract)
                        rep6 = post.abstract
                        if 'img' in post.abstract:
                            print('img4')
                            import re
                            match = re.search(r'src="(.*?)"', rep6)
                            if '.jpg' in match[0] or '.jpeg' in match[0] or '.JPG' in match[0] or '.JPEG' in match[0]:
                                rep6 = post.abstract.replace('img', 'span')#.replace('src', 'href')
                                print('match',match[0])
                            else:
                                rep6 = post.abstract.replace('img', 'img height="100"')
                            print('rep6',rep6)

                        pdf.write_html("Abstract: " + rep6.encode('latin-1', 'replace').decode('latin-1'))

                    #if post.abstract:
                    #    pdf.write_html("Abstract: " + post.abstract.encode('latin-1', 'replace').decode('latin-1'))
                        pdf.ln(15)
                    j += 1
                pdf.ln(15)

        #Participants name affiliation email
        pdf.set_font('DejaVu', 'B', 17)
        pdf.cell(h=3, w=0,txt='Participants')
        pdf.ln(7)
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(h=3, w=0,txt='Number of participants: '+str(len(uniqueusers)))
        pdf.ln(12)

        for users in uniqueusers:
            pdf.cell(h=3, w=0, txt=users.user.first_name+' '+users.user.last_name+' ('+users.user.userprofileinfo.institute+')')
            pdf.ln(7)

    pdf.alias_nb_pages()

    pdf.set_author('CarbonFreeConf')

    #pdf.set_doc_option('core_fonts_encoding', 'utf-8')

    #print("pdf.output(dest='S')",pdf.output(dest='S').encode('latin-1'))

    #return pdf.output(dest='S').encode('latin-1')
    return pdf.output(dest='S')#.encode('latin-1', 'ignore')

    #return pdf.output(name='joe.pdf').encode('latin-1')


def createabstractbook(request,confnum):
    from fpdf import FPDF, HTMLMixin

    class MyFPDF(FPDF, HTMLMixin):

        #def header(self):
            # Logo
            #self.image('logo_pb.png', 10, 8, 33)
            # Arial bold 15
            #self.set_font('Arial', 'B', 7)
            # Move to the right
            #self.cell(80)
            # Title
            #self.cell(30, 10, 'Carbon-neutral conference powered by carbonfreeconf.com', 0, 0, 'C')
            # Line break
            #self.ln(20)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    tzloc = request.session.get('django_timezone', '')  # request.session['django_timezone']
    if tzloc:
        local = pytz.timezone(tzloc)
    else:
        local = pytz.timezone('UTC')

    now = datetime.datetime.utcnow()  # .replace(tzinfo=utc)
    shift = now.astimezone(local).replace(tzinfo=None) - now.replace(tzinfo=None)
    print('shift',shift)

    conftopass2 = CreateConf.objects.filter(id=confnum)

    if conftopass2[0].masterconf:
        conftopass3=CreateConf.objects.filter(masterconfidfordaughter=confnum,acceptconf=True).order_by('title')
        from itertools import chain
        conftopass = list(chain(conftopass2,conftopass3))        #conftopass =conftopass2 | conftopass3
        #print('getall',conftopass)

    else:
        conftopass = conftopass2

    print('conftopass',conftopass2)

    #print('confx',confnum)
    #from fpdf import FPDF, pdf.write_html(html)



    pdf = MyFPDF('P', 'mm', 'A4')

    #pdf = FPDF()
    pdf.add_page()
    #pdf.set_global('SYSTEM_TTFONTS', "my_app/font/")
    #FPDF_FONTPATH = 'my_app/font/'
    #pdf.add_font('Comic Sans', '', '/app/my_app/font/Comic_Sans_MS.ttf', uni=True)

    #print('path',os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed.ttf'))
    pdf.add_font('DejaVu', '', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed-Bold.ttf'), uni=True)
    pdf.add_font('DejaVu', 'I', os.path.join(settings.BASE_DIR, "font", 'DejaVuSansCondensed-Oblique.ttf'), uni=True)

    #pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    #pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    #pdf.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
    #pdf.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)

    pdf.set_font('DejaVu', '', 14)

    #pdf.set_fill_color(32.0, 47.0, 250.0)  # color for outer rectangle
    #pdf.rect(5.0, 5.0, 200.0, 287.0, 'DF')
    #pdf.set_fill_color(255, 255, 255)  # color for inner rectangle
    #pdf.rect(8.0, 8.0, 194.0, 282.0, 'FD')

    #header
    # Set up a logo
    #pdf.image('fg', 10, 8, 33)
    pdf.set_font('DejaVu', 'B', 20)

    # Add an address
    #pdf.cell(100)

    pdf.multi_cell(0, 7, "List of abstracts for the conference: "+conftopass2[0].title, 0, 'C')

    #pdf.cell(100)
    #pdf.cell(0, 5, '123 American Way', ln=1)
    #pdf.cell(100)
    #pdf.cell(0, 5, 'Any Town, USA', ln=1)

    print('before room logo')
    if conftopass2[0].room_logo:
        if not conftopass2[0].room_logo.url.endswith('.jpg') and not conftopass2[0].room_logo.url.endswith('.jpeg'):
            pdf.ln(25)
            pdf.set_xy(80., 30.0)
            pdf.image(conftopass2[0].room_logo.url, link='', type='',w=60)

    print('after room logo')

    # Line break
    pdf.ln(20)

    #pdf.line(10, 10, 10, 100)
    #pdf.set_line_width(1)
    #pdf.set_draw_color(255, 0, 0)
    #pdf.line(20, 20, 100, 20)

    #pdf.set_font('Times', 'B', 15)
    #pdf.cell(w=210, h=9, txt=title, border=0, ln=1, align='C', fill=0)
    #pdf.set_font('Times', 'B', 15)
    #pdf.cell(w=0, h=6, txt=heading, border=0, ln=1, align='L', fill=0)
    #pdf.set_font('Times', '', 12)
    #pdf.multi_cell(w=0, h=5, txt=text)
    #response.headers['Content-Type'] = 'application/pdf'
    #return pdf.output(dest='S')
    #from django.utils.safestring import SafeString



    for ic in range(len(conftopass)):
        if len(conftopass)>1:
            pdf.ln(10)
            pdf.set_font('DejaVu', 'B', 18)
            if ic==0:
                pdf.multi_cell(h=10, w=0, txt="Plenary session: "+conftopass[ic].title)
            else:
                pdf.multi_cell(h=10, w=0, txt="Session "+str(ic)+") "+conftopass[ic].title)
            pdf.ln(10)

        pdf.set_font('DejaVu', 'B', 15)
        if len(conftopass)>1:
            pdf.multi_cell(h=10, w=0, txt="Session Abstract")
        else:
            pdf.multi_cell(h=10, w=0, txt="Conference Abstract")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(h=10, w=0, txt=conftopass[ic].abstract)
        pdf.ln(20)

        talks = RegisterConf.objects.filter(conference=conftopass[ic], type__in=[1, 2, 3, 6]).order_by(
            'user__last_name')
        talksetal = RegisterConf.objects.filter(conference=conftopass[ic]).order_by('user__last_name')

        schedule = Schedule.objects.filter(conference=conftopass[ic]).order_by('start_date')

        print('talks', talks)

        uniqueusers = [talksetal.filter(user=item['user']).first() for item in
                       talksetal.values('user').distinct()]

        posters = RegisterConf.objects.filter(conference=conftopass[ic], type=4).order_by('user__last_name')


        i=1
        pdf.set_font('DejaVu', 'B', 17)
        pdf.ln(10)
        pdf.cell(h=3, w=0, txt="Talks")
        pdf.ln(15)
        for talk in talks:
            print('ta',talk)
            #print('safe',SafeString(talk.abstract))
            pdf.set_font('DejaVu', 'B', 13)
            pdf.cell(h=3, w=0, txt=str(i)+") "+talk.user.first_name+' '+talk.user.last_name+ ' ('+talk.get_status_display()+')')
            pdf.ln(7)
            pdf.set_font('DejaVu', 'B', 12)
            pdf.multi_cell(h=5, w=0, txt="Title: "+talk.title)
            pdf.ln(7)
            pdf.set_font('DejaVu', '', 12)
            #pdf.multi_cell(h=10, w=0, txt=SafeString(talk.abstract))
            if talk.abstract:
                #text2 = text.encode('latin-1', 'replace').decode('latin-1')
                #pdf.set_font('DejaVu', '', 12)
                print('2033',talk.abstract)
                rep = talk.abstract
                #check for img tag
                if 'img' in talk.abstract:
                    print('img')
                    #pdf.ln(25)
                    #pdf.set_xy(80., 30.0)
                    import re
                    match = re.search(r'src="(.*?)"', rep)
                    if '.jpg' in match[0] or '.jpeg' in match[0] or '.JPG' in match[0] or '.JPEG' in match[0]:
                        rep = talk.abstract.replace('img', 'span')  # .replace('src', 'href')
                        print('match', match[0])
                    else:
                        rep = talk.abstract.replace('img', 'img height="100"')
                    #rep=talk.abstract.replace('img','img height="100"')
                    print('rep',rep)
                    #pdf.ln(25)
                    #pdf.set_xy(80., 30.0)
                pdf.write_html("Abstract: "+rep.encode('latin-1', 'replace').decode('latin-1'))
                #pdf.write_html("Abstract: "+talk.abstract)

            if talk.biography:
                print('bio',talk.biography)
                rep2 = talk.biography

                pdf.ln(7)
                pdf.write_html("Biography: "+rep2.encode('latin-1', 'replace').decode('latin-1'))

                #pdf.multi_cell(h=5, w=0, txt="Biography: " + talk.biography)


            pdf.ln(15)

            i+=1

        if conftopass[ic].poster:
            if posters:
                j = 1
                pdf.set_font('DejaVu', 'B', 17)
                pdf.ln(10)
                pdf.cell(h=3, w=0, txt="Posters")
                pdf.ln(15)
                for post in posters:
                    # print('safe',SafeString(talk.abstract))
                    print('ti',post.title)
                    pdf.set_font('DejaVu', 'B', 13)
                    pdf.cell(h=3, w=0, txt=str(j) + ") " + post.user.first_name + ' ' + post.user.last_name + ' ('+post.get_status_display()+')')
                    pdf.ln(7)
                    pdf.set_font('DejaVu', '', 12)
                    pdf.multi_cell(h=5, w=0, txt="Title: " + post.title)
                    pdf.ln(7)
                    pdf.set_font('DejaVu', '', 12)
                    # pdf.multi_cell(h=10, w=0, txt=SafeString(talk.abstract))
                    if post.abstract:
                        print('2034',post.abstract)
                        rep4 = post.abstract
                        if 'img' in post.abstract:
                            print('img4')
                            import re
                            match = re.search(r'src="(.*?)"', rep4)
                            if '.jpg' in match[0] or '.jpeg' in match[0] or '.JPG' in match[0] or '.JPEG' in match[0]:
                                rep4 = post.abstract.replace('img', 'span')#.replace('src', 'href')
                                print('fmatch',match[0])
                                print('rep426',rep4)
                            else:
                                rep4 = post.abstract.replace('img', 'img height="100"')
                                print('rep42',rep4)

                        pdf.write_html("Abstract: " + rep4.encode('latin-1', 'replace').decode('latin-1'))
                        #pdf.ln(15)

                    if post.biography:
                        print('biopost', post.biography)
                        rep3 = post.biography

                        pdf.ln(7)
                        pdf.write_html("Biography: " + rep3.encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln(15)

                    j += 1
                #pdf.ln(15)

        #Participants name affiliation email
        pdf.set_font('DejaVu', 'B', 17)
        pdf.cell(h=3, w=0,txt='Participants')
        pdf.ln(7)
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(h=3, w=0,txt='Number of participants: '+str(len(uniqueusers)))
        pdf.ln(12)

        for users in uniqueusers:
            pdf.cell(h=3, w=0, txt=users.user.first_name+' '+users.user.last_name+' ('+users.user.userprofileinfo.institute+')')
            pdf.ln(7)

    pdf.alias_nb_pages()

    pdf.set_author('CarbonFreeConf')

    #pdf.set_doc_option('core_fonts_encoding', 'utf-8')

    #print("pdf.output(dest='S')",pdf.output(dest='S').encode('latin-1'))

    #return pdf.output(dest='S').encode('latin-1')
    return pdf.output(dest='S')#.encode('latin-1', 'ignore')


def funcvalidate(conftopass, size, userr, talknumber,cantchange):

    print('cantchange',cantchange)

    userconf = RegisterConf.objects.filter(
        Q(conference=conftopass, role=3) | Q(conference=conftopass, socloc__in=[1, 2]) | Q(
            conference=conftopass, status=1))
    # print('userconf', userconf, len(userconf))
    item_nbuser = [userconf.filter(user=item['user']).first() for item in
                   userconf.values('user').distinct()]
    # print('item', item_nbuser)
    nbuserconf = len(item_nbuser)

    #for user in userconf:
    #    print('username', user.user.username)

    if nbuserconf > 1.1 * size:
        # faire un truc
        print('attention too many participants')

    else:
        if 0 == 0:
            print('tn',talknumber,conftopass)
            regtalk = RegisterConf.objects.filter(user=userr, conference=conftopass)[talknumber]
            print('rt',regtalk.title)
            if regtalk.status == 0:
                regtalk.status = 1

                if conftopass.masterconf or conftopass.daughterconf:
                    # check if other attendance only and accept them if conf where can access all talks
                    masterconftopass = CreateConf.objects.filter(masterconfpass=conftopass.masterconfpass, masterconf=True)[0]
                    if masterconftopass.parsession:
                        # check if talk in master session and else
                        # add to master session automatically

                        mastertalk = RegisterConf.objects.filter(user=userr,
                                                                 conference__masterconfpass=conftopass.masterconfpass,
                                                                 conference__masterconf=True, status=1)



                        # quentin
                        if masterconftopass.subtomastautomatic:
                            if not mastertalk:
                                print('not')
                                if RegisterConf.objects.filter(user=userr, conference=masterconftopass).exists():
                                    print('exist')
                                    existingmasttalks=RegisterConf.objects.filter(user=userr, conference=masterconftopass)
                                    for e in existingmasttalks:
                                        if e.type==5:
                                            e.status=1
                                else:
                                    print('pasexist')
                                    obj, created = RegisterConf.objects.update_or_create(
                                        user=userr, conference=masterconftopass,
                                        defaults={'status': 1, 'type': 5, 'title': 'Attendance only'},
                                    )

                        allattendtalk = RegisterConf.objects.filter(user=userr,
                                                                    conference__masterconfpass=conftopass.masterconfpass,
                                                                    status=0, type=5)

                        for at in allattendtalk:
                            print('at',at.title)
                            at.status = 1

                            if regtalk.free:
                                at.free = True

                            at.save()

                            #do rocket chat subscription in asynchronous coz otherwise it goes beyond 30sec
                            print('y',at.conference.title, userr.username)
                            x = asynchronouschatsub.delay(at.conference.title, userr.username)
                            print('x')

                # try:
                with sessions.Session() as session2:
                    # log-in

                    try:
                        rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                            server_url='https://chat.carbonfreeconf.com', session=session2)
                    except:
                        subject = "Nooooooooo Rocket chat what????"
                        message = "Oups <strong>Rocket chat</strong> fait de la merde!!!!"
                        # message+="<img src='https://bucketeer-83011bf8-623d-4ad2-8e34-40829bae363d.s3.amazonaws.com/static/images/carbonfreeconf_logo_title.svg' width='200' height='60' alt='Make my own CarbonFreeConf workshop'>"

                        emailto = []
                        emailto.append("quentin.kral@gmail.com")
                        emailto.append("carbonfreeconf@gmail.com")

                        email = EmailMessage(
                            subject,
                            message,
                            'CarbonFreeConf <communication@carbonfreeconf.com>',  # from
                            emailto,  # to
                            # getemails,  # bcc
                            # reply_to=replylist,
                            headers={'Message-From': 'www.carbonfreeconf.com'},
                        )
                        email.content_subtype = "html"

                        #email.send(fail_silently=False)
                    slugtitleconf = slugify(str('%s' % (conftopass.title)))
                    # print('slug', slugtitleconf)
                    #list = rocket.groups_list_all().json()
                    # print('l', list)
                    # pprint(rocket.groups_info(room_name=slugtitleconf).json())
                    contentroom = rocket.groups_info(room_name=slugtitleconf).json()
                    # print('c', contentroom)
                    if contentroom['success'] == True:
                        keyroom = contentroom['group']['_id']

                        contentuser = rocket.users_info(username=userr.username).json()
                        # if contentuser['success'] == True:
                        key = contentuser['user']['_id']
                        # print('keyo',key,keyroom)

                        pprint(rocket.groups_invite(room_id=keyroom, user_id=key).json())

                        slugtitleconfcafe = slugify(
                            str('%s' % ('Coffee break for ' + conftopass.title)))

                        contentroomcafe = rocket.groups_info(room_name=slugtitleconfcafe).json()
                        if contentroomcafe['success']:
                            # print('c', contentroomcafe)
                            keyroomcafe = contentroomcafe['group']['_id']

                            contentusercafe = rocket.users_info(username=userr.username).json()
                            keycafe = contentusercafe['user']['_id']
                            # print('keyo',key,keyroom)

                            pprint(rocket.groups_invite(room_id=keyroomcafe, user_id=keycafe).json())

                if conftopass.daughterconf:  # or conftopass.masterconf:
                    # find mast conf room
                    # tbbbbbbbbbbbbbbbbbbbbbbbbbb
                    confmast = \
                        CreateConf.objects.filter(masterconfpass=conftopass.masterconfpass, masterconf=True)[0]
                    slugtitleconfmast = slugify(str('%s' % (confmast.title)))

                    contentroommast = rocket.groups_info(room_name=slugtitleconfmast).json()
                    if contentroommast['success'] == True:
                        keyroommast = contentroommast['group']['_id']
                        # print('keyroommast', keyroommast)

                        pprint(rocket.groups_invite(room_id=keyroommast, user_id=key).json())

                    slugtitleconfcafemast = slugify(
                        str('%s' % ('Coffee break for ' + confmast.title)))

                    contentroomcafemast = rocket.groups_info(room_name=slugtitleconfcafemast).json()
                    if contentroomcafemast['success']:
                        # print('c', contentroomcafemast)
                        keyroomcafemast = contentroomcafemast['group']['_id']

                        contentusercafemast = rocket.users_info(username=userr.username).json()
                        keycafemast = contentusercafemast['user']['_id']
                        # print('keyo',key,keyroom)

                        pprint(rocket.groups_invite(room_id=keyroomcafemast, user_id=keycafemast).json())

                rocket.logout()
                # except:
                # print('noooo')


            elif cantchange == 0 and regtalk.status == 1:
                # print('!!!!!!!!!!!!!!!!!!!!a')

                regtalk.status = 0

                if conftopass.masterconf and conftopass.subtomastautomatic:
                    # find all talks of person
                    daughtalks = RegisterConf.objects.filter(user=userr,
                                                             conference__masterconfpass=conftopass.masterconfpass,
                                                             conference__daughterconf=True, status=1)
                    # print('daughtalks',daughtalks)
                    for dau in daughtalks:
                        # print('ti',dau.title,dau.conference.title)
                        dau.status = 0
                        dau.save()

                with sessions.Session() as session3:
                    # log-in
                    try:
                        rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                            server_url='https://chat.carbonfreeconf.com', session=session3)
                    except:
                        subject = "Nooooooooo Rocket chat what????"
                        message = "Oups <strong>Rocket chat</strong> fait de la merde!!!!"
                        # message+="<img src='https://bucketeer-83011bf8-623d-4ad2-8e34-40829bae363d.s3.amazonaws.com/static/images/carbonfreeconf_logo_title.svg' width='200' height='60' alt='Make my own CarbonFreeConf workshop'>"

                        emailto = []
                        emailto.append("quentin.kral@gmail.com")
                        emailto.append("carbonfreeconf@gmail.com")

                        email = EmailMessage(
                            subject,
                            message,
                            'CarbonFreeConf <communication@carbonfreeconf.com>',  # from
                            emailto,  # to
                            # getemails,  # bcc
                            # reply_to=replylist,
                            headers={'Message-From': 'www.carbonfreeconf.com'},
                        )
                        email.content_subtype = "html"

                        #email.send(fail_silently=False)

                    slugtitleconf = slugify(str('%s' % (conftopass.title)))
                    # print('slug', slugtitleconf)
                    #list = rocket.groups_list_all().json()
                    # print('l', list)
                    # pprint(rocket.groups_info(room_name=slugtitleconf).json())
                    contentroom = rocket.groups_info(room_name=slugtitleconf).json()
                    if contentroom['success'] == True:
                        # print('c', contentroom)
                        keyroom = contentroom['group']['_id']

                        contentuser = rocket.users_info(username=userr.username).json()
                        key = contentuser['user']['_id']
                        # print('keyo', key, keyroom)

                        pprint(rocket.groups_kick(room_id=keyroom, user_id=key).json())

                    if conftopass.daughterconf:  # or conftopass.masterconf:
                        # find mast conf room
                        # tbbbbbbbbbbbbbbbbbbbbbbbbbb
                        confmast = \
                            CreateConf.objects.filter(masterconfpass=conftopass.masterconfpass, masterconf=True)[0]
                        slugtitleconfmast = slugify(str('%s' % (confmast.title)))
                        contentroommast = rocket.groups_info(room_name=slugtitleconfmast).json()

                        if contentroommast['success'] == True:
                            keyroommast = contentroommast['group']['_id']
                            # print('keyroommast', keyroommast)

                        # We don't kick out in case the person is in multiple sessions and is kicked out only from one
                        # pprint(rocket.groups_kick(room_id=keyroommast, user_id=key).json())

                    rocket.logout()
                    # except:
                    # print('noooo2')

            print('save')
            regtalk.save()
        else:
            # can't undo talk of master conf chief
            print('nope')
    #return HttpResponseRedirect(reverse('my_app:createconf'))
    return 1

def conf_list_user(request):
    if not request.user.is_authenticated:
        stuff_for_frontend = {
            'conf_list_user': None
        }
        return None#stuff_for_frontend
    else:
        # a partir d'ici remplacer request.user by mainusertbb
        if request.user.is_superuser:
            querysetother = RegisterConf.objects.filter()#tbb
        else:
            querysetother = RegisterConf.objects.filter(user=request.user,role=3)#tbb
            #print('qq', querysetother.values_list('conference__title',flat=True))


        querysetotherunique = [querysetother.filter(conference=item['conference']).first() for item in
                    querysetother.values('conference').distinct()]
        other=0
        #print('querysetunique', querysetotherunique)
        querysetotherconf2=CreateConf.objects.none()

        if request.user.is_superuser:
            for i in range(len(querysetotherunique)):

                querysetotherconf = CreateConf.objects.filter(id=querysetotherunique[i].conference.id).order_by('-start_date')

                querysetotherconf2 = querysetotherconf2 | querysetotherconf

            queryset = querysetotherconf2

        else:

            if querysetotherunique:
                for i in range(len(querysetotherunique)):
                    #print('iq',i,querysetotherunique[i].conference)
                    if UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user):
                        mainuser = UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
                        if mainuser != request.user.id:
                            querysetotherconf = CreateConf.objects.filter(user=mainuser,id=querysetotherunique[i].conference.id).order_by('-start_date')
                            #print('q',i,mainuser,querysetotherconf)
                            other=1
                            querysetotherconf2=querysetotherconf2|querysetotherconf

                #for i in range(len(querysetother)):
                 #   mainuser = UserLink.objects.filter(conference=querysetother[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
                  #  querysetotherconf = CreateConf.objects.filter(user=mainuser,conference=querysetother[i].conference).order_by('-start_date')
                   # print('rrez',i,mainuser,querysetotherconf)
                            #print('Geo',querysetotherconf)

            queryset = CreateConf.objects.filter(user=request.user).order_by('-start_date')

            if other==1:
                #print('Geo')
                queryset=queryset|querysetotherconf2

        stuff_for_frontend = {
            'conf_list_user': queryset
        }
    return queryset#stuff_for_frontend

def conf_list_user_inv(request):
    if not request.user.is_authenticated:
        stuff_for_frontend = {
            'conf_list_user_inv': None
        }
        return None#stuff_for_frontend
    else:
        # a partir d'ici remplacer request.user by mainusertbb
        querysetother = RegisterConf.objects.filter(user=request.user,role__lt=3,status=1)#tbb
        #print('rrezdddgraphy', querysetother)


        querysetotherunique = [querysetother.filter(conference=item['conference']).first() for item in
                    querysetother.values('conference').distinct()]
        other=0
        #print('querysetuniquegraphy', querysetotherunique)
        querysetotherconf2=CreateConf.objects.none()

        if querysetotherunique:
            for i in range(len(querysetotherunique)):
                #print('i',i,querysetotherunique[i].conference)
                #if UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user):
                #    mainuser = UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
                #    if mainuser != request.user.id:
                querysetotherconf = CreateConf.objects.filter(id=querysetotherunique[i].conference.id).order_by('-start_date')
                #print('rrez',i,querysetotherconf)
                other=1
                querysetotherconf2=querysetotherconf2|querysetotherconf

            #for i in range(len(querysetother)):
             #   mainuser = UserLink.objects.filter(conference=querysetother[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
              #  querysetotherconf = CreateConf.objects.filter(user=mainuser,conference=querysetother[i].conference).order_by('-start_date')
               # print('rrez',i,mainuser,querysetotherconf)
                        #print('Geography',querysetotherconf2)

        #queryset = CreateConf.objects.filter(user=request.user).order_by('-start_date')
        #queryset=CreateConf.objects.none()

        #stuff_for_frontend = {
        #    'conf_list_user_inv': False
        #}

        queryset=None
        if other==1:
        #if querysetotherunique:
            #print('Geo')
            queryset=querysetotherconf2
            #queryset=querysetotherunique
            #print('rreze',queryset)
        #stuff_for_frontend = {
        #        'conf_list_user_inv': queryset
        #    }
        return queryset#stuff_for_frontend


def conf_list_user_inv2(request):
    if not request.user.is_authenticated:
        stuff_for_frontend = {
            'conf_list_user_inv2': None
        }
        return None#stuff_for_frontend
    else:
        # a partir d'ici remplacer request.user by mainusertbb
        querysetother = RegisterConf.objects.filter(user=request.user,role__lt=4,status=1)#tbb
        #print('rrezdddgraphy', querysetother)


        querysetotherunique = [querysetother.filter(conference=item['conference']).first() for item in
                    querysetother.values('conference').distinct()]
        other=0
        #print('querysetuniquegraphy', querysetotherunique)
        querysetotherconf2=CreateConf.objects.none()

        if querysetotherunique:
            for i in range(len(querysetotherunique)):
                #print('i',i,querysetotherunique[i].conference)
                #if UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user):
                    #mainuser = UserLink.objects.filter(conference=querysetotherunique[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
                    #if mainuser != request.user.id:
                querysetotherconf = CreateConf.objects.filter(id=querysetotherunique[i].conference.id).order_by('-start_date')
                #print('rrez',i,mainuser,querysetotherconf)
                other=1
                querysetotherconf2=querysetotherconf2|querysetotherconf

            #for i in range(len(querysetother)):
             #   mainuser = UserLink.objects.filter(conference=querysetother[i].conference, user=request.user).values_list('mainuser', flat=True)[0]
              #  querysetotherconf = CreateConf.objects.filter(user=mainuser,conference=querysetother[i].conference).order_by('-start_date')
               # print('rrez',i,mainuser,querysetotherconf)
                    #print('Geography',querysetotherconf2)

        #queryset = CreateConf.objects.filter(user=request.user).order_by('-start_date')
        #queryset=CreateConf.objects.none()

        stuff_for_frontend = {
            'conf_list_user_inv2': False
        }

        queryset=None
        if other==1:
            #print('Geo')
            queryset=querysetotherconf2

            stuff_for_frontend = {
                'conf_list_user_inv2': queryset
            }
    return queryset#stuff_for_frontend
