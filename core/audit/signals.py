from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.audit.middleware import RequestMiddleware


def get_models():
    from django.contrib.contenttypes.models import ContentType
    data = []
    for i in ContentType.objects.filter().exclude(id__in=[1, 2, 3, 4, 5]):
        model = i.model_class()
        data.append(model.__name__)
    return data


@receiver(post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
    list_of_models = get_models()
    if sender.__name__ not in list_of_models:
        return
    user = get_user()
    if not user is None:
        if not user.is_anonymous:
            if created:
                instance.save_addition(user)
            elif not raw:
                instance.save_edition(user)


@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
    list_of_models = get_models()
    if sender.__name__ not in list_of_models:
        return
    user = get_user()
    if not user is None:
        if not user.is_anonymous:
            instance.save_deletion(user)


def get_user():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'user'):
        user = thread_local.user
    else:
        user = None
    return user
