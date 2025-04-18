"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from library_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('user_login/',views.user_login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path("admin_dashboard/",views.dashboard, name="admin_dashboard"),
    path('user_logout/',views.user_logout,name='logout'),
    path("search/", views.search_book, name="search_book"),
    path('create/',views.create_book,name='book-create'),
    path('show/',views.book_list,name="book-list"),
    path('book/<int:book_id>/',views.book_detail,name='book-detail'),
    path('book/<int:pk>/edit/',views.book_update,name='book-update'),
    path('book/<int:pk>/delete/',views.book_delete,name='book-delete'),
    path('rate/<int:pk>/',views.add_rating, name='add-rating'),
    path('comments/<int:id>/',views.addcomment,name='comment'),
    path('like/<int:id>/',views.book_like, name='like-book'),
    path('borrow/<int:book_id>/',views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),
    path('oauth/',include('social_django.urls',namespace='social')),
]
  