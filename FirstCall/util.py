from django.contrib.admin.models import LogEntry,ADDITION, CHANGE, DELETION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType

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