from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import SignupForm,LoginForm,RatingForm,BorrowBookForm
from .forms import BookForm
from .models import BooKtable
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    return render(request,'index.html')


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations!! Account is created successfully!!')
            user=form.save()
            form=SignupForm()
    else:
      form=SignupForm()
    return render(request,'signup.html',{'form':form})

def user_login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password) 

        if user is not None:
            login(request, user)  

            if user.is_superuser:
                return HttpResponseRedirect("/admin_dashboard/")  
            else:
                return HttpResponseRedirect("/dashboard/") 
    else:
        form=LoginForm()
    return render(request, "login.html",{'form':form})   


def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/") 

    if request.user.is_superuser:
        return render(request, "admin_dashboard.html")  
    else:
        return render(request, "dashboard.html") 


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def search_book(request):
    query = request.GET.get('q','') 
    # book =  BooKtable.objects.all()

    if query: 
        book = BooKtable.objects.filter(Q(book_name__icontains=query)
                                        |Q(book_cate__icontains=query)
                                        |Q(book_published_year__icontains=query)
                                        |Q(authors__author_name__icontains=query))
    else:
        return HttpResponseRedirect('/')

    return render(request, "bookdetails.html", {"books": book, "query": query})

def create_book(request):
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)  
            book.save()  
            book.authors.set(form.cleaned_data['authors'])
            messages.success(request,'Book created successfully!')
            return redirect('book-create')
    else:
        form=BookForm()
    return render(request,'addbook.html',{'form':form})

def book_list(request):
    all_post=BooKtable.objects.all().order_by('id')
    paginator=Paginator(all_post,per_page=3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'book_list.html',{'books':page_obj})


def book_detail(request,pk):
    book=BooKtable.objects.get(pk=pk)
    return render(request,'book_detail.html',{'book':book})


def book_update(request,pk):
    book=BooKtable.objects.get(pk=pk)
    if request.method=="POST":
        form=BookForm(request.POST,instance=book)
        if form.is_valid():
            book = form.save(commit=False)  
            book.save()  
            book.authors.set(form.cleaned_data['authors'])
            messages.success(request,'Book-updated successfully!!')
            return redirect('book-update',pk=book.pk)
    else:
        form=BookForm(instance=book)
    return render(request,'addbook.html',{'form':form})

def book_delete(request,pk):
    book=BooKtable.objects.get(pk=pk)
    book.delete()
    messages.success(request,"Book deleted successfully!!")
    return redirect('book-list')


def rate_book(request, pk):
    book =BooKtable.objects.get (pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-detail', pk=book.pk)
    else:
        form = RatingForm(instance=book)
    
    return render(request, 'rate_book.html', {'form': form, 'book': book})

from django.shortcuts import render, get_object_or_404, redirect


def borrow_book(request):
        if request.method == 'POST':
            form = BorrowBookForm(request.POST)
            if form.is_valid():
              form.save()
              form=BorrowBookForm()
        else:
            form = BorrowBookForm()
        return render(request, 'borrow_book.html', {'form': form})
    
