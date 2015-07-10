from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from MainDataCollect.models import *
from MainDataCollect.forms import *

import json
import datetime, time
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from collections import defaultdict
from pprint import pprint #debug

import scipy
from scipy import stats
from scipy.stats import pearsonr

import re

# Create your views here.
def home(request):
    ''' loads mainpage / '''
    return HttpResponseRedirect('/uploadVideo') 
    #return render_to_response('index.html', context_instance=RequestContext(request))

def oneclick(request):
    ''' loads onecick data collection page /clicker '''
    return render_to_response('oneclick.html', context_instance=RequestContext(request))

def stepclicker(request, UName, VideoName):
    ''' loads onecick data collection page /step-clicker '''
    Vidobject = get_object_or_404(UploadedVideo, UploaderName=UName, Video=VideoName)
    data = {
        'VideoName':VideoName, #video size?
        'UploaderName':UName,
    }
    return render_to_response('stepclicker.html', data, context_instance=RequestContext(request))

def recvData(request):
    '''store Data'''
    if request.method == 'POST':
        UserID = str(request.POST.get('userid', ""))
        UserGender = str(request.POST.get('usergender', ""))
        UserAge = int(request.POST.get('userage', ""))
        page = str(request.POST.get('page', ""))
        videoname = str(request.POST.get('pagevideo', ""))
        uploadername = str(request.POST.get('pageuploader', ""))

        Vidobject = get_object_or_404(UploadedVideo, UploaderName=uploadername, Video=videoname)

        RatingsList = json.loads(request.POST.get('ratings', False))
        DateList = json.loads(request.POST.get('daterate', False))


        userobj = UserDetails.objects.create(UserID=UserID, UserGender=UserGender, UserAge=UserAge, Page=page, FVideo=Vidobject)

        if page == 'OC':
            for rate,date in zip(RatingsList, DateList):
                OneClickRating.objects.create(FVideo=Vidobject, UserID=userobj, RatingType=rate, Date=date)

            return HttpResponse('Success!')

        else:
            for rate,date in zip(RatingsList, DateList):
                StepClickRating.objects.create(FVideo=Vidobject, UserID=userobj, RatingType=rate, Date=date)

            return HttpResponse('Success!')

