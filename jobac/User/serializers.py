from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import User, Freelancer, Employer


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    user_type=validated_data['user_type'],
                    email=validated_data['email'],
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Freelancer
        fields = ('user', 'first_name', 'family_name', 'sex', 'age', 'skills', 'resume')

    def create(self, validated_data):
        username = validated_data['user.username']
        pasword = validated_data['user.password']
        email = validated_data['user.email']
        user_type = 2
        user_data = {'username': username, 'password': password, 'email': email,
                     'user_type': user_type}

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)

        person = Freelancer.objects.update_or_create(user=user, name=validated_data.get('first_name'),
                                                     last_name=validated_data.get(
            'last_name'),
            sex=validated_data.get(
            'sex'),
            age=validated_data.get(
            'age'),
            resume=validated_data.get('resume'))
        return person


class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Employer
        fields = ('user', 'name', 'foundation_year',
                  'address', 'number', 'fields')
        # read_only_fields = ('token',)

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['user.username']
        email = validated_data['user.email']
        password = validated_data['user.password']
        user_type = 1
        user_data = {'username': username, 'email': email,
                     'user_type': user_type, 'password': password}
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)

        company, created = Employer.objects.update_or_create(user=user, name=validated_data.get('name'),
                                                             creation_year=validated_data.get(
            'foundation_year'),
            address=validated_data.get(
            'address'),
            number=validated_data.get('number'))
        return company
