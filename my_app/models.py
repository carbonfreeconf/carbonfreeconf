from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from .search import PostIndex, ConfIndex
#from multiselectfield import MultiSelectField
#from cloudinary_storage.storage import RawMediaCloudinaryStorage
from conf.storage_backends import PrivateMediaStorage, PublicMediaStorage
from djmoney.models.fields import MoneyField
from vote.models import VoteModel
from colorfield.fields import ColorField
from django.utils.timezone import now
import os
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

#check
# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    orcid = models.CharField(max_length=19, verbose_name=_('Orcid ID'), blank=True)
    institute = models.TextField(verbose_name=_('Institute/Company'), null=True, max_length=200)
    profile_pic = models.ImageField(upload_to='static/profilepic/',blank=True,verbose_name='',storage=PublicMediaStorage())
    remember_me = models.BooleanField(blank=True)
    instcountry=models.CharField(_('Country of Institute/Company'),max_length=200,null=True)
    isinconf = models.BooleanField(blank=True, default=False)
    job = models.CharField(_('Your job title'),max_length=50,blank=True,null=True)#,
    customerid = models.CharField(max_length=200,null=True,blank=True)
    iban=models.CharField(max_length=50,null=True,blank=True, verbose_name='IBAN')
    accountnumber=models.CharField(_('Account number'),max_length=50,null=True,blank=True)
    rootingnumber=models.CharField(_('Rooting number'),max_length=50,null=True,blank=True)
    bicswiftcode=models.CharField(_('BIC/Swift code'),max_length=50,null=True,blank=True)
    sortcode=models.CharField(_('Sort code'),max_length=50,null=True,blank=True)
    bankcountry=models.CharField(_('Country'),max_length=200,null=True,blank=True)
    bankusername=models.CharField(_('Name of bank account owner (you or your institute)'),max_length=300,null=True,blank=True)
    codeactive = models.CharField(max_length=50,default="", blank=True)#,
    forgotpass = models.CharField(max_length=50,default="", blank=True)#,
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class CreateConf(models.Model):
    #class Meta():
    title = models.CharField(_('Conference title'),max_length=300)
    title_extra = models.CharField(max_length=10,null=True,blank=True)
    abstract = models.TextField(_('Conference abstract'),max_length=3000)
    messagetoall = models.TextField(_('Message to all participants'),max_length=500,null=True,blank=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'),null=True)
    closing_date = models.DateField(_('Closing date'),null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #idconf = models.CharField(max_length=30,null=True)
    #recidconf = models.CharField(max_length=30,null=True,blank=True)
    #mp4_url = models.CharField(max_length=100,null=True,blank=True)
    submitparticipations = models.BooleanField(_('Can the participants submit presentations?'),default=True)
    activateqandp = models.BooleanField(_('Activate the questions and polls during the conference?'),default=True)
    finishimport = models.BooleanField(default=False)
    masterconf = models.BooleanField(_('Are you creating the master conference?'),default=False)
    acceptconf = models.BooleanField(default=False)
    daughterconf = models.BooleanField(_('Or are you creating a session for a master conference that has already been created?'),default=False)
    masterconfpass = models.IntegerField(_('What is the ID of the master conference?'),null=True,blank=True)
    minleft = models.IntegerField(default=0,null=True,blank=True)
    minleftid = models.IntegerField(default=0,null=True,blank=True)
    minleftcreated = models.DateTimeField(blank=True,null=True)
    minleftuserfln = models.CharField(max_length=300,blank=True,null=True)
    masterconfidfordaughter = models.IntegerField(null=True,blank=True)#master conf id for daughter conferences
    masterconfdaughterposition = models.IntegerField(null=True,blank=True)#master conf id for daughter conferences
    masterconfdaughtername = models.CharField(max_length=200,blank=True)#master conf id for daughter conferences
    daughterconfstarwars = models.BooleanField(_("Do you want the daughter conferences to be named using some of the famous Star wars planets' names?"), default=False)
    subtomastautomatic = models.BooleanField(_("Should participants be automatically added to the master session (plenaries) when they get a participation accepted?"),default=False)
    coffeebreak = models.BooleanField(_("Add a coffee break parallel room that is always accessible?"),default=True)
    coffeebreakgames = models.BooleanField(_("Add games in the coffee break room?"),default=True)
    payingatonce = models.BooleanField(_('Is the payment centralized to the master conference (or each session should pay on their own)?'),default=False)
    STATUS = (
        (0, "Draft"),
        (1, "Published"),
        (2, "Paid"),
    )

    status = models.IntegerField(choices=STATUS, default=0)


    ASTRO = "Astrophysics"
    MATH = "Mathematics"
    PHY = "Physics"
    BIO = "Biology"
    MED = "Medicine"
    INFO = "Informatics"
    STAT = "Statistics"
    OTHER = "Other"

    # (...)

    SUBJECT_CHOICES = (
        (ASTRO, "Astrophysics"),
        (MATH, "Mathematics"),
        (PHY, "Physics"),
        (BIO, "Biology"),
        (MED, "Medicine"),
        (INFO, "Informatics"),
        (STAT, "Statistics"),
        (OTHER, "Other"),

    )

    subject = models.CharField(_('Conference subject'), max_length=100,default="")#,
                             #choices=SUBJECT_CHOICES,
                             #default="Astrophysics", verbose_name='Conference subject')

    VERYSMALL = "<10"
    SMALL = "10-50"
    NORMAL = "50-100"
    LARGE = "100-300"
    VERYLARGE = "300-500"
    VERYVERYLARGE = "500-1000"

    # (...)

    SIZE_CHOICES = (
        (VERYSMALL, "<10 people"),
        (SMALL, "10-50 people"),
        (NORMAL, "50-100 people"),
        (LARGE, "100-300 people"),
        (VERYLARGE, "300-500 people"),
        (VERYVERYLARGE, "500-1000 people"),
    )

    EUR = "Euros"
    USD = "US Dollars"
    GBP = "GB Pounds"

    CURRENCY_CHOICES = (
        (EUR, "Euros"),
        (USD, "US Dollars"),
        (GBP, "GB Pounds"),
    )

    PUB="Public"
    PRIV="Private"

    PRIV_CHOICES = (
        (PUB, "Public"),
        (PRIV, "Private"),
    )

    fee = models.BooleanField(_('Pay the conferences fees but get money back from participants?'),default=False)
    fee_amount = models.FloatField(_('Fee they must pay'), null=True,blank=True,default=0.)
    fee_currency = models.CharField(_('In which currency?'), max_length=15,choices=CURRENCY_CHOICES,default=EUR)
    fee_to_carbon = models.BooleanField(_('Should the fees collected be used by us to offset more carbon emissions? (or paid to you?, in this case do not check the box)'),default=False)
    fee_variable = models.BooleanField(_('Participants can give what they want'), default=False)
    feeunique = models.BooleanField(_('Share the conference fees between everyone by choosing a unique fee per person (it includes everything such as technical support and we also offset the carbon emissions)'), default=False)
    fee_currency_unique = models.CharField(_('Choose the currency of most participants that will be proposed by default'), max_length=15,choices=CURRENCY_CHOICES,default=EUR)
    fee_amount_unique = models.FloatField(null=True,blank=True,default=0.)
    justtools = models.BooleanField(_('We will just use the CarbonFreeConf organizing tools for free (e.g. abstract management, website creation, participant and program handling, ...) but not run the actual conference with the CarbonFreeConf video conferencing tools'), default=False)


    size = models.CharField(_('Conference size'),max_length=9,
                             choices=SIZE_CHOICES,
                             default=NORMAL)

    priv = models.CharField(_('Public or private conference?'),max_length=9,
                            choices=PRIV_CHOICES,
                            default=PRIV)
    privpass = models.CharField(max_length=50,default="", blank=True)#,
    fastpass = models.CharField(max_length=50,default="", blank=True)#,

    #data={"channel_id": "q425296", "title": "Conference title","start_time": "2020-03-09 14:10"}

    #PUB = "public"
    #PRIV = "private"

    #PRIVACY_CHOICES = (
    #    (PUB, "public"),
    #    (PRIV, "private"),
    #@)

    poster = models.BooleanField(_('Are posters allowed?'),default=False)

    dialin = models.BooleanField(_('Enable dial-in?'), default=False)
    dialin_number = models.CharField(max_length=30, blank=True, null=True)
    dialin_id = models.CharField(max_length=30, blank=True, null=True)
    dialin_passcode = models.CharField(max_length=30, blank=True, null=True)
    dialin_passcode_presenter = models.CharField(max_length=30, blank=True, null=True)

    parsession = models.BooleanField(_('Participants can access to all parallel sessions?'), default=True)

    recording = models.BooleanField(_('Record the conference?'), default=False)
    proceedin = models.BooleanField(_('Presenters must write proceedings after the conference?'), default=False)
    hybrid = models.BooleanField(_('Is the conference hybrid (i.e. both face-to-face and virtual)?'), default=False)

    ANY = "Everyone"
    MEMB = "Only conference participants"
    #PRIV = "Only through a private link"

    WHO_CHOICES = (
        (ANY, "Everyone"),
        (MEMB, "Only conference participants"),
        #(PRIV, "Only through a private link"),
    )

    whorecording = models.CharField(_('Who can see the recording?'), max_length=50,
                               choices=WHO_CHOICES,
                               default=ANY)
    youtuberecording = models.BooleanField(_('Put the recording on youtube?'), default=False)
    room_logo = models.ImageField(upload_to='static/logos/',blank=True, null=True, verbose_name='',storage=PublicMediaStorage())
    background = models.ImageField(upload_to='static/back/',blank=True, null=True, verbose_name='',storage=PublicMediaStorage())
    twitterhashtag = models.CharField(_('Twitter Hashtag'),max_length=300, default="#CarbonFreeConf")

    ZOOM="Zoom"
    BM="Big Marker"
    ROOM_CHOICES = (
        (ZOOM, "Zoom"),
        (BM, "Big Marker"),
    )
    roomtype = models.CharField(_('Which virtual room you want?'), max_length=50,
                                    choices=ROOM_CHOICES,
                                    default=ZOOM)



    def __str__(self):
        return self.title

    if 'ON_HEROKU' in os.environ:
      def indexing(self):
          #obj = PostIndex(meta={'id': self.id}, content=self.content)
          obj = ConfIndex(meta={'id': self.id}, user=self.user.username,start_date=self.start_date,
                          end_date=self.end_date, title=self.title, abstract=self.abstract,
                          subject=self.subject,poster=self.poster,recording=self.recording)
          #obj = ConfIndex(meta={'id': self.id}, user=self.user.username, start_date=self.start_date,
          #               end_date=self.end_date, title=self.title, abstract=self.abstract)
          obj.save()

          return obj.to_dict(include_meta=True)

class CreateQuestion(VoteModel,models.Model):
    question = models.TextField(null=True)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(_('Anonymous?'), default=False)
    active = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)

    def __str__(self):
        return self.question

class CreatePoll(models.Model):
    question = models.TextField(null=True,verbose_name='Question')
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updateactive = models.DateTimeField(null=True,blank=True)
    change = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(_('Anonymous?'), default=False)
    pollimage = models.ImageField(upload_to='static/pollimages/',blank=True, null=True, verbose_name='',storage=PublicMediaStorage())
    active = models.BooleanField(default=False)
    activedonce = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    showres = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class ChoicePoll(VoteModel,models.Model):
    created = models.DateTimeField(auto_now_add=True)
    poll = models.ForeignKey(CreatePoll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=2000)

    def __str__(self):
        return self.poll.question+':'+self.choice_text

class CreateVisio(models.Model):
    idconf = models.CharField(max_length=30,null=True)
    idconfcb = models.CharField(max_length=30,null=True)
    recidconf = models.TextField(null=True,blank=True)
    mp4_url = models.TextField(null=True,blank=True)
    mp4_id = models.TextField(null=True,blank=True)
    vimeo_url = models.TextField(null=True,blank=True)
    recstart = models.TextField(null=True,blank=True)
    recend = models.TextField(null=True,blank=True)
    rectitles = models.TextField(null=True,blank=True)
    rights = models.TextField(null=True,blank=True)#"anybody","disable","nobody"
    passzoom = models.CharField(max_length=50,null=True,blank=True)
    passzoomcb = models.CharField(max_length=50,null=True,blank=True)
    zoomcreator = models.CharField(max_length=500,null=True,blank=True)
    zoomcreatorcb = models.CharField(max_length=500,null=True,blank=True)
    starturlzoom = models.TextField(null=True,blank=True)
    joinurlzoom = models.TextField(null=True,blank=True)
    starturlzoomcb = models.TextField(null=True, blank=True)
    joinurlzoomcb = models.TextField(null=True, blank=True)
    celery_task_id = models.TextField(null=True,blank=True)
    date = models.DateTimeField()
    duration = models.IntegerField(blank=True,null=True)#in minutes
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    testroom = models.BooleanField(default=False)
    expirytime = models.DateTimeField(blank=True,null=True)
    celery_task_id_fin = models.CharField(max_length=400,null=True,blank=True)
    celery_task_id_fin_cb = models.CharField(max_length=400,null=True,blank=True)

    def __str__(self):
        return self.conference.title

class People(models.Model):
    firstname = models.CharField(max_length=200,blank=False)
    lastname = models.CharField(max_length=200,blank=False)
    email = models.EmailField(max_length=256,blank=False,error_messages={'required': 'Please provide your email address.'},)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)#onetoone plutot, non?
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    def __str__(self):
        return self.email

