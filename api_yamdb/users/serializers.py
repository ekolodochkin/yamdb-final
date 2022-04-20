from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class CustomUserCreationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[validators.UniqueValidator(
                                   queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('email', 'username'),
                message="Логин и email должны быть уникальными"
            )
        ]

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(f'Логин {username} недоступен')
        return username


class CodeConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    extra_kwargs = {
        'confirmation_code': {'required': True},
        'username': {'required': True},
    }
