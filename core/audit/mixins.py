from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str, force_text
from datetime import datetime

from config import settings as setting


class AuditMixin(object):
    def save_log(self, user, message, ACTION):
        content_type =ContentType.objects.get_for_model(self)
        log = LogEntry.objects.create(
            user_id=user.id,
            content_type_id=content_type.id,
            object_id=self.id,
            object_repr=content_type.name,
            action_flag=ACTION,
            change_message=message,
            action_time=datetime.now()
        )

    def save_addition(self, user):
        if setting.SAVE_LOGS:
            self.save_log(user, 'Ha utilizado la acción de crear', ADDITION)

    def save_edition(self, user):
        if setting.SAVE_LOGS:
            self.save_log(user, 'Ha utilizado la acción de editar', CHANGE)

    def save_deletion(self, user):
        if setting.SAVE_LOGS:
            self.save_log(user, 'Ha utilizado la acción de eliminar', DELETION)