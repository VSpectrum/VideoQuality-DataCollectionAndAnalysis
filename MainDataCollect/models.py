from django.db import models
from time import time
import datetime

def get_upload_file_name(instance, filename):
    return "%s_%s" % (str(datetime.datetime.now().date()), filename)

# Create your models here.

class UploadedVideo(models.Model):
    Video = models.FileField(upload_to=get_upload_file_name)
    UploaderName = models.CharField(max_length=50, blank=False)
    class Meta:
        verbose_name = 'Uploaded Video'
        verbose_name_plural = 'Uploaded Videos'

    def __unicode__(self):
        return str(self.id)

class VideoMetaData(models.Model):
    UpVideo = models.ForeignKey(UploadedVideo)
    DataUnit = models.CharField(max_length=10, blank=True)
    DataRange = models.CharField(max_length=50, blank=True)
    SecondsIn = models.IntegerField(blank=False)
    class Meta:
        verbose_name = 'Uploaded Video MetaData'
        verbose_name_plural = 'Uploaded Video MetaData'

    def __unicode__(self):
        return str(self.id)

class VideoControlData(models.Model):
    UpVideo = models.ForeignKey(UploadedVideo)
    DataVal = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    class Meta:
        verbose_name = 'Video Control Data'
        verbose_name_plural = 'Video Control Data'

    def __unicode__(self):
        return str(self.id)

class UserDetails(models.Model):
    Pages = (
        ('OC', 'One Clicker'),
        ('SC', 'Step Clicker'),
    )    

    UserID = models.CharField(max_length=33, blank=False)
    UserGender = models.CharField(max_length=1, blank=False)
    UserAge = models.IntegerField(blank=False)
    Page = models.CharField(max_length=2, choices=Pages, blank=False)
    FVideo = models.ForeignKey(UploadedVideo)
    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'

    def __unicode__(self):
        return self.UserID



class OneClickRating(models.Model):
    Types = (
        ('A', 'Audio'),
        ('V', 'Video'),
        ('ST', 'Started Video'),
    )
    FVideo = models.ForeignKey(UploadedVideo)
    UserID = models.ForeignKey(UserDetails)
    RatingType = models.CharField(max_length=2, choices=Types, blank=False)
    Date = models.DateTimeField()

    class Meta:
        verbose_name = 'OneClick Ratings'
        verbose_name_plural = 'OneClick Ratings'

    def __unicode__(self):
        return self.UserID.UserID

class StepClickRating(models.Model):
    FVideo = models.ForeignKey(UploadedVideo)
    UserID = models.ForeignKey(UserDetails)
    RatingType = models.IntegerField(blank=False) #0 signifies start
    Date = models.DateTimeField()

    class Meta:
        verbose_name = 'StepClick Ratings'
        verbose_name_plural = 'StepClick Ratings'

    def __unicode__(self):
        return self.UserID.UserID