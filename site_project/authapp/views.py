from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.serializers import ProfileSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            update_session_auth_hash(request, request.user)

        return Response({"new_password": "Successfully saved"})


class SetAvatarView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user, data=request.data)
        serializer.Meta.fields = ("avatar",)
        serializer.Meta.read_only_fields = []

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({"url": serializer.data["avatar"]})
