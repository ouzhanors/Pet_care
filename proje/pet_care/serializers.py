from rest_framework import serializers
from .models import Pet, CareTask, Expense, Reminder
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Pet
        fields = '__all__'

class CareTaskSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    
    class Meta:
        model = CareTask
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    
    class Meta:
        model = Reminder
        fields = '__all__' 