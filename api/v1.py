from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, list_route, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from app.models import *
from app.serializers import *

User = get_user_model()


@api_view(['GET', 'POST'])
def test(request):
	return Response('ok')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def test_with_login(request):
	serializer = UserSerializer(request.user, fields=['username', 'email', 'last_login', 'date_joined'])
	return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def list(self, request, *args, **kwargs):
		users = User.objects.all()
		if not request.user.is_anonymous:
			serializer = UserSerializer(users, many=True)
		else:
			serializer = UserSerializer(users, fields=['username', 'email'], many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None, *args, **kwargs):
		user = get_object_or_404(self.queryset, pk=pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	@list_route(methods=['post'])
	def register(self, request, *args, **kwargs):
		serializer = UserSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		User.objects.create_user(**serializer.validated_data)
		return Response(serializer.validated_data)

	@list_route(methods=['post'])
	def login(self, request, *args, **kwargs):
		serializer = LoginSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		serializer.validated_data['token'] = token
		return Response({'token': token.key})


class MomentViewSet(viewsets.ModelViewSet):
	queryset = Moment.objects.all()
	serializer_class = MomentSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, ]

	def create(self, request, *args, **kwargs):
		serializer = MomentSerializer(data=request.data, fields=['image'])
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		moment = Moment.objects.create(author=request.user, **serializer.validated_data)
		return Response(MomentSerializer(moment).data)
