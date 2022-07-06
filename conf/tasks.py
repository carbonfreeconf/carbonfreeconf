from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
#from djmoney import settings
#from celery import shared_task
#from djmoney.contrib.exchange.backends import OpenExchangeRatesBackend
#from django.conf import settings
#from conf.my_app.utils import updateratesautomatically

from django.core.mail import EmailMessage

#from my_app.utils import uploadvidtovimeo
from six.moves import urllib
from django.conf import settings

#from django.conf.my_app.models import CreateVisio
from django.apps import apps
from celery import shared_task
import requests
import json
from django.http import HttpResponse
from django.db import transaction
import jwt
import time
import http.client
from django.db.models import Q
import http.client
from rocketchat_API.rocketchat import RocketChat
from requests import sessions
from django.core.mail import EmailMessage
from django.utils.text import slugify
import tweepy
from datetime import date
from pprint import pprint


#from djmoney.contrib.exchange.backends import OpenExchangeRatesBackend

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

import django
django.setup()
from conf.celery import app as celery_app
#from celery.schedules import crontab

os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'


@shared_task
def task1():

    print('Hello World!')

    return 'results'

#from celery import task


#app = Celery('tasks')

#@app.task
#def echoe():
#    """
#    A simple task that echoes a Hello World! text to celery console.
#    """
#    print('Hello World!')

@shared_task
def add(x, y):
    return x + y

#@shared_task
#def update_rates():
#    backend = import_string(backend)()
#    OpenExchangeRatesBackend().update_rates()#pas sur que ca marche car je peux pas importer...
#    updateratesautomatically()

#app.conf.beat_schedule = {
    # Executes every day at  12:30 pm.
#    'run-every-afternoon': {
#        'task': 'tasks.add',
#        'schedule': 10.,#crontab(hour=14, minute=33),
#        'args': (),
#    },
#}

#@celery_app.on_after_finalize.connect
#def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, test.s('hello'))

    #sender.add_periodic_task(crontab(hour=11, minute=1),add.s(2,12),name='brah')

@shared_task
def test(arg):
    print(arg)

#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
#    sender.add_periodic_task(1., add.s(2,2), name='every 6 hours')
#    sender.add_periodic_task(21600., update_rates.s(), name='every 6 hours')

    # Executes every day at 15h01 UTC, it works...if needed
#    sender.add_periodic_task(
#        crontab(hour=15, minute=1),
#        add.s(2,2),name='brah'
#    )

@shared_task
def sendgroupemailasynchronously(emailmes):
    emailmes.send(fail_silently=False)#inaya
    return 'emails sent'

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

@shared_task
def finishzoomsession(idcf):
    payload = "{\"action\":\"end\"}"

    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    conn = http.client.HTTPSConnection("api.zoom.us")

    #conn.request("PUT", "/v2/meetings/" + str(idcf) + "/status", payload, headers)

    #res = conn.getresponse()
    #data = res.read()

    #print('finish meeting', data.decode("utf-8"))
    return "session finished"

