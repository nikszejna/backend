from django.db import models


class Dashboard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class CommentRecord(models.Model):
    user = models.CharField(max_length=50)
    usercomment = models.TextField()
    likecount = models.SmallIntegerField()
    commentid = models.CharField(max_length=50, unique=True)
    publishingdate = models.DateTimeField()
    sentimentscore = models.FloatField(default=0.0)
    videoid = models.CharField(max_length=50, default="INVALID_VIDEO_ID")

