from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator,MinValueValidator
class Authortable(models.Model):
    author_name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.author_name

class BooKtable(models.Model):
    authors=models.ManyToManyField(Authortable)
    book_name=models.CharField(max_length=60)
    book_cate=models.CharField(max_length=70)
    book_published_year=models.DateField()
    rating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0)
    
    def book_written_by(self):
        return ",".join([str(p) for p in self.authors.all()])
    
    def __str__(self):
        return self.book_name
    
class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User borrowing the book
    book = models.ForeignKey(BooKtable, on_delete=models.CASCADE)  # Book being borrowed
    borrow_date = models.DateField(auto_now_add=True)  # Borrow date
  
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"
   
    def borrow_book(self):
        return ",".join([str(p) for p in self.book.book_name])
   