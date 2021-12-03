from rest_framework import serializers
from .models import Dashboard
from .models import CommentRecord

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ('id' ,'title', 'description', 'completed')




class CommentRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommentRecord
        fields = ('user', 'usercomment','likecount','commentid','publishingdate','videoid')
        
