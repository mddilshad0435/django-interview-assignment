
from django.db import models
from django.conf import settings
# Create your models here.

class Book(models.Model):
    STATUS = (
        ('Available','Available'),
        ('Borrowed','Borrowed'),
    )
    book_title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    publisher = models.CharField(max_length=250)
    price = models.IntegerField()
    
    status = models.CharField(
       max_length=32,
       choices=STATUS,
       default='Available',
    )
class Borrower(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)


