from rest_framework import serializers

from .models import CustomUser, Global, Spam


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = '__all__'
    
    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GlobalDbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Global
        fields = '__all__'

class SpamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spam
        fields = '__all__'