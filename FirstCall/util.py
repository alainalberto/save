from django.contrib.admin.models import LogEntry,ADDITION, CHANGE, DELETION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from FirstCall import settings
from django.contrib import auth

from datetime import datetime

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




def set_last_activity(session, dt):
    """ Set the last activity datetime as a string in the session. """
    session['_session_security'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')


def get_last_activity(session):
    """
    Get the last activity datetime string from the session and return the
    python datetime object.
    """
    try:
        return datetime.strptime(session['_session_security'],
                '%Y-%m-%dT%H:%M:%S.%f')
    except AttributeError:
        #################################################################
        # * this is an odd bug in python
        # bug report: http://bugs.python.org/issue7980
        # bug explained here:
        # http://code-trick.com/python-bug-attribute-error-_strptime/
        # * sometimes, in multithreaded enviroments, we get AttributeError
        #     in this case, we just return datetime.now(),
        #     so that we are not logged out
        #   "./session_security/middleware.py", in update_last_activity
        #     last_activity = get_last_activity(request.session)
        #   "./session_security/utils.py", in get_last_activity
        #     '%Y-%m-%dT%H:%M:%S.%f')
        #   AttributeError: _strptime
        #
        #################################################################

        return datetime.now()
    except TypeError:
        return datetime.now()

