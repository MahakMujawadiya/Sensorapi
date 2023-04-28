from rest_framework import serializers
from .models import Usermodel,Residence

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermodel
        fields = '__all__'

class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = '__all__'