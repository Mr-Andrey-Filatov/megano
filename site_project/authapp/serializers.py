from rest_framework import serializers
from authapp.models import User


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                "Your old password was entered incorrectly. Please enter it again."
            )

        return value

    def update(self, instance, validated_data):
        password = validated_data["new_password"]
        instance.set_password(password)
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "fullName", "email", "phone", "avatar"
        read_only_fields = ["avatar"]
