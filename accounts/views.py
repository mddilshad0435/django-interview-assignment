from functools import partial
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import BasicAuthentication
from .models import User

from .serializers import (LibrarianRegestrationSerializer,
                          UserDetailSerializer, UserLoginSerializer,
                          UserRegestrationSerializer)


# Creating token manually.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegestrationView(APIView):
    def post(self, request):
        serializer = UserRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        email = request.data['email']
        password = request.data['password']
        print(email,password)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            print("from else")
            return Response({'errors':{'non_fields_errors':['Email or password is not valid']}}, 
                    status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, pk=None):
        print(request.user.id)
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response({'msg':'Account Deleted Successfully'})

class LibrarianRegestrationView(APIView):
    def post(self,request):
        serializer = LibrarianRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CRUDUserLibrarianView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        id = pk
        if id is not None:
            user = User.objects.get(id=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = UserRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'data':serializer.data,'token':token,'msg':'member Registered Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserRegestrationSerializer(user,data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'data':serializer.data,'token':token,'msg':'User data Updated'},status=status.HTTP_200_OK)
    def patch(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserRegestrationSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'data':serializer.data,'token':token,'msg':'User data Updated'},status=status.HTTP_200_OK)
    def delete(self, request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'msg':'Member Deleted Successfully'}, status=status.HTTP_200_OK)