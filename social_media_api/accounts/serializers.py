# accounts/serializers.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # include fields you want to expose
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']
        read_only_fields = ['id']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def create(self, validated_data):
        """
        Create a new user using the project's user model and create a token.
        This uses get_user_model().objects.create_user as requested.
        """
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data.get('email', '')

        # create_user ensures password is hashed and default fields are set
        user = User.objects.create_user(username=username, email=email, password=password)

        # create a token for the new user (Token.objects.create used as requested)
        Token.objects.create(user=user)

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Unable to authenticate with provided credentials.")

        # Attach the user to validated data so the view can access it
        attrs['user'] = user

        # Ensure a token exists (use get_or_create to avoid duplicate token errors)
        token, _ = Token.objects.get_or_create(user=user)
        attrs['token'] = token.key

        return attrs
