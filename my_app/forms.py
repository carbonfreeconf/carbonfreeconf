from django import forms
from .models import UserProfileInfo, CreateConf, People, Website, RegisterConf, EmailPeople, Proceeding, CreateQuestion, ProgramDesign
from django.contrib.auth.models import User
from django.db import models
from bootstrap_datepicker_plus import DatePickerInput 
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login
from django.forms import DateInput
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from my_app.field import ListTextWidget
#from bdea.django_validators import disposable_email_validator
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.safestring import mark_safe
from colorfield.widgets import ColorWidget
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

#class EmailField(forms.EmailField):
 #   default_validators = forms.EmailField.default_validators + [disposable_email_validator]
#

import re

#regexexpr = re.compile('^[\w-]+$',re.UNICODE)
#        regex=r'(?!^[àáâãäåçèéêëìíîïðòóôõöùúûüýÿ]+$])(?=^[\w\-]+$)',
#^[A-Za-z0-9\-_]+$

class UserForm(forms.ModelForm):
    username = forms.RegexField(
        label='Username',
        max_length=150,
        regex=r'^[A-Za-z0-9\-_]+$',#regexexpr,#r'(?!^[àáâãäåçèéêëìíîïðòóôõöùúûüýÿ]+$])(?=^[\w\-]+$)',
        help_text='', )
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput(), validators=[validate_password])
    #password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    email = forms.CharField(label=_('Email'),required=True, widget=forms.EmailInput(attrs={'class': 'validate'}))
    #email = forms.EmailField(required=True)#, widget=forms.EmailInput(attrs={'class': 'validate'}))
    first_name = forms.CharField(label=_('First name'),required=True)
    last_name=forms.CharField(label=_('Last name'),required=True)

    class Meta():
        model = User
        fields = ('first_name', 'last_name','username','password','email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'last_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'username': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            # 'email': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
        }

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and User.objects.filter(username__iexact=username).exclude(email=email).exists():
            raise forms.ValidationError('This username has already been taken!')

        return username


