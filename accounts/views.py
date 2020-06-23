from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView

from accounts.models import UserProfile
from accounts.serializers import UserSerializer, UserProfileSerializer


# Create your views here.


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class UserProfileView(RetrieveUpdateAPIView):
    model = UserProfile
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListUsersView(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(Q(user__email__contains=keyword) |
                                          Q(user__username__contains=keyword) |
                                          Q(user__username__contains=keyword) |
                                          Q(user__first_name__contains=keyword) |
                                          Q(user__last_name__contains=keyword) |
                                          Q(bio__contains=keyword) |
                                          Q(location__contains=keyword) |
                                          Q(website__contains=keyword))
