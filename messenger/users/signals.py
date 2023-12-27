from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import User


@receiver(post_save, sender=User)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Новый пользователь',
            f'Зарегестрирорван новый юзер  #{instance.username, instance.email}.',
            'maysannas51@gmail.com',
            ['egoriegor1511@gmail.com'],
            fail_silently=False,
        )