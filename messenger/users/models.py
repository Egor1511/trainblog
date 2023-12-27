from django.contrib.auth.models import AbstractUser
from django.db import models


class Contact(models.Model):
    user_from = models.ForeignKey(
        'User', related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        'User',
        related_name='rel_to_set',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/",
        blank=True, null=True,
        verbose_name="Фотография"
    )
    date_birth = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    following = models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
