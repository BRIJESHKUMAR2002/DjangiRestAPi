from rest_framework import serializers
from .models import Task, TaskMember


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskMember
        fields = '__all__'
