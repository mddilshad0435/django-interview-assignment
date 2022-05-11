from django.contrib import admin

from .models import Book, Borrower

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_title', 'author', 'publisher', 'price', 'status']
@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['id','user','book']
