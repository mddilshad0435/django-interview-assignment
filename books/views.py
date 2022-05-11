import imp
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Book, Borrower
from .serializers import BookSerializer, BorrowerSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BookListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request, pk=None):
        id = pk
        if id is not None:
            boo = Book.objects.get(id=pk)
            serializer = BookSerializer(boo)
            return Response(serializer.data)
        boo = Book.objects.all()
        serializer = BookSerializer(boo, many=True)
        return Response(serializer.data)
class BookCRUDView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request, pk=None):
        id = pk
        if id is not None:
            boo = Book.objects.get(id=pk)
            serializer = BookSerializer(boo)
            return Response(serializer.data)
        boo = Book.objects.all()
        serializer = BookSerializer(boo, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request, pk=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'data Created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    def put(self, request, pk=None):
        boo = Book.objects.get(id=pk)
        serializer = BookSerializer(boo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'data fully Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors)
    def patch(self, request, pk=None):
        boo = Book.objects.get(id=pk)
        serializer = BookSerializer(boo,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'data partial Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors)
    def delete(self, request, pk=None):
        boo = Book.objects.get(id=pk)
        boo.delete()
        return Response({'msg':'Data Deleted!!'},status=status.HTTP_200_OK)
class BorrowBookView(APIView):
    authentication_classes= [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
    def post(self, request, pk=None):
        book = pk
        user = request.user.id
        print("book",book,"user",user)
        serializer = BorrowerSerializer(data={"book":book,"user":user})
        if serializer.is_valid():
            book = Book.objects.filter(id=pk).filter(status='Available').first()
            if book is not None:
                serializer.save()
                book = Book.objects.get(id=pk)
                book.status='Borrowed'
                book.save()
                return Response({'msg':'Book Borrowed successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Book is not available'},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_200_OK)
            
class BookReturnView(APIView):
    authentication_classes= [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            borrow = Borrower.objects.filter(id=pk).filter(user=user).first()
            serializer = BorrowerSerializer(borrow)
            return Response(serializer.data)
        borrow = Borrower.objects.all().filter(user=user)
        serializer = BorrowerSerializer(borrow, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request, pk=None):
        borrow = Borrower.objects.get(id=pk)
        book = borrow.book.id
        book = Book.objects.get(id=book)
        book.status='Available'
        book.save()
        borrow.delete()
        return Response({'msg':'Book return successfully'},status=status.HTTP_200_OK)

class BorrowedListBookView(APIView):
    authentication_classes= [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request):
        borrow = Borrower.objects.all()
        serializer = BorrowerSerializer(borrow, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

        


    


    




