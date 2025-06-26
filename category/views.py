from ast import AugLoad
from xmlrpc.client import ResponseError

from django.shortcuts import render
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework import status
from rest_framework.generics import  ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.permissions import HasCoursePermission

# Create your views here.


class AddCategoryView(CreateAPIView):

    permission_classes = [HasCoursePermission]
    required_permission = 'add_category'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EditCategoryView(UpdateAPIView):

    permission_classes = [HasCoursePermission]
    required_permission = 'edit_category'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class DeleteCategoryView(DestroyAPIView):
    permission_classes = [HasCoursePermission]
    required_permission = 'delete_category'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        self.perform_destroy(category)
        return Response({"message":"Category Deleted"},status=status.HTTP_200_OK)



class ListCategoryView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ViewCategory(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'





