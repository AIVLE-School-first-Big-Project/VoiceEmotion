from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

# Create your models here.

User = get_user_model()


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    content = models.TextField(null=False)
    image = models.FileField(null=True, blank=True, upload_to='img/')
    date = models.DateTimeField(default=now, editable=False, null=False)

    class Meta:
        db_table = 'board'


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, editable=False, null=False)
    content = models.TextField()

    class Meta:
        db_table = 'comment'
