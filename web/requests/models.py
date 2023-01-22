from django.utils.html import mark_safe
from django.db import models


class Request(models.Model):
    id = models.BigIntegerField(
        verbose_name="Telegram ID",
        unique=True,
        primary_key=True
    )

    full_name = models.CharField(
        verbose_name="Full name",
        max_length=100
    )

    username = models.CharField(
        max_length=100,
        verbose_name='Username'
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True
    )

    def get_username(self):
        return mark_safe(f"<a href='https://t.me/{self.username}'>@{self.username}</a>")

    def __str__(self):
        return self.full_name
