from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'date_of_registration', 'first_name', 'last_name']

    """
    Code below is for a usual Serializer class, not ModelSerializer:

    id = serializers.IntegerField(read_only=True)
    date_of_registration = serializers.DateTimeField(format="%Y-%m-%d")
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    
    def create(self, data):
        return User.objects.create(**data)
    
    def update(self, instance, data):
        instance.date_of_registration = data.get('date_of_registration', instance.date_of_registration)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.save()

        return instance
    """
    