from django.shortcuts import render
from .serializers import DashboardSerializer, CommentRecordSerializer 
from rest_framework import viewsets     
from django.http import HttpResponse 
from .models import Dashboard    
from .models import CommentRecord
from rest_framework.decorators import api_view            
from rest_framework import status 
from django.http.response import JsonResponse
import nltk
from .sentiment_analysis import  getSentimentLabel, get_sentiment_barchart_bytes
from .get_comments import get_comments


import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
import sqlite3
 



class DashboardView(viewsets.ModelViewSet):  
    serializer_class = DashboardSerializer   
    queryset = Dashboard.objects.all()     

class CommentView(viewsets.ModelViewSet):
    queryset = CommentRecord.objects.all().order_by('user')
    serializer_class = CommentRecordSerializer


@api_view(['GET'])
def start_comment_retrieval(request):
    if request.method == 'GET':
        videoId = request.query_params.get('videoid', None)
        if videoId is not None:
            get_comments(videoId)
        else:
            return JsonResponse({"error":"videoid required"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'started':True}, status=status.HTTP_200_OK) 

@api_view(['GET'])
def get_video_sentiment_chart(request):
    if request.method == 'GET':
        videoId = request.query_params.get('videoid', None)
        if videoId is not None:
            barchart_bytes = get_sentiment_barchart_bytes(videoId)
            return HttpResponse(barchart_bytes, content_type="image/png")
        else:
            return JsonResponse({"error":"videoid required"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'started':True}, status=status.HTTP_200_OK) 







