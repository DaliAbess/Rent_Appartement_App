from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password','phone','role','avatar','username']
        extra_kwargs = {
            'password' : { 'write_only': True}
        }
    def validate(self, data):
        if User.objects.filter(email=data['email']).first():
            raise serializers.ValidationError({"error":"Email Adresse Already Exist"})
        if User.objects.filter(phone=data['phone']).first():
            raise serializers.ValidationError({"error":"Phone number Already Exist"})
        return data
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance   
