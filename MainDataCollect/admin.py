from django.contrib import admin

# Register your models here.
from MainDataCollect.models import *

class UserRatingAdmin(admin.ModelAdmin):
	def time_seconds(self, obj):
		return obj.Date.strftime("%d-%b-%Y | %H:%M:%S")
	time_seconds.short_description = 'Precise Time'  
	
	list_display = ('UserID', 'RatingType', 'FVideo', 'time_seconds',)

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('UserID', 'UserGender', 'UserAge', 'Page', 'FVideo',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'Video', 'UploaderName',)

class VideoMetaAdmin(admin.ModelAdmin):
    list_display = ('UpVideo', 'DataUnit', 'DataRange', 'SecondsIn')

class ControlDataAdmin(admin.ModelAdmin):
    list_display = ('UpVideo', 'DataVal')

admin.site.register(OneClickRating, UserRatingAdmin)
admin.site.register(StepClickRating, UserRatingAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(UploadedVideo, VideoAdmin)
admin.site.register(VideoMetaData, VideoMetaAdmin)
admin.site.register(VideoControlData, ControlDataAdmin)