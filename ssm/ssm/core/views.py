from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user or request.user
            token = serializer.validated_data.get('token')
        else:
            return Response({'msg': 'Wrong email or password'}, status=HTTP_401_UNAUTHORIZED)

        # mimic mode
        if user.is_staff and request.data.get('user_id'):
            user = self.user.objects.get(id=request.data.get('user_id'))
            token = str(AccessToken().for_user(user))

        return Response({**serializer.validated_data, **{'token': str(token)}}, status=HTTP_200_OK)
