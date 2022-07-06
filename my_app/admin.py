from django.contrib import admin
from .models import Search
from .models import UserProfileInfo, User, CreateConf, Schedule, People, Post, Website, \
    RegisterConf, UserLink,EmailPeople, CreateVisio, Proceeding, Transac, CreateQuestion, UserUpdateQ, \
    CreatePoll, ChoicePoll, ProgramDesign, ChatCanal, PosterView, StatsMaster, HeroPicture
from django_summernote.admin import SummernoteModelAdmin

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MyUserCreationForm(UserCreationForm):
    username = forms.RegexField(
        label='Username',
        max_length=150,
        regex=r'^[A-Za-z0-9\-_]+$',
        help_text = 'Required. 150 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores, no accents).',)
        #error_message = 'This value must contain only letters, numbers, hyphens and underscores.')

class MyUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label='Username',
        max_length=150,
        regex=r'^[A-Za-z0-9\-_]+$',
        help_text = 'Required. 150 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores, no accents).',)
        #error_message = 'This value must contain only letters, numbers, hyphens and underscores.')

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)



class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    search_fields = ('user__email', 'user__last_name', 'user__first_name')


# Register your models here.
admin.site.register(ProgramDesign)
admin.site.register(Search)
admin.site.register(UserProfileInfo,UserAdmin)
#admin.site.register(CreateConf)
#admin.site.register(Event)
admin.site.register(Schedule)
admin.site.register(People)
admin.site.register(UserLink)
admin.site.register(EmailPeople)
admin.site.register(Proceeding)
admin.site.register(Transac)
admin.site.register(CreateQuestion)
admin.site.register(UserUpdateQ)
admin.site.register(CreatePoll)
admin.site.register(ChatCanal)
admin.site.register(PosterView)
admin.site.register(StatsMaster)
admin.site.register(HeroPicture)

class RegisterAdmin(SummernoteModelAdmin):
    summernote_fields = ('abstract',)
    search_fields = ('user__email', 'user__last_name', 'user__first_name','title','abstract','conference__title')

    #class Media:
    #    js = (
    #        '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
    #        '//cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
    #        '//stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js',
    #        '//cdnjs.cloudflare.com/ajax/libs/summernote/0.8.18/summernote.min.js',
    #        '//cdnjs.cloudflare.com/ajax/libs/summernote/0.8.18/summernote-bs4.min.js',
            #'//cdn.jsdelivr.net/npm/bs4-summernote@0.8.10/dist/summernote-bs4.min.js',
    #    )

admin.site.register(RegisterConf,RegisterAdmin)

class CreateVisioAdmin(admin.ModelAdmin):
    search_fields = ('conference__title',)

admin.site.register(CreateVisio,CreateVisioAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(ChoicePoll,ChoiceAdmin)

class WebsiteAdmin(SummernoteModelAdmin):
    #summernote_fields = ('rationale','homecontent','guidelines')
    search_fields = ('conference__title', 'rationale', 'homecontent')

admin.site.register(Website,WebsiteAdmin)



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


#class PostAdmin(SummernoteModelAdmin):
 #   summernote_fields = ('content',)

#admin.site.register(Post, PostAdmin)

class ConfAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status')
    list_filter = ("status",)
    search_fields = ['title']
    readonly_fields = ('created',)

admin.site.register(Post, PostAdmin)
admin.site.register(CreateConf, ConfAdmin)


#admin.site.register(Post)
