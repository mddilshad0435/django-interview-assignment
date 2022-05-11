from django.contrib import admin
from django.urls import path, include
from books import views

urlpatterns = [
    # Url of member view list of book
    path('list/', views.BookListView.as_view()),
    path('list/<int:pk>', views.BookListView.as_view()),
    # URL of librarian to view create update and delete a book
    path('lists/', views.BookCRUDView.as_view()),
    path('lists/<int:pk>', views.BookCRUDView.as_view()),
    # URL to view book available for borrow and borrow book from post method
    path('borrow/', views.BorrowBookView.as_view()),
    path('borrow/<int:pk>', views.BorrowBookView.as_view()),
    # URL to view borrowed book and can also return through post method
    # only the same user can see the borrowed book and can return
    path('return/',views.BookReturnView.as_view()),
    path('return/<int:pk>',views.BookReturnView.as_view()),

    # URL to see who borrowed the which book only admin-user can see
    path('borrowed/book/',views.BorrowedListBookView.as_view()),
    
]