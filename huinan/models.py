from django.db import models


class Member(models.Model):
    openid = models.CharField(max_length=100, primary_key=True, default='')
    sessionKey = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True)
    nickName = models.CharField(max_length=100, blank=True, default='')
    avatarUrl = models.TextField()
    phoneNum = models.CharField(max_length=100, default='')
    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
