from django.utils.six import text_type
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    user = None
    user_serializer = None

    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        data['token'] = text_type(self.get_token(self.user).access_token)
        data['user'] = self.user.id
        if getattr(self, 'user_serializer', None):
            data['user'] = self.user_serializer(self.user).data
        return data
