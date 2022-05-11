from django.contrib import admin
from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # URL for regester member
    path('register/', views.UserRegestrationView.as_view()),
    # URL for login both member and librarian
    path('login/',views.LoginView.as_view()),
    # URL for detail view of user and a user can delete account using delete http method
    path('detail/', views.UserDetailView.as_view(), name='detail'),
    # URL for register librarian 
    path('register/librarian/', views.LibrarianRegestrationView.as_view()),
    # URL for refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # A librarian can add delete update member
    path('accounts/', views.CRUDUserLibrarianView.as_view()),
    path('accounts/<int:pk>', views.CRUDUserLibrarianView.as_view()),
    
]