class ProgramDesign(models.Model):
    timestart = models.IntegerField(_('Start time of schedule span'), default=0)
    timefinish = models.IntegerField(_('End time of schedule span'), default=24)
    mineventheight = models.IntegerField(_('Minimum height of schedule boxes'), default=100)
    heighthr = models.IntegerField(_('Height for each hour slot'), default=2)
    minieventtime = models.IntegerField(_('Under how many minutes does it switch to the mini format?'), default=10)
    opacity = models.IntegerField(_('Opacity of the boxes'), default=10)
    #start_time = models.TimeField(blank=False, null=False, help_text="Start time (00:00 format)")
    #end_time = models.TimeField(blank=False, null=False, help_text="End time (00:00 format)")
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    def __str__(self):
        return self.conference.title

class Schedule(models.Model):
    text = models.CharField(max_length=200)
    abstract = models.TextField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    speaker = models.CharField(max_length=200, null=True)
    important = models.BooleanField(null=True)
    notpart = models.BooleanField(null=True,default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    rand = models.IntegerField(null=True)

    #TALK = "Talk"
    #DISC = "Discussion"
    #INVTALK = "Invited Talk"
    #REV = "Review"


    TYPE = (
        (6, "Talk"),
        (1, "Invited Talk"),
        (2, "Discussion"),
        (3, "Review"),
        (4, "Poster"),
        (5, "Attendance only"),
        (7, "Pause"),
    )
    type = models.IntegerField(choices=TYPE, default=6, verbose_name='Oral type')

    #type = models.CharField(max_length=15,
     #                       choices=TYPE_CHOICES,
      #                      default="Talk", verbose_name='Oral type')

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.text


class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='my_app_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('my_app:post_detail',
                       args=[str(self.slug)])

    if 'ON_HEROKU' in os.environ:
      def indexing(self):
          #obj = PostIndex(meta={'id': self.id}, content=self.content)
          obj = PostIndex(meta={'id': self.id}, author=self.author.username, slug=self.slug, created_on=self.created_on, title=self.title, title_suggest=self.title, content=self.content)
          obj.save()

          return obj.to_dict(include_meta=True)

