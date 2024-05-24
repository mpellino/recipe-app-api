"""
Serializer for the user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model= get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self,validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
    
class AuthTokenSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = True
    )

    def validate(self,attrs):
        """Validate and authenticate the user"""

        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg= 'Request of authentication failed with provided credentian'
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