class UpdateUserForm(forms.ModelForm):
    username = forms.RegexField(
        label='Username',
        max_length=150,
        regex=r'^[A-Za-z0-9\-_]+$',
        help_text='Required. 150 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores, no accents).', )
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput(), validators=[validate_password])
    #password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    email = forms.CharField(label=_('Email'),required=True, widget=forms.EmailInput(attrs={'class': 'validate'}))
    #email = forms.EmailField(required=True)#, widget=forms.EmailInput(attrs={'class': 'validate'}))
    first_name = forms.CharField(label=_('First name'),required=True)
    last_name=forms.CharField(label=_('Last name'),required=True)
    username = forms.CharField(label=_('Username'),widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta():
        model = User
        fields = ('username','first_name', 'last_name','password','email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'last_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'username': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            # 'email': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
        }

    def clean_email(self):
        # Get the email
        #email = self.cleaned_data.get('email')

        # Check that email is not duplicate
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        users = User.objects.filter(email__iexact=email).exclude(username__iexact=username)
        if users:
            raise forms.ValidationError('A user with that email already exists.')
        return email.lower()



class PeopleForm(forms.ModelForm):
    firstname = forms.CharField(label=_('First name'),required=True)
    lastname = forms.CharField(label=_('Last name'),required=True)
    email = forms.EmailField(label=_('Email'),required=True, widget=forms.EmailInput(attrs={'class': 'validate'}))
    class Meta():
        model = People
        fields = ('firstname', 'lastname', 'email')
        #widgets = {
            #'firstname': forms.Textarea(attrs={'rows': 1, 'class':'col-2'}),
            #'lastname': forms.Textarea(attrs={'rows': 1, 'class':'col-2'}),
            #'email': forms.Textarea(attrs={'rows': 1, 'class':'col-2'}),

            # 'start_time': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            # 'start_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat
            # 'end_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat

        #}

class ProgramForm(forms.ModelForm):#/^([1-9]?\d|100)$/
    timestart = forms.CharField(label=_('Start time of schedule span'),max_length=2, validators=[RegexValidator(r'^\d{1}$|^[1]{1}\d{1}$|^[2]{1}[0-3]{1}$', message=('The start time value should be greater than or equal to 0 and not exceed 23'),)])
    timefinish = forms.CharField(label=_('End time of schedule span'),max_length=2, validators=[RegexValidator(r'^\d{1}$|^[1]{1}\d{1}$|^[2]{1}[0-4]{1}$', message=('The schedule time span cannot exceed 24'),)])
    mineventheight = forms.CharField(label=_('Minimum height of schedule boxes'),max_length=4, validators=[RegexValidator(r'^\d{1,3}$', message=('It should be less than 1000'))])
    heighthr = forms.CharField(label=_('Height for each hour slot'),max_length=2, validators=[RegexValidator(r'^\d{1,2}$', message=('It should be less than 100'))])
    minieventtime = forms.CharField(label=_('Under how many minutes does it switch to the mini format?'),max_length=2, validators=[RegexValidator(r'^\d{1,2}$', message=('It should be less than 100'))])
    opacity = forms.CharField(label=_('Opacity of the boxes'),max_length=2, validators=[RegexValidator(r'^([1-9]|10)$', message=('It should be less than 10 but greater than 0'))])

    class Meta():
        model = ProgramDesign
        fields = ('timestart', 'timefinish', 'mineventheight','heighthr','minieventtime','opacity')

    def clean(self):
        cleaned_data = super().clean()
        #print('clean',cleaned_data)
        if len(cleaned_data)>5:
            st = cleaned_data['timestart']
            end = cleaned_data['timefinish']
            #print('st',st,end)
            if int(st) > int(end):
                raise forms.ValidationError('The start time must be less than the end time.')
            return cleaned_data


class UserProfileInfoForm(forms.ModelForm):
    captcha = CaptchaField(label=_('Solve this math problem'))
    class Meta():
         model = UserProfileInfo
         fields = ('orcid','profile_pic','institute','instcountry','remember_me','job')
         widgets = {
                    'institute': forms.Textarea(attrs={'rows': 1, 'class':'col-8'})
         }
    def __init__(self, *args, **kwargs):
        _job_list = kwargs.pop('data_list', None)
        _country_list = kwargs.pop('data_list2', None)
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['job'].widget = ListTextWidget(data_list=_job_list, name='job-list')
        self.fields['instcountry'].widget = ListTextWidget(data_list=_country_list, name='country-list-inst')

class UpdateUserProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(label=(''),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)#label=_('Company Logo'),

    class Meta():
         model = UserProfileInfo
         fields = ('orcid','profile_pic','institute','instcountry','iban','accountnumber','rootingnumber','bicswiftcode','sortcode','bankcountry','bankusername','remember_me','job')
         widgets = {
                    'institute': forms.Textarea(attrs={'rows': 1, 'class':'col-8'})
         }
    def __init__(self, *args, **kwargs):
        _job_list = kwargs.pop('data_list', None)
        _country_list = kwargs.pop('data_list2', None)
        super(UpdateUserProfileInfoForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['job'].widget = ListTextWidget(data_list=_job_list, name='job-list')
        self.fields['bankcountry'].widget = ListTextWidget(data_list=_country_list, name='country-list')
        self.fields['instcountry'].widget = ListTextWidget(data_list=_country_list, name='country-list-inst')

class CreateConfForm(forms.ModelForm):
    #title= forms.CharField(widget=forms.TextInput(attrs={'style':'max-width: 12em'}))#attrs={"onChange": 'this.form.submit()'}
    start_date = forms.DateField(input_formats=["%d/%m/%Y"], widget=DatePickerInput(format="%d/%m/%Y",attrs={'style':'max-width: 12em'}).start_of('app'))
    end_date = forms.DateField(input_formats=["%d/%m/%Y"], widget=DatePickerInput(format="%d/%m/%Y",attrs={'style':'max-width: 12em'}).start_of('app'))#'onClick':'endchange()',

    class Meta():
        model = CreateConf
        fields = ('title', 'start_date', 'end_date', 'abstract','priv','justtools','feeunique','fee_currency_unique','fee', 'fee_amount', 'fee_currency','fee_to_carbon','fee_variable', 'size', 'subject','proceedin','hybrid','dialin','submitparticipations','activateqandp','daughterconfstarwars','subtomastautomatic','recording','youtuberecording','coffeebreak','coffeebreakgames','room_logo','background','masterconf','daughterconf','masterconfpass')#,'privacy','whorecording'
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5, 'class':'col-9'}),
            'title': forms.Textarea(attrs={'rows':1,'class':'col-9'}),
            #'start_time': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            #'start_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat
            #'end_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat

        }

    def __init__(self, *args, **kwargs):
        _subject_list = kwargs.pop('data_list', None)
        super(CreateConfForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['subject'].widget = ListTextWidget(data_list=_subject_list, name='subject-list')

class CreateConfLightForm(forms.ModelForm):
    closing_date = forms.DateField(label='Abstract deadline for participants', required=False, input_formats=["%d/%m/%Y"], widget=DatePickerInput(format="%d/%m/%Y",attrs={'style':'max-width: 12em'}).start_of('app'))

    class Meta():
        model = CreateConf
        fields = ('poster','dialin','submitparticipations','activateqandp','daughterconfstarwars','subtomastautomatic','recording','whorecording','youtuberecording','coffeebreak','coffeebreakgames','room_logo','background','payingatonce','messagetoall','twitterhashtag','parsession','closing_date')
        widgets = {
            'messagetoall': forms.Textarea(attrs={'rows': 5, 'class': 'col-9'}),
        }

class ProceedingForm(forms.ModelForm):
    #file = forms.FileField(label='',required=False)

    class Meta():
        model = Proceeding
        fields = ('title', 'text','bibtex','status')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10,'class':'col-12',"onClick": 'modtext()',"onfocus": 'modtext()'}),
        }

