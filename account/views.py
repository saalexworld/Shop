
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from .models import User
from drf_yasg.utils import swagger_auto_schema

class RegisterView(APIView): # только пост запрос
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request): # обязательно принимает реквест
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successufully register', status=201)


class ActivationView(APIView):
    def get(self, reqiuest, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('User does not exist', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', status=200)