class HeroPicture(models.Model):
    heroimages = models.ImageField(upload_to='static/heroimages/', blank=True, null=True, verbose_name='',storage=PublicMediaStorage())
    heroname = models.CharField(_("Name of hero image"),max_length=70,blank=True,null=True)

    def __str__(self):
        return str(self.heroname)


class Website(models.Model):
    #title = models.CharField(max_length=200, unique=True)
    #slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    homecontent = models.TextField(_('Text for the homepage'))
    rationale = models.TextField(_('Rationale of your conference'),)
    hero = models.ForeignKey(HeroPicture, on_delete = models.SET_NULL, null = True,blank=True, verbose_name='Hero image')
    guidelines = models.TextField(_('Guidelines for your participants'))
    created_on = models.DateTimeField(auto_now_add=True)
    conference = models.OneToOneField(CreateConf, on_delete=models.CASCADE)
    #slug = models.SlugField(max_length=200, unique=True)
    titleurl = models.CharField(_("Enter your website's url"),max_length=30,blank=True,null=True)
    showprogram = models.BooleanField(_('Program and Timeline ready to be displayed on the conference website?'), default=False)
    showdoc = models.BooleanField(_('Show a page with conference documents (slides/posters/papers)?'), default=False)
    onlypprogram = models.BooleanField(_('Program and Timeline showed only to validated participants?'), default=False)
    onlypabstract = models.BooleanField(_('Abstracts showed only to validated participants?'), default=False)
    onlypposter = models.BooleanField(_('Posters showed only to validated participants?'), default=False)
    onlypdoc = models.BooleanField(_('Documents only accessible to validated participants?'), default=False)
    color_background = ColorField(_('Background color on the conference website'), default='#223')
    color_men = ColorField(_('Menu color on the conference website'), default='#888888')
    color_text = ColorField(_('Text color on the conference website'), default='#fff')
    share = models.BooleanField(_('Show the twitter and facebook share buttons at the bottom of the conference website?'), default=False)

    def __str__(self):
        return str(self.conference.title)

    def get_absolute_url(self):
        return reverse('my_app:website',
                       args=[self.id,'home'])

    #def indexing(self):
        #obj = PostIndex(meta={'id': self.id}, content=self.content)
        #obj = PostIndex(meta={'id': self.id}, author=self.author.username, slug=self.slug, created_on=self.created_on, title=self.title, title_suggest=self.title, content=self.content)
        #obj.save()

        #return obj.to_dict(include_meta=True)


