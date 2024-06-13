from rest_framework import serializers
from user.models import User, Discussion


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class DiscussionSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.name
        else:
            return None
    class Meta:
        model = Discussion
        fields = "__all__"

    
    def create(self, validated_data):
        return super().create(validated_data)
   