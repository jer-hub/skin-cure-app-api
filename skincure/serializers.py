from rest_framework import serializers
from .models import Profile, Result
from django.utils.timezone import localtime

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user']
        
class ResultSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ['id', 'profile', 'skin_disease', 'accuracy', 'description', 'age', 'sex', 'pic', 'created_at']

    def get_created_at(self, obj):
        created_at = localtime(obj.created_at).strftime("%m-%d-%y %H:%M")
        return created_at