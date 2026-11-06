from rest_framework import generics, viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        return Response(self.get_serializer(request.user).data)


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False

    def validate(self, attrs):
        username = attrs.pop('username', None)
        if username and not attrs.get('email'):
            user = User.objects.filter(username=username).first()
            if user:
                attrs['email'] = user.email
        if not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Este campo es obligatorio.'})
        return super().validate(attrs)


class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer
