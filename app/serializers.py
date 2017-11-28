from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from app.models import *

User = get_user_model()


class DynamicModelSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		excludes = kwargs.pop('exclude', None)

		if fields and excludes:
			raise EthanWarning("Cannot have both `fields` and `exclude` arguments at the same time!")

		super(DynamicModelSerializer, self).__init__(*args, **kwargs)

		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)

		if excludes is not None:
			existing = set(self.fields.keys())
			excludes = set(excludes)
			allowed = existing - excludes
			excludes = existing - allowed
			for field_name in excludes:
				self.fields.pop(field_name)


class UserSerializer(DynamicModelSerializer):
	class Meta:
		model = User
		exclude = [
			'is_superuser', 'password', 'is_staff',
			'is_active', 'user_permissions','groups'
		]


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)

		if user:
			if not user.is_active:
				msg = _('User account is disabled.')
				raise serializers.ValidationError(msg, code='authorization')
		else:
			msg = _('username or password incorrect.')
			raise serializers.ValidationError(msg, code='authorization')

		data['user'] = user
		return data


class MomentSerializer(DynamicModelSerializer):
	class Meta:
		model = Moment
		fields = '__all__'