#@task(name="asynchronousuploadvimeo")
@shared_task
def asynchronousuploadvimeo(idcf,i,urlvideo,recid,name,descr,privacy,recstart,recend):
    CreateVisio = apps.get_model(app_label='my_app', model_name='CreateVisio')

    visio = CreateVisio.objects.filter(conference_id=idcf, testroom=False)

    #else:
     #   print('nopevurl')
    #uploadfunc = apps.get_model(app_label='my_app', model_name='CreateVisio')

    #uri=utils.uploadvidtovimeo(mp4_url, tit, descr, who)

    print('filesizef',urlvideo)

    site = urllib.request.urlopen(urlvideo)

    print('site',site)

    # meta = site.info()
    file_size = int(site.getheader('Content-Length'))

    # vidsize=meta.getheaders("Content-Length")
    # charset = meta.headers.get_content_charset()
    print('filesize', file_size)

    # WHO_CHOICES = (
    #    (ANY, "Everyone"),
    #    (MEMB, "Only conference participants"),
    #    (PRIV, "Only through a private link"),
    # )

    # whorecording
    if privacy == "Everyone":
        privacyvim = "anybody"
    elif privacy == "Only conference participants":
        privacyvim = "disable"#"unlisted"#"nobody"
    else:
        privacyvim = "nobody"

    url = 'https://api.vimeo.com/me/videos'
    # headers = {'Authorization': 'bearer %s' % settings.SECRETVIM, 'Content-Type': 'application/json','Accept': 'application/vnd.vimeo.*+json;version=3.4'}
    headers = {'Authorization': 'bearer %s' % settings.SECRETVIM, 'Content-Type': 'application/json',
               'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

    name2 = (name[:124] + '...') if len(name) > 124 else name
    data = {'upload': {'approach': 'tus', 'size': file_size}, 'name': name2, 'description': descr,
            'privacy': {'view': privacyvim, 'embed': 'public'}}

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print('r', r,name,descr,file_size,privacyvim)
    print('tt', json.loads(r.content.decode('utf-8')))

    if r.status_code == 200:
        print('ro', r)

        uri = r.json()['uri']  # link to final video
        upload_link = r.json()['upload']['upload_link']
        approach = r.json()['upload']['approach']  # should be tus

        print('r2', uri, upload_link, approach)

        if approach == 'tus':
            # first attempt to upload video

            headers = {'Tus-Resumable': '1.0.0', 'Upload-Offset': '0',
                       'Content-Type': 'application/offset+octet-stream',
                       'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

            # video_rb = video.open('rb')
            # videolink = 'https://d14c1kqvi6lpt9.cloudfront.net/03bdcde6e854-1591281300/bigmarker-recording.mp4'
            # recid=4c0342c6d4a6
            # video_rb = videolink.open('rb')

            # vid = urllib.request.urlopen(videolink)
            # fhand = open('cover3.jpg', 'wb')
            size = 0
            CHUNK = 1024 * 1024 * 2  # 2Mb
            while True:
                info = site.read(CHUNK)
                if len(info) < 1: break
                size = size + len(info)
                r = requests.patch(upload_link, info, headers=headers)
                print('rdf', size, r)
                headers = {'Tus-Resumable': '1.0.0', 'Upload-Offset': str(size),
                           'Content-Type': 'application/offset+octet-stream',
                           'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

            print(size, 'video uploaded.')
            # fhand.close()

            # r = requests.patch(upload_link, video_rb, headers=headers)
            # r = requests.patch(upload_link, urlvideolink, headers=headers)
            # print('r3', r)
            # pprint(r)
            # Second attempt to upload video

            # Verify upload is complete

            headers = {'Tus-Resumable': '1.0.0', 'Accept': 'application/vnd.vimeo.*+json;version=3.4'}
            r = requests.head(upload_link, headers=headers)

            print('r4', r)
            # pprint(r)

            print('all good',idcf,i,uri,visio[i].mp4_url,visio[i].conference)

            #return uri

            #celery_export_file = CeleryExportFile(name=name, file=output, expiration_date=datetime.datetime.now())
            #celery_export_file.save()

            #visio[i].vimeo_url = uri
            #test=visio[i]
            #test.save(update_fields=['vimeo_url'])
            vurl0 = visio[i].vimeo_url
            vurl = []

            if vurl0:
                if "," not in vurl0:
                    vurl1 = vurl0.replace('[', '').replace(']', '').replace("'", "")
                    vurl.append(vurl1)
                else:
                    print('vurl', vurl)
                    vurl1 = vurl0.replace('[', '').replace(']', '').replace("'", "")
                    vurl = vurl1.split(',')

            vurl.append(uri)

            rights0 = visio[i].rights
            rights2 = []

            if rights0:
                if "," not in rights0:
                    rights1 = rights0.replace('[', '').replace(']', '').replace("'", "")
                    rights2.append(rights1)
                else:
                    print('rights', privacyvim)
                    rights1 = rights0.replace('[', '').replace(']', '').replace("'", "")
                    rights2 = rights1.split(',')

            rights2.append(privacyvim)

            recstart0 = visio[i].recstart
            recstart2 = []

            if recstart0:
                if "," not in recstart0:
                    recstart1 = recstart0.replace('[', '').replace(']', '').replace("'", "")
                    recstart2.append(recstart1)
                else:
                    print('recstart', recstart)
                    recstart1 = recstart0.replace('[', '').replace(']', '').replace("'", "")
                    recstart2 = recstart1.split(',')

            recstart2.append(recstart)

            recend0 = visio[i].recend
            recend2 = []

            if recend0:
                if "," not in recend0:
                    recend1 = recend0.replace('[', '').replace(']', '').replace("'", "")
                    recend2.append(recend1)
                else:
                    print('recend', recend)
                    recend1 = recend0.replace('[', '').replace(']', '').replace("'", "")
                    recend2 = recend1.split(',')

            recend2.append(recend)

            with transaction.atomic():

                obj, created = CreateVisio.objects.update_or_create(
                    id=visio[i].id,
                    defaults={'vimeo_url': vurl,'recidconf': recid, 'recstart':recstart2, 'recend':recend2,'rights':rights2},
                )
                print('dji',obj,created,vurl,visio[i].id)
                #attention j'ai rajouté rights sinon avant: defaults={'vimeo_url': vurl,'recidconf': recid, 'recstart':recstart2, 'recend':recend2},


            return "upload successful"

        else:
            print('not tus???')
            return "Problem while uploading, retry or contact the administrator"

            #return 0
    else:
        print('Problem with vimeo')
        return "Problem while uploading, retry and/or contact the administrator"

        #return 0


    #return 'upload worked'
    #return HttpResponse("upload successful")

@shared_task
def asynchronouschatsub(confnew,userr):
    print('in asynchat')
    #print('wh',confnew,userr)


    with sessions.Session() as session2:
        # log-in

        try:
            rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                server_url='https://chat.carbonfreeconf.com',
                                session=session2)
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
                'CarbonFreeConf <conference@carbonfreeconf.com>',  # from
                emailto,  # to
                # getemails,  # bcc
                # reply_to=replylist,
                headers={'Message-From': 'www.carbonfreeconf.com'},
            )
            email.content_subtype = "html"

            email.send(fail_silently=False)

        #confnew = at.conference  # paula

        slugtitleconf = slugify(str('%s' % (confnew)))
        # print('slug', slugtitleconf,confnew)
        list = rocket.groups_list_all().json()
        # print('l', list)
        # pprint(rocket.groups_info(room_name=slugtitleconf).json())
        contentroom = rocket.groups_info(room_name=slugtitleconf).json()
        # print('c', contentroom)
        if contentroom['success'] == True:
            keyroom = contentroom['group']['_id']

            contentuser = rocket.users_info(username=userr).json()
            key = contentuser['user']['_id']
            # print('keyo',key,keyroom)

            rocket.groups_invite(room_id=keyroom, user_id=key).json()

        slugtitleconfcafe = slugify(
            str('%s' % ('Coffee break for ' + confnew)))

        contentroomcafe = rocket.groups_info(room_name=slugtitleconfcafe).json()
        if contentroomcafe['success']:
            # print('c', contentroomcafe)
            keyroomcafe = contentroomcafe['group']['_id']

            contentusercafe = rocket.users_info(username=userr).json()
            keycafe = contentusercafe['user']['_id']
            # print('keyo',key,keyroom)

            rocket.groups_invite(room_id=keyroomcafe, user_id=keycafe).json()


        rocket.logout()


    return "donechat"

@shared_task
def asynchronouscheckstats(idcf,statmastid,CO2):
    RegisterConf = apps.get_model(app_label='my_app', model_name='RegisterConf')
    PosterView = apps.get_model(app_label='my_app', model_name='PosterView')
    ChatCanal = apps.get_model(app_label='my_app', model_name='ChatCanal')

    CreateVisio = apps.get_model(app_label='my_app', model_name='CreateVisio')
    User = apps.get_model(app_label='auth', model_name='User')

    CreateConf = apps.get_model(app_label='my_app', model_name='CreateConf')
    #print('idcf',idcf)

    conftopass = CreateConf.objects.filter(id=idcf)[0]

    start_date = conftopass.start_date



    timeover = False
    if start_date < date.today():
        timeover = True

    #print('conftopass',conftopass)

    StatsMaster = apps.get_model(app_label='my_app', model_name='StatsMaster')
    statmaster = StatsMaster.objects.filter(id=statmastid)[0]

    #print('statmaster',statmaster)

    allconf = CreateConf.objects.filter(
        Q(masterconfpass=conftopass.masterconfpass, acceptconf=True) | Q(masterconfpass=conftopass.masterconfpass,
                                                                         masterconf=True))

    allconfdau = CreateConf.objects.filter(masterconfpass=conftopass.masterconfpass, acceptconf=True)
    #print('allconf', allconf)
    # Number of participants

    nbparts = 0
    nbpartsevensubm = 0
    nbtalks = 0
    nbpart = 0
    nbparttot = 0
    countv = 0
    nbhourzoom = 0.
    countvview = 0.
    countvduration = 0.
    nbroom = 0
    nbmes = 0
    nbposts = 0
    nbdiff=0
    hashtagused = []
    diffemails=[]
    sup = False
    nbmespo = 0
    nbposters=0
    nbviewp = 0
    natt = 0
    nattnonacc = 0

    atton=[]
    item_list=[]
    item_listevensubm=[]
    item_listevensubmdau = []
    talksorposters=[]
    attendance=[]
    attendanceacc=[]
    attonlynonacc=[]
    talksorpostersacc=[]

    peopleallmast = RegisterConf.objects.filter(conference=conftopass)
    item_list_mast=[peopleallmast.filter(user=item['user']).values_list('user', flat=True).first() for item in
                      peopleallmast.values('user').distinct()]

    for conftopas in allconfdau:
        #print('item',item_list)#attention c'est des querysets donc set fonctionne pas, mettre .values_list('user',flat=True)
        peopleallevensubmdau = RegisterConf.objects.filter(conference=conftopas)
        # Query against the full list to return a list of objects
        item_listevensubmdau.extend([peopleallevensubmdau.filter(user=item['user']).values_list('user',flat=True).first() for item in
                             peopleallevensubmdau.values('user').distinct()])

    difflist=list(set(item_listevensubmdau) - set(item_list_mast))
    #print('difflist',difflist,len(difflist))
    nbdiff=len(difflist)

    for i in range(len(difflist)):
        usernotsub = User.objects.filter(id=difflist[i])[0]
        #print(',',usernotsub.email)
        diffemails.append(usernotsub.email)

        #obj, created = RegisterConf.objects.update_or_create(
        #    user=usernotsub, conference=conftopass,
        #    defaults={'status': 0, 'type': 5, 'role':2},
        #)#

    for conftopas in allconf:
        peopleall = RegisterConf.objects.filter(conference=conftopas, status=1)
        # Query against the full list to return a list of objects
        #list1.extend(list2)

        item_list.extend([peopleall.filter(user=item['user']).values_list('user',flat=True).first() for item in
                     peopleall.values('user').distinct()])

        #print('item',item_list)#attention c'est des querysets donc set fonctionne pas, mettre .values_list('user',flat=True)
        peopleallevensubm = RegisterConf.objects.filter(conference=conftopas)
        # Query against the full list to return a list of objects
        item_listevensubm.extend([peopleallevensubm.filter(user=item['user']).values_list('user',flat=True).first() for item in
                             peopleallevensubm.values('user').distinct()])
        #nbpartsevensubm += len(item_listevensubm)

        #talks or posters
        talks = RegisterConf.objects.filter(conference=conftopas, type__in=[1, 2, 3, 4, 6])

        #print('joe')
        for ta in talks:
            talksorposters.append(ta.user)

        # number of attendance only (no poster, no talk)
        attonly = RegisterConf.objects.filter(conference=conftopas, type=5)

        for atto in attonly:
            attendance.append(atto.user)

        talksac = RegisterConf.objects.filter(conference=conftopas, status=1, type__in=[1, 2, 3, 4, 6])

        #print('joe2')

        for tac in talksac:
            talksorpostersacc.append(tac.user)

        attonlyacc = RegisterConf.objects.filter(conference=conftopas, status=1, type=5)

        #print('joe3')

        for attoacc in attonlyacc:
            attendanceacc.append(attoacc.user)

        # number of attendance only (no poster, no talk)
        attonlynonac = RegisterConf.objects.filter(conference=conftopas, status=0, type=5)

        #print('joe4')

        for attnon in attonlynonac:
            attonlynonacc.append(attnon.user)

    difflistatto = list(set(attendance) - set(talksorposters))

    myset3 = set(difflistatto)
    #print('myset3',myset3,len(myset3))
    natt = len(myset3)

    difflistattononacc = list(set(attonlynonacc) - set(talksorpostersacc) - set(attendanceacc))

    myset4 = set(difflistattononacc)
    # print('myset',myset,len(myset))
    nattnonacc = len(myset4)

    myset = set(item_list)
    #print('myset',myset,len(myset))
    nbparts = len(myset)

    #print('joe5')

    myset2 = set(item_listevensubm)
    # print(myset,len(myset))
    nbpartsevensubm = len(myset2)
    oldvote = 0
    newpos = ''
    oldvote2 = 0
    newpos2 = ''
    oldview=0
    oldview2=0
    for conftopas in allconf:

        talks = RegisterConf.objects.filter(conference=conftopas, status=1, type__in=[1, 2, 3, 6])
        usert = []
        for t in talks:
            usert.append(t.user)

        nbtalks += talks.count()



        # Number of recorded videos: (if rec)
        visio = CreateVisio.objects.filter(conference=conftopas, testroom=False)
        # getnumberofdays = abs(end - start).days + 1

        #if visio.exists():
            #headers = {'authorization': 'Bearer %s' % my_app.utils.generateToken(),
            #           'content-type': 'application/json'}

            #conn = http.client.HTTPSConnection("api.zoom.us")

        for iu in visio:
            # total number hours of zoom
            # print('iu',iu.duration,iu.duration/60.)
            if iu.duration != 1:
                nbhourzoom += iu.duration / 60.
            if iu.idconf:
                # number of people on zoom  https: // marketplace.zoom.us / docs / api - reference / zoom - api / reports / reportmeetingparticipants < / li >

                # import http.client

                # conn.request("GET", "/v2/users?page_size=300&status=active", headers=headers)
                if 1 == 0:
                    print('nada')
                    '''
                    pagesize = 300
                    conn.request("GET", "/v2/report/meetings/" + str(iu.idconf) + "/participants?page_size=" + str(
                        pagesize), headers=headers)

                    res = conn.getresponse()
                    data = res.read()

                    if res.status == 200:
                        nbpages = json.loads(data)['page_count']
                        nbparttot += json.loads(data)['total_records']
                        # print('decode', data.decode("utf-8"), nbpersons, nbpages)

                        participantnames = []
                        # nloop = min(pagesize, nbpersons)

                        for page in range(nbpages):
                            # print('p', page)
                            nextpagetoken = json.loads(data)['next_page_token']
                            # print('next', nextpagetoken)

                            nloop = len(json.loads(data)['participants'])
                            for nb in range(nloop):
                                participantnames.append(json.loads(data)['participants'][nb]['name'])
                                # print('name',json.loads(data)['participants'][nb]['name'])

                            conn.request("GET",
                                         "/v2/report/meetings/" + str(iu.idconf) + "/participants?page_size=" + str(
                                             pagesize) + "&next_page_token=" + nextpagetoken, headers=headers)
                            res = conn.getresponse()
                            data = res.read()

                        # get number of unique participants names
                        if participantnames:
                            myset = set(participantnames)
                            # print(myset,len(myset))
                            nbpart += len(myset)
                    '''
            if iu.vimeo_url:
                # print('iu',iu.vimeo_url,len(iu.vimeo_url))#should count number of '
                # print('gh',iu.vimeo_url.count("'"))#ca marche
                countv += int(iu.vimeo_url.count("'") / 2.)
                countvview += 1
                taskid3 = iu.vimeo_url.replace('[', '').replace(']', '').replace("'", '').replace(" ", "")
                arr2 = taskid3.split(',')
                # print('arr2',arr2)

                if 1 == 0:
                    import vimeo

                    client = vimeo.VimeoClient(
                        token='ad1e934c05fe16362aebbeac14a3bee6',
                        key='a8c8c13e49a86bb01b1c1f398a3e94b38f4e5552',
                        secret='uQXvpT0/yisn3GCfmmJMa53sWtVmTKA6RHgbNOAFymlaiiBfbwPE0vmAvpEBHfz19/oG2BiKQkFlcvgnmatka+/P+VbwvoZYrgTgYN1zLlejcyGUrKlL3kybWoxHbG8F'
                    )

                    # response = client.get('/me')  # ,params={"fields": "uri"})
                    # print('ffnkjvndfkjvndfkjvbndfkj', response.json())
                    # https: // api.vimeo.com / videos?links = https: // vimeo.com / 74648232, https: // vimeo.com / 232323497

                    # stats.plays=how many time viewed
                    # duration=how long

                    for i in range(len(arr2)):
                        redvimurl = arr2[i].split('/')[2]

                        response = client.get('/videos/' + redvimurl,
                                              params={"fields": "uri,status,duration,stats"})
                        # response = client.get('/videos?uris='+visio[i].vimeo_url+'&fields=uri,link,name,description')#,params={"fields": "uri"})

                        if response.status_code == 200:
                            # print('ffnkjvndfkjvndfkjvbndfkj2', redvimurl, response.json())
                            # print('ffnkjv', response.json()['status'])

                            # videostatus = response.json()['status']
                            videodur = response.json()['duration']  # in seconds
                            videonbvie = response.json()['stats']
                            videonbview = videonbvie['plays']
                            # print('oooo',videonbvie,videonbview)
                            countvview += videonbview
                            countvduration += videodur / 60. / 60.  # in hour

                    # print('vidstat',videostatus)
                    # print('viddur',videodur)
                    # print('vidnbview',videonbview)
        countvview = int(countvview)
        countvduration = round(countvduration, 2)
        nbhourzoom = round(nbhourzoom, 1)
        # Number of hours videos watched

        # number of chat rooms

        # print('ok3')

        posters = RegisterConf.objects.filter(conference=conftopas, status=1, type=4)

        if 1 == 1:
            with sessions.Session() as session2:
                # log-in

                try:
                    rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                        server_url='https://chat.carbonfreeconf.com', session=session2)
                except:
                    # time.sleep(20)
                    # rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                    # server_url='https://chat.carbonfreeconf.com', session=session2)
                    subject = "Nooooooooo Rocket chat what????"
                    message = "Oups <strong>Rocket chat</strong> fait de la merde!!!!"
                    # message+="<img src='https://bucketeer-83011bf8-623d-4ad2-8e34-40829bae363d.s3.amazonaws.com/static/images/carbonfreeconf_logo_title.svg' width='200' height='60' alt='Make my own CarbonFreeConf workshop'>"

                    emailto = []
                    emailto.append("quentin.kral@gmail.com")
                    emailto.append("carbonfreeconf@gmail.com")

                    email = EmailMessage(
                        subject,
                        message,
                        'CarbonFreeConf <conference@carbonfreeconf.com>',  # from
                        emailto,  # to
                        # getemails,  # bcc
                        # reply_to=replylist,
                        headers={'Message-From': 'www.carbonfreeconf.com'},
                    )
                    email.content_subtype = "html"

                    email.send(fail_silently=False)

                slugtitleconf = slugify(str('%s' % (conftopas.title)))
                slugtitleconforg = slugify(str('%s' % ('organization of ' + conftopas.title)))

                # create room for organizers
                slugtitleconfcafe = slugify(str('%s' % ('Coffee break for ' + conftopas.title)))
                contentroom = rocket.groups_info(room_name=slugtitleconf).json()
                # print('c', contentroom)

                if contentroom['success'] == True:
                    nbroom += 1
                    keyroom = contentroom['group']['_id']
                    # print('keyroom',keyroom)
                    channelmess = rocket.groups_history(room_id=keyroom).json()
                    # channelmess = rocket.channels_history(room_name=slugtitleconf).json()
                    nbmes += len(channelmess['messages'])
                    # print('channelmess',len(channelmess['messages']))

                contentroomo = rocket.groups_info(room_name=slugtitleconforg).json()
                # print('c', contentroom)
                if contentroomo['success'] == True:
                    nbroom += 1
                    keyroomo = contentroomo['group']['_id']
                    # print('keyroomo', keyroomo)
                    channelmesso = rocket.groups_history(room_id=keyroomo).json()
                    # print('channelmesso', channelmesso)
                    nbmes += len(channelmesso['messages'])
                    # print('channelmesso', len(channelmesso['messages']))

                contentroomc = rocket.groups_info(room_name=slugtitleconfcafe).json()
                # print('c', contentroom)
                if contentroomc['success'] == True:
                    nbroom += 1
                    keyroomc = contentroomc['group']['_id']
                    # print('keyroomc', keyroomc)
                    channelmessc = rocket.groups_history(room_id=keyroomc).json()
                    # print('channelmessc', channelmessc)
                    nbmes += len(channelmessc['messages'])
                    # print('channelmessc', len(channelmessc['messages']))
                # print('slug', slugtitleconf)
                # list = rocket.groups_list_all().json()
                # print('l', list)
                # pprint(rocket.groups_info(room_name=slugtitleconf).json())
                # contentroom = rocket.groups_info(room_name=slugtitleconf).json()
                # print('c', contentroom)
                # if contentroom['success'] == True:
                #    keyroom = contentroom['group']['_id']

                #    contentuser = rocket.users_info(username=user.username).json()
                #    key = contentuser['user']['_id']
                # print('keyo',key,keyroom)

                canalconf = ChatCanal.objects.filter(conference=conftopas)
                if canalconf:
                    nbextracanal = canalconf.count()
                    nbroom += nbextracanal
                    for c in canalconf:
                        slugtitleconfextra = slugify(str('%s' % (conftopas.title + '-' + c.titleg)))
                        contentroome = rocket.groups_info(room_name=slugtitleconfextra).json()
                        # print('c', contentroom)

                        if contentroome['success'] == True:
                            keyroome = contentroome['group']['_id']
                            # print('keyroome', keyroome)
                            channelmesse = rocket.groups_history(room_id=keyroome).json()
                            # channelmess = rocket.channels_history(room_name=slugtitleconf).json()
                            # print('channelmesse', channelmesse['messages'])
                            nbmes += len(channelmesse['messages'])
                            # print('channelmesse', len(channelmesse['messages']))
                # number discussion on chat about posters
                for po in posters:

                    slugtitleconfposter = slugify(str('%s' % (
                            'poster_' + po.user.first_name + ' ' + po.user.last_name + '_' + po.title)))
                    contentroompo = rocket.groups_info(room_name=slugtitleconfposter).json()
                    # print('c', contentroom)

                    if contentroompo['success'] == True:
                        keyroompo = contentroompo['group']['_id']
                        # print('keyroom',keyroom)
                        channelmesspo = rocket.groups_history(room_id=keyroompo).json()
                        # channelmess = rocket.channels_history(room_name=slugtitleconf).json()
                        nbmespo += len(channelmesspo['messages'])
            # number of posters
            # print('ok4')

        userp = []


        for p in posters:
            userp.append(p.user)
            nbviewp+=PosterView.objects.filter(poster=p).count()
            view = PosterView.objects.filter(poster=p).count()

            if view > oldview:
                oldvote2 = p.votes.count()
                newpos2 = p
                newposview2 = view
                oldview=view

            vote = p.votes.count()
            if vote > oldvote:
                oldvote = vote
                newpos = p
                newposview = view

        #statmaster.bestposter = newpos
        #statmaster.votes = oldvote
        #statmaster.view = newposview
        #votes = models.IntegerField(null=True, blank=True)
        #view = models.IntegerField(null=True, blank=True)
        #bestposter = models.ForeignKey(RegisterConf, on_delete=models.CASCADE, blank=True, null=True)

        nbposters+=posters.count()



        # Number of posts, engagements and impressions on twitter tagging# ...
        '''
        if 1 == 0:  # too long to reply
            api = my_app.utils.startapi()

            # removehashtag = conftopass.twitterhashtag.split('#')
            # tweet_user = []
            # tweet_screenuser = []
            # tweet_text = []
            # tweet_image = []
            # tweet_id = []
            # tweet_date = []
            # tweet_retweet = []
            # tweet_retweetcount = []
            # tweet_count = 0

            if conftopas.twitterhashtag not in hashtagused:
                query = conftopas.twitterhashtag  # '#science'
                hashtagused.append(conftopas.twitterhashtag)

                apirateexc = False
                if query != '#':
                    max_tweets = 10  # 1000
                    try:
                        searched_tweets = [status for status in
                                           tweepy.Cursor(api.search, q=query, include_entities=True,
                                                         tweet_mode="extended").items(max_tweets)]
                    except:
                        apirateexc = True
                        # print('except')
                    # searched_tweets2 = [status for status in tweepy.Cursor(api.search, q=query, include_entities=False).items(max_tweets)]

                    if apirateexc == False:
                        # for tweet in api.search(q="carbon-neutral",rpp=25):#conftopass[0].twitterhashtag):
                        # print('searched tweets',len(searched_tweets))
                        nbposts += len(searched_tweets)
                        if len(searched_tweets) == max_tweets:
                            sup = True

                    else:
                        nbposts = "We couldn't get the value, try again later"

        # print('ok5')
    if sup == True:
        nbposts = '>' + str(nbposts)
    else:
        nbposts = str(nbposts)
        '''

    #nbparts = len(item_list)

    statmaster.nbpartsm=nbparts
    statmaster.nbpartsevensubmm=nbpartsevensubm
    statmaster.CO2m=CO2
    statmaster.nbtalksm=nbtalks
    statmaster.bestposter=newpos
    statmaster.votes=oldvote
    statmaster.view=newposview
    statmaster.bestposter2 = newpos2
    statmaster.votes2 = oldvote2
    statmaster.view2 = newposview2
    statmaster.nbdiffm=nbdiff
    statmaster.diffemails=diffemails
    statmaster.nbattonlym=natt
    statmaster.nbattonlynonaccm=nattnonacc
    statmaster.nbpostersm=nbposters
    statmaster.nbviewpm=nbviewp
    statmaster.countvm=countv
    statmaster.nbroomm=nbroom
    statmaster.nbmesm=nbmes
    statmaster.nbmespom=nbmespo
    statmaster.nbhourzoomm=nbhourzoom
    statmaster.timeoverm=timeover
    statmaster.countvviewm=countvview
    statmaster.countvdurationm=countvduration
    statmaster.nbpostsm=nbposts
    statmaster.nbpartm=nbpart
    statmaster.nbparttotm=nbparttot

    statmaster.finished = True
    statmaster.save()

    return "done"