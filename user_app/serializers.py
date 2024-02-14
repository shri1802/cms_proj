from rest_framework import serializers
from .models import Claim, Policy

class ClaimUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['amt', 'reason']  # Fields accessible to users

class ClaimAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'

class PolicyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['start_date', 'end_date','type','lumpsum','premium']  # Fields accessible to users

class ClaimAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'