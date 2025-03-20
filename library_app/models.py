from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.db.models import Avg
from datetime import timedelta,date
from django.core.validators import MaxValueValidator,MinValueValidator
class Authortable(models.Model):
    author_name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.author_name

class BooKtable(models.Model):
    authors=models.ManyToManyField(Authortable)
    book_name=models.CharField(max_length=60)
    book_sr_no=models.CharField(max_length=10, unique=True)
    book_cate=models.CharField(max_length=70)
    book_published_year=models.DateField()
    rating=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0.0)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    
    def book_written_by(self):
        return ",".join([str(p) for p in self.authors.all()])
    
    def __str__(self):
        return f"{self.book_name}  ({self.book_cate}/{self.book_sr_no})"
    
    def update_average_rating(self):
        ratings = Bookrating.objects.filter(book=self)
        total_ratings = ratings.count()
        if total_ratings > 0:
            average = sum(r.user_rating for r in ratings) / total_ratings
            self.rating = round(average, 2)  
        else:
            self.rating = 0.0
        self.save()
        
class Bookrating(models.Model):
    book = models.ForeignKey(BooKtable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])  
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_average_rating()
        
class Borrow(models.Model):
    book=models.ForeignKey(BooKtable,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    issue_date = models.DateField(auto_now_add=True)
    return_date=models.DateField(null=True,blank=True)
    due_date = models.DateField(default=date.today() + timedelta(days=7))
    is_returned = models.BooleanField(default=False)
        
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name} "

    def book_sr_no(self):
        return self.book.book_sr_no
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BooKtable, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(User,related_name='comment_likes', blank=True)
    
    def total_likes(self):
        return self.likes.count()
               

