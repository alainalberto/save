from django.contrib.admin.models import LogEntry,ADDITION, CHANGE, DELETION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from FirstCall import settings
from django.contrib import auth

def accion_user(object, action_flag, user):
    """Log changes to Admin log."""
    if action_flag:
        if action_flag == ADDITION:
            change_message = {"added": force_text(object)}
        elif action_flag == CHANGE:
            change_message = {"change": force_text(object)}
        elif action_flag == DELETION:
            change_message = {"delete": force_text(object)}
        try:
            LogEntry.objects.log_action(
                user_id = user.pk,
                content_type_id = ContentType.objects.get_for_model(object).pk,
                object_id = object.pk,
                object_repr = force_text(object),
                change_message = change_message,
                action_flag = action_flag,
                )
        except:
            print("Failed to log action.")



class AutoLogout:
     def __init__(self, get_response):
            self.get_response = get_response

     def __call__(self, request):
       if not request.user.is_authenticated():
        return

       try:
         if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
             auth.logout(request)
             del request.session['last_touch']
             return
       except KeyError:
         pass
       request.session['last_touch'] = datetime.now()
