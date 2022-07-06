from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from django.core.mail import EmailMessage
#from . import utils#updateratesautomatically
import django
from requests import sessions
from rocketchat_API.rocketchat import RocketChat

#django.setup()

# Lets the celery command line program know where project settings are.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Creates the instance of the Celery app.
app = Celery('conf',broker=settings.BROKER_URL)
#app = Celery('file_upload', broker_pool_limit=1, broker=redis_url, result_backend=redis_url)


#app.config_from_object('django.conf:setting')
# app.config_from_object('django.conf:settings', namespace='CELERY')


# Set up autodiscovery of tasks in the INSTALLED_APPS.
#app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

django.setup()

from djmoney.contrib.exchange.backends import OpenExchangeRatesBackend


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

#@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds. It works...
    sender.add_periodic_task(36000., update_rates.s(), name='every 10 hr')
    #sender.add_periodic_task(1440., test.s('what?'), name='every day')
    sender.add_periodic_task(600., sendemail.s('carbonfreeconf@gmail.com'), name='every 10 mins')

#    sender.add_periodic_task(21600., update_rates.s(), name='every 6 hours')

    # Executes every day at 12h10 UTC, it works...if needed
    #sender.add_periodic_task(crontab(hour=12, minute=00),update_rates.s(),name='update rates')
    #sender.add_periodic_task(crontab(hour=12, minute=10),sendemail.s('quentin.kral@gmail.com'),name='brah')

@app.task
def test(arg):
    print(arg)
    from conf.tasks import test
    test(arg)

@app.task
def update_rates():
    #backend = import_string(backend)()
    OpenExchangeRatesBackend().update_rates()#pas sur que ca marche car je peux pas importer...
    #updateratesautomatically()

@app.task
def sendemail(emailtothem):#email if rocket chat down
    with sessions.Session() as session:
        try:
            rocket = RocketChat('carbonfreeconf', settings.SECRETROCK,
                                server_url='https://chat.carbonfreeconf.com',
                                session=session)
        except:
            emailto = []
            emailto.append(emailtothem)
            email = EmailMessage(
                'from celery',
                'crazy <b>ducky</b>',
                'CarbonFreeConf <conference@carbonfreeconf.com>',  # from
                emailto,  # to
                # getemails,  # bcc
                # reply_to=replylist,
                headers={'Message-From': 'www.carbonfreeconf.com'},
            )
            email.content_subtype = "html"

            email.send(fail_silently=False)

if __name__ == '__main__':
    app.start()