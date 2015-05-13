__author__ = 'Diegopc'

from django.forms import widgets
from rest_framework import serializers
from inverboy.models import *


class StageSerializer(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    name = serializers.CharField(max_length=140)
    initials = serializers.CharField(max_length=4)
    description = serializers.CharField(widget=widgets.Textarea, max_length=100000)
    #image = serializers.ImageField()p
    