class RegisterConf(VoteModel,models.Model):
    #class Meta():
    title = models.CharField(max_length=500, verbose_name='Title',blank=True)
    abstract = models.TextField(_('Abstract'),blank=True,null=True)
    biography = models.TextField(_('Tell the organizers about you'),blank=True,null=True)
    facetoface = models.BooleanField(_('It is an hybrid conference. Will you come in person to the conference? (if you assist virtually do not tick the box)'),default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    slides = models.FileField(upload_to='static/slides/',blank=True, null=True, verbose_name='',storage=PublicMediaStorage())#,storage=RawMediaCloudinaryStorage())
    slidesid = models.CharField(max_length=300,blank=True, null=True)
    slideshow = models.BooleanField(default=False)
    paperurl = models.URLField(max_length = 300,blank=True, verbose_name='')
    haspaid = models.BooleanField(null=True,default=False)
    free = models.BooleanField(null=True,default=False)
    rectalk = models.BooleanField(null=True,default=False)
    idconf = models.CharField(max_length=30, null=True, blank=True)
    recid = models.CharField(max_length=300,blank=True, null=True)
    recidconf = models.CharField(max_length=100, null=True, blank=True)
    mp4_url = models.CharField(max_length=400, null=True, blank=True)
    mp4show = models.BooleanField(default=False)
    mp4_url_bm = models.CharField(max_length=400, null=True, blank=True)
    poster_invite_chat_url = models.CharField(max_length=400, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    testvirtualroom = models.BooleanField(null=True,default=False)
    idconftest = models.CharField(max_length=30, null=True, blank=True)
    datetest = models.DateTimeField(null=True, blank=True)

    STATUS = (
        (0, "Submitted"),
        (1, "Accepted"),
        (2, "Other"),
    )

    status = models.IntegerField(choices=STATUS, default=0)

    TYPE = (
        (6, "Talk"),
        (1, "Invited Talk"),
        (2, "Discussion"),
        (3, "Review"),
        (4, "Poster"),
        (5, "Attendance only"),
    )

    type = models.IntegerField(choices=TYPE, default=6, verbose_name='Participation type')

    ROLE = (
        (0, "Presenter"),
        (1, "Moderator"),
        (2, "Attendee"),
        (3, "Superuser")
    )

    role = models.IntegerField(choices=ROLE, default=0)

    SOCLOC = (
        (0, "Not an organizer/decision panel member"),
        (1, "Program committee member"),
        (2, "Organizer"),
    )

    socloc = models.IntegerField(choices=SOCLOC, default=0)

    def __str__(self):
        return self.user.email

class MinLeftModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    minleftidu = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.user.username+' '+self.conference.title+' ')+str(self.minleftidu)


class UserUpdateL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    lastlogintimepanel = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.user.username+' '+self.conference.title+' ')+str(self.lastlogintimepanel)