def dataVis(request, UName, VideoName): #videoname in url
    ''' Graphically display results'''
    SCResults = StepClickRating.objects.filter(FVideo__UploaderName=str(UName), FVideo__Video=str(VideoName)) #filter videoname

    VideoData = VideoMetaData.objects.filter(UpVideo__UploaderName=str(UName), UpVideo__Video=str(VideoName))

    UniqueIDs = list(SCResults.values_list('UserID__UserID').distinct())

    #------------------------------------ getting partition data ----------------------------------------------------
    parttimelist = []
    viddata = []
    viddatavals = []

    parttimelist = VideoData.values_list('SecondsIn')
    parttimelist = [i[0] for i in parttimelist]

    for VidDataObj in VideoData:
        vidvals = re.findall("[\d\.\d]+", VidDataObj.DataRange)
        vidvals = [float(x) for x in vidvals]
        vidvals = sum(vidvals)/len(vidvals)
        viddatavals.append(vidvals)
        viddata.append(VidDataObj.DataRange + ' ' + VidDataObj.DataUnit)

    #------------------------------------ Scatter Plot ----------------------------------------------------
    timelist = []
    ratinglist = []
    objlist = [] #list of filter results

    for uid in UniqueIDs: #uid is tuple (second val is blank)
        objlist = ( SCResults.filter(UserID__UserID=uid[0]))
        mintime = time.mktime(min(objlist.values_list('Date')[0]).timetuple())
        prevtimediff = 0
        for obj in objlist:
            timediff = time.mktime(obj.Date.timetuple()) - mintime
            if prevtimediff == timediff: #prevents multiple inputs on the same time (user clicked button multiple times in 1s)
                continue
            else:
                if obj.RatingType != 0:
                    prevtimediff = timediff
                    timelist.append(timediff)
                    ratinglist.append(obj.RatingType)

    resultsdata = zip(timelist, ratinglist)

    #------------------------------------ Control Data Plot----------------------------------------------------
    controlData = VideoControlData.objects.filter(UpVideo__Video=VideoName, UpVideo__UploaderName=UName)
    controlVals = [i[0] for i in controlData.values_list('DataVal')]
    controlTime = range(1, len(controlVals)+1)

    #------------------------------------ Average Plot + Correlation Calc (Pearson) --------------------------------

    r_rows = []
    p_values = []

    avgtime = []
    avgdata = []
    r_row=0
    p_value=0

    tempparttimelist = parttimelist
    tempparttimelist.append(60000) #last segment cant be more than 60000s

    if len(parttimelist) < 2:
        tempavgtimeparse = []
        tempavgdataparse = []
        for timeval, rating in zip(timelist, ratinglist):
            tempavgtimeparse.append(timeval)
            tempavgdataparse.append(rating)
        if len(tempavgtimeparse) > 0:
            avgtime.append(float(sum(tempavgtimeparse))/len(tempavgtimeparse))
            avgdata.append(float(sum(tempavgdataparse))/len(tempavgdataparse))
            x = scipy.array(tempavgtimeparse)
            y = scipy.array(tempavgdataparse)
            r_row, p_value = pearsonr(x, y)
            if np.isnan(r_row): r_row='Cannot compute'
            r_rows.append(r_row)
            p_values.append(p_value)

    else:
        for i in xrange(len(parttimelist) - 1):
            tempavgtimeparse = []
            tempavgdataparse = []
            for timeval, rating in zip(timelist, ratinglist):
                if timeval<=tempparttimelist[i+1] and timeval>tempparttimelist[i]:
                    tempavgtimeparse.append(timeval)
                    tempavgdataparse.append(rating)
            if len(tempavgtimeparse) > 0:
                avgtime.append(float(sum(tempavgtimeparse))/len(tempavgtimeparse))
                avgdata.append(float(sum(tempavgdataparse))/len(tempavgdataparse))
                x = scipy.array(tempavgtimeparse)
                y = scipy.array(tempavgdataparse)
                r_row, p_value = pearsonr(x, y)
                if np.isnan(r_row): r_row='Cannot compute'
                r_rows.append(r_row)
                p_values.append(p_value)

    statsdata = 0
    if len(viddata) > 1:
        statoftotal = 0
        x = scipy.array(timelist)
        y = scipy.array(ratinglist)
        r_row, p_value = pearsonr(x, y)
        if np.isnan(r_row): r_row='Cannot compute'
        r_rows.append(r_row)
        p_values.append(p_value)
        statsdata = zip(viddata+['All Sections'], r_rows, p_values)
    else:
        statsdata = zip(['All Sections'], r_rows, p_values)


    #------------------------------------ Feeback vs Control Data (avg) Plot -----------------------------------------------
    #''' Control data and video msut be time-synchronized '''
    #get rating associated with time, get control value associated with time
    #average controlled data over the previous two seconds is taken as the synced value (for that time instant)
    feedbackvscontrol = []

    if len(controlVals) > 1:
        synccontroldata = []
        for i in xrange(len(timelist)-1):
            if timelist[i] > 1:
                avg2s = (controlVals[int(timelist[i]-1)] + controlVals[int(timelist[i]-2)])/2
                synccontroldata.append(avg2s)
        feedbackvscontrol = zip(synccontroldata, ratinglist)

    elif len(viddatavals) > 1:
        for i in xrange(len(tempparttimelist)-1):
            for timeval, feedback in resultsdata:
                if timeval < parttimelist[i+1] and timeval>parttimelist[i]:
                    feedbackvscontrol.append( (viddatavals[i], feedback) )

    #------------Stats for Feedback vs Control ---------------------------
    controlstats = []
    if len(feedbackvscontrol) > 1:
        x,y = zip(*feedbackvscontrol)
        x = [float(i) for i in x]
        y = [float(i) for i in y]
        x = scipy.array(x)
        y = scipy.array(y)
        controlstats = stats.linregress(x,y) # returns slope, intercept, r_value, p_value, std_err
        pprint(controlstats)

    #------------------------------------ Load Page with Calc Data -----------------------------------------------
    data = {
        'resultsdata' : resultsdata,
        'vidmetadata' : zip(parttimelist, viddata),
        'avgresultsdata' : zip(avgtime, avgdata),
        'pearsonstats' : statsdata,
        'numparticipants' : len(UniqueIDs),
        'controldata' : zip(controlTime, controlVals),
        'controlunit' : VidDataObj.DataUnit,
        'feedbackvscontrol' : feedbackvscontrol,
        'feedbackvscontrolstats' : controlstats,
    }

    return render_to_response('data-vis.html', data,  context_instance=RequestContext(request))

def uploadVideo(request):
    if request.POST:
        form = UploadVideoForm(request.POST, request.FILES)
        parttimelist = (request.POST.getlist('PartTime[]',0))
        dataunitlist = (request.POST.getlist('DataUnit[]',0))
        datarangelist = (request.POST.getlist('DataRange[]',0))
        datavals = (request.POST.get('datavals','')).splitlines()

        pprint(datavals)

        if form.is_valid():
            form.save()

            UploaderName = str(request.POST.get('UploaderName', ""))
            LatestUserVidObj = UploadedVideo.objects.filter(UploaderName=UploaderName)[::-1][0]
            LatestUserVid = str(LatestUserVidObj.Video)

            for parttime, dataunit, datarange in zip(parttimelist, dataunitlist, datarangelist):
                if parttime != '':
                    VideoMetaData.objects.create(UpVideo=LatestUserVidObj, DataUnit=dataunit, DataRange=datarange, SecondsIn=parttime)

            for dataval in datavals:
                VideoControlData.objects.create(UpVideo=LatestUserVidObj, DataVal=dataval)

            return HttpResponseRedirect('/step-clicker/'+UploaderName+'/'+LatestUserVid) #user/videoname

    else:
        form = UploadVideoForm()

    args = {}
    args['form'] = form

    return render_to_response('upload.html', args, context_instance=RequestContext(request))