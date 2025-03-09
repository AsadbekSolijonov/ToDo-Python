from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from todo.serializers import PhoneNumberAuthTokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = PhoneNumberAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number
        }, status=status.HTTP_200_OK)