class UserUpdateQ(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    question_last_updated = models.DateTimeField(null=True)
    poll_last_updated = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.user.username+' '+self.conference.title+' ')+str(self.question_last_updated)+str(self.poll_last_updated)

class UserLink(models.Model):
    mainuser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='mainuser')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Proceeding(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(null=True)
    texthtml = models.TextField(null=True)
    bibtex = models.TextField(null=True,blank=True, verbose_name='')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    regconf = models.ForeignKey(RegisterConf, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    def __str__(self):
        return self.title

class EmailPeople(models.Model):
    #class Meta():
    subjectt = models.CharField(_('Subject'), max_length=300)
    message = models.TextField(max_length=4000, verbose_name='Message')
    replyto = models.CharField(_('Email for people to reply to (if several, separate with commas)'),max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    whoto = models.CharField(max_length=1000)
    topersonemail = models.CharField(max_length=100,null=True)
    all = models.BooleanField(_('Send the message to participants from all sessions of the conference? (to click before the "who to" selection)'), default=False)

    #whoto = MultiSelectField(WHOTO)
    #whoto = models.IntegerField(choices=WHOTO, default=0, verbose_name='Who to?')

    def __str__(self):
        return self.subjectt

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.whoto:
            self.whoto = eval(self.whoto)

class ChatCanal(models.Model):
    titleg = models.TextField(null=True)
    description = models.TextField(null=True)
    topic = models.CharField(null=True,max_length=300)
    people = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    def __str__(self):
        return self.titleg

class PosterView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ForeignKey('RegisterConf', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now, blank=True)
    number = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

class StatsMaster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now, blank=True)
    number = models.CharField(max_length=100,blank=True)
    celery_task_id = models.TextField(null=True,blank=True)
    nbpartsm = models.IntegerField(null=True,blank=True)
    nbpartsevensubmm = models.IntegerField(null=True,blank=True)
    votes = models.IntegerField(null=True,blank=True)
    view = models.IntegerField(null=True,blank=True)
    bestposter = models.ForeignKey(RegisterConf, on_delete=models.CASCADE, blank=True, null=True,related_name="bestposter")
    votes2 = models.IntegerField(null=True, blank=True)
    view2 = models.IntegerField(null=True, blank=True)
    bestposter2 = models.ForeignKey(RegisterConf, on_delete=models.CASCADE, blank=True, null=True,related_name="postervie")
    nbattonlym = models.IntegerField(null=True,blank=True)
    nbattonlynonaccm = models.IntegerField(null=True,blank=True)
    nbtalksm = models.IntegerField(null=True,blank=True)
    nbpostersm = models.IntegerField(null=True,blank=True)
    nbviewpm = models.IntegerField(null=True,blank=True)
    countvm = models.IntegerField(null=True,blank=True)
    nbroomm = models.IntegerField(null=True,blank=True)
    nbmesm = models.IntegerField(null=True,blank=True)
    nbmespom = models.IntegerField(null=True,blank=True)
    countvviewm = models.IntegerField(null=True,blank=True)
    nbpartm = models.IntegerField(null=True,blank=True)
    nbparttotm = models.IntegerField(null=True,blank=True)
    nbpostsm = models.IntegerField(null=True,blank=True)
    nbdiffm = models.IntegerField(null=True,blank=True)
    nbhourzoomm = models.FloatField(null=True,blank=True)
    CO2m = models.FloatField(null=True,blank=True)
    countvdurationm = models.FloatField(null=True,blank=True)
    timeoverm = models.BooleanField(null=True,blank=True,default=False)
    finished = models.BooleanField(null=True,blank=True,default=False)
    diffemails = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name+' '+self.conference.title

class Transac(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(CreateConf, on_delete=models.CASCADE)
    isparticipantfee = models.BooleanField(null=True,blank=True,default=False)
    insti = models.TextField(null=True, max_length=200)
    amount = models.FloatField(null=True)
    amountprep = models.FloatField(null=True)
    amountoff = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    discountispercentage = models.BooleanField(null=True)
    coupon = models.CharField(max_length=15,null=True)
    currency = models.CharField(max_length=10,default='EUR')
    balance = MoneyField(max_digits=14, decimal_places=2, null=True, default_currency='USD')
    email = models.EmailField(max_length=256,blank=True)
    address = models.TextField(null=True)
    vat = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=300)
    zip = models.CharField(max_length=30)
    country = models.CharField(max_length=200)
    transacid = models.CharField(max_length=100, null=True)
    transacdate = models.DateTimeField(null=True)
    transaccreated = models.CharField(max_length=100, null=True)
    creditcartoken = models.CharField(max_length=100, null=True)
    validatedwebhook = models.BooleanField(null=True,blank=True,default=False)
    customerid = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.conference.title