class WebsiteForm(forms.ModelForm):
    #homecontent = forms.CharField(required=True)
    #rationale = forms.CharField(required=True)

    class Meta():
        model = Website
        fields = ('showprogram','titleurl','hero','showdoc','onlypprogram','onlypabstract','onlypposter','onlypdoc','homecontent', 'rationale','guidelines','color_background','color_text','color_men','share')
        widgets = {
            #'homecontent': forms.Textarea(attrs={'rows': 5, 'cols': 85}),
            #'rationale': forms.Textarea(attrs={'rows': 5, 'cols': 85}),
            'homecontent': SummernoteWidget(),
            'rationale': SummernoteWidget(),
            'guidelines': SummernoteWidget(),
            'color_background': ColorWidget,
            'color_text': ColorWidget,
            'color_men': ColorWidget,

        }

TYPE = (
        (6, "Talk"),
        (1, "Invited Talk"),
        (2, "Discussion"),
        (3, "Review"),
        (4, "Poster"),
        (5, "Attendance only"),
        (7, "Pause"),
)

TYPE_LIMITED = (
        (6, "Talk"),
        (4, "Poster"),
        (5, "Attendance only"),
    )

TYPE_VERY_LIMITED = (
        (6, "Talk"),
        (5, "Attendance only"),
    )

class RegisterConfForm(forms.ModelForm):

    class Meta():
        model = RegisterConf
        fields = ('title', 'abstract', 'biography','facetoface')#,'privacy','whorecording'
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'class': 'col-6'}),
            #'abstract': forms.Textarea(attrs={'rows': 5, 'class':'col-6'}),
            'abstract': SummernoteWidget(),
            'biography': forms.Textarea(attrs={'rows': 5,'class':'col-6'}),
            #'type': forms.Select(),#'refresh(this)'}),

        #'start_time': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            #'start_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat
            #'end_date': DatePickerInput(format='%d/%m/%Y'),  # specify date-frmat

        }

class RegisterConfLightForm(forms.ModelForm):
    class Meta():
        model = RegisterConf
        fields = ('type',)
        widgets = {
            #'type': forms.Select(attrs={"onChange": 'this.form.submit()'}),  # 'refresh(this)'}),
            'type': forms.Select(),  # 'refresh(this)'}),
        }

    def __init__(self, *args, **kwargs):
        is_superuser = kwargs.pop('is_superuser')
        is_noposter = kwargs.pop('is_noposter')
        super(RegisterConfLightForm, self).__init__(*args, **kwargs)
        if is_superuser:
            self.fields['type'].choices = TYPE
        elif is_noposter:
            self.fields['type'].choices = TYPE_VERY_LIMITED
        else:
            self.fields['type'].choices = TYPE_LIMITED

class ArticleUrlForm(forms.ModelForm):

    class Meta():
        model = RegisterConf
        fields = ('paperurl',)#,'privacy','whorecording'
        #field_args = {
         #   "paperurl": {
         #       "error_messages": {
         #           "invalid": "Please let us know what to call you!",
         #           "required": "Pll you!"
        #}
        #    }
        #}

class InstForm(forms.Form):
    abstract = forms.CharField(label=(''),widget=SummernoteWidget())  # instead of forms.Textarea
    #message = forms.CharField(label=_('Your message'),widget=forms.Textarea(attrs={'rows': 5, 'class': 'col-9'}), required=True)


class SlidesForm(forms.ModelForm):

    class Meta():
        model = RegisterConf
        fields = ('slides',)#,'privacy','whorecording'




