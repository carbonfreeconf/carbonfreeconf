from django import template
import datetime
from datetime import date, timedelta
from django.utils.timezone import localtime, now
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def datechange(value):
    return value[:10]

@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    delta = value - datetime.date.today()#localtime(now()).date#datetime.datetime.now()
    print('ind',value,delta,localtime(now()).date)
    if delta.days == 0:
        return "Today!"
    elif delta.days < 1:
        return "%s %s ago" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 1:
        return "In %s days" % delta.days

@register.filter(name='get_due_datetime_string')
def get_due_date_string(value):
    delta = value - localtime(now())#datetime.datetime.now()
    print('ind',value,delta,localtime(now()))
    if delta.days == 0:
        return "Today!"
    elif delta.days < 1:
        return "%s %s ago" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 1:
        return "In %s days" % delta.days


@register.filter(name='ellipses')
def ellipses(value, arg):
    original_string = value
    max_length = arg

    if len(original_string) <= max_length:
        return original_string
    else:
        return original_string[:max_length] + "..."

@register.simple_tag
def pagenum(pagenum, perpage, forloop):
    new_id = (pagenum-1)*perpage+forloop    ## here's the mathematical operation
    return new_id

@register.filter
def get_item(queryset,i):
    return queryset[i].abstract

