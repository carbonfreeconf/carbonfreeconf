from .models import Post, CreateConf
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

if 'ON_HEROKU' in os.environ:
  @receiver(post_save, sender=Post)
  def index_post(sender, instance, **kwargs):
      instance.indexing()

if 'ON_HEROKU' in os.environ:
  @receiver(post_save, sender=CreateConf)
  def index_conf(sender, instance, **kwargs):
      instance.indexing()