WHOTO = (
        (0, "Super Users"),
        (1, "All"),
        (2, "Participants with accepted talks/review/discussion"),
        (3, "Participants presenting posters"),
        (4, "Participants with no talks/posters accepted who registered"),
        (5, "Program committee"),
        (6, "Organizers"),
        (7, "Participants you invited but did not register yet"),
        (8, "Moderators"),
        (9, "Those that are only attending but not presenting"),
        (10, "Participants with invited talks"),
        (11, "Participants with discussions"),
        (12, "Participants with reviews"),
        (13, "Participants who paid (if paying conference)"),
        (14, "Participants who have not paid yet (if paying conference)"),
        (15, "Participants who were chosen to participate for free (if paying conference)")
)

class EmailPeopleForm(forms.ModelForm):
    whoto = forms.MultipleChoiceField(choices=WHOTO,label=_("Who to? (you can select several using the Alt key - or Command for Macs - on your keyboard)"))

    class Meta():
        model = EmailPeople
        fields = ('subjectt', 'message', 'whoto', 'replyto','all')#,'privacy','whorecording'
        widgets = {
        #    'message': forms.Textarea(attrs={'rows': 7, 'cols': 120}),
            #'whoto': forms.Select(attrs={'style': 'width:2px'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'col-9'}),
        }


class ExcelPeopleForm(forms.Form):
    excel_file = forms.FileField(label='',required=False)

class EmailPeopleLightForm(forms.ModelForm):

    class Meta():
        model = EmailPeople
        fields = ('subjectt', 'message','replyto')#,'privacy','whorecording'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'col-9'}),
        #    'subject': forms.Textarea(attrs={'rows': 1,'cols': 120}),
        #    'replyto': forms.Textarea(attrs={'rows': 1, 'cols': 80}),
        }

class EmailContactLightForm(forms.ModelForm):
    captcha = CaptchaField(label=_('Solve this math problem'))

    class Meta():
        model = EmailPeople
        fields = ('subjectt', 'message')#,'privacy','whorecording'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'col-9'}),
        #    'subject': forms.Textarea(attrs={'rows': 1,'cols': 120}),
        #    'replyto': forms.Textarea(attrs={'rows': 1, 'cols': 80}),
        }

class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(label=_('Password'),widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            #self.add_error('confirm_password', mark_safe('<p>The Password is not right.</p>'))
            self.add_error('confirm_password', mark_safe('<div class ="alert alert-danger mt-3 col-6" role="alert"><h4> You did not enter the right password.</h4></div>'))


    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    from_email = forms.EmailField(label=_('Your email'),required=True)
    subjecte = forms.CharField(label=_('Subject of the enquiry'),required=True)
    message = forms.CharField(label=_('Your message'),widget=forms.Textarea(attrs={'rows': 5, 'class': 'col-9'}), required=True)
    captcha = CaptchaField(label=_('Solve this math problem'))

class DemoForm(forms.Form):
    from_email = forms.EmailField(label=_('Your work email'),required=True)
    fname = forms.CharField(label=_('First Name'),required=True)
    lname = forms.CharField(label=_('Last Name'),required=True)
    company = forms.CharField(label=_('Company'),required=False)
    phone = forms.CharField(label=_('Phone Number'),required=False)
    message = forms.CharField(label=_('Optional message'),widget=forms.Textarea(attrs={'rows': 5, 'class': 'col-9'}),required=False)
    captcha = CaptchaField(label=_('Solve this math problem'))

class ChatForm(forms.Form):
    titleg = forms.CharField(label=_('Title of the new group'),required=True)
    description = forms.CharField(label=_('Description of the group'),widget=forms.Textarea(attrs={'rows': 5, 'class': 'col-9'}),required=True)
    topic = forms.CharField(label=_('The topic of your group'), required=False)

    def __init__(self, *args, **kwargs):
        people = kwargs.pop('people')
        #print('people',people)
        super(ChatForm, self).__init__(*args, **kwargs)
        counter = 1
        for q in people:
            #print('q',q)
            self.fields[q.username] = forms.BooleanField(label=_('Add ')+q.first_name+' '+q.last_name+' ('+q.email+')?',initial=True,required=False)
            counter += 1

class QuestionForm(forms.ModelForm):
    class Meta():
        model = CreateQuestion

        fields = ('question', 'anonymous')#,'privacy','whorecording'
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2, 'class': 'col-8'}),
        }
        labels = {
            'question': '',
        }
