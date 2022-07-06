# context_processors.py
'''def message_processor(request):
    if request.user.is_authenticated:
        no_msgs = 1#request.user.profile.msgs
        print('r'+str(no_msgs))
    else:
        no_msgs = 0
    return {
        'mess2' : request.session.get('idconf','')#request.get_full_path()#str(no_msgs)
    }'''