from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from .forms import SignupForm,LoginForm,RatingForm,Borrowform,RatingForm
from .forms import BookForm
from .models import BooKtable,Comment,Borrow,Bookrating
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now 
from datetime import date

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


def book_detail(request, book_id):
    book = get_object_or_404(BooKtable, id=book_id)
    user_rating =Bookrating.objects.filter(book=book, user=request.user).first()
    user_has_borrowed = book.borrow_set.filter(user=request.user, is_returned=False).exists()
    borrowed_books_count = Borrow.objects.filter(user=request.user, is_returned=False).values('book').distinct().count()
    user_reached_limit = borrowed_books_count >= 5

    return render(request, "book_detail.html", {
        "book": book,
        "user_has_borrowed": user_has_borrowed,
        "user_reached_limit": user_reached_limit,
        'user_rating':user_rating
    })


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


def add_rating(request, pk):
    book = get_object_or_404(BooKtable, id=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            rating, created = Bookrating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'user_rating': rating_value,}
            )
            return redirect('book-detail', book_id=pk)
    else:
        form = RatingForm()
    return render(request, 'rate_book.html', {'form': form, 'book': book})


def addcomment(request,id):
            book=BooKtable.objects.get(pk=id)
            comments = book.comment_set.all()
            if request.method == "POST":
                text = request.POST.get("text","").strip()
                if text:
                    Comment.objects.create(book=book, user=request.user,text=text)
                    return redirect('comment', id=book.id)
            return render(request,'comment.html',{'alldata':comments ,'book':book})
        
def book_like(request, id):
        comment = Comment.objects.get(pk=id)
        if request.user.is_authenticated:
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)  
            else:
                comment.likes.add(request.user)

        return redirect('comment', id=comment.book.id)
    

def borrow_book(request, book_id):
    book = get_object_or_404(BooKtable, id=book_id)
    already_borrowed = Borrow.objects.filter(user=request.user, book=book, is_returned=False).exists()
    if already_borrowed:
        messages.error(request, f"You have already borrowed '{book.book_name}'.")

    if request.method == "POST":
        form = Borrowform(request.POST)
        if form.is_valid():
            if book.available_copies > 0:
                borrow = form.save(commit=False)
                borrow.user = request.user
                borrow.book = book
                borrow.save()
                book.available_copies -= 1
                book.save()
                messages.success(request, f"You have borrowed '{book.book_name}'. Return by {borrow.due_date}.")
            else:
                messages.error(request, "Sorry, this book is currently not available.")
        else:
            messages.error(request, "Invalid data submitted.")
    else:
        form = Borrowform()

    return render(request, 'borrow_book.html', {"form": form, "book": book})


def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    
    if not borrow.is_returned:
        borrow.is_returned = True
        borrow.return_date = date.today()
        borrow.book.available_copies += 1
        borrow.book.save()
        borrow.save()

        messages.success(request, f"You have successfully returned '{borrow.book.book_name}'.")
    else:
        messages.warning(request, "This book is already returned.")

    return render(request, 'book_detail.html', {"book": borrow.book})
    


def my_borrowed_books(request):
    borrowed_books = Borrow.objects.filter(user=request.user).select_related('book')
    returned_books = borrowed_books.filter(is_returned=True)
    not_returned_books = borrowed_books.filter(is_returned=False)  

    return render(request, 'borrowed.html', {
        'borrowed_books':borrowed_books,
        'not_returned_books': not_returned_books,
        'returned_books': returned_books
    })






