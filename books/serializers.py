from dataclasses import fields
import imp
from pyexpat import model
from rest_framework import serializers
from .models import Book, Borrower

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_title', 'author', 'publisher', 'price', 'status']
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'user', 'book']
