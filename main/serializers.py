from rest_framework import serializers
from main.models import RefBook, RefBookElement


class RefBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefBook
        fields = ['id', 'code', 'name']


class RefBookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefBookElement
        fields = ['code', 'value']
