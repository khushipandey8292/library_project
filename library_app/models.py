from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator,MinValueValidator
class Authortable(models.Model):
    author_name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.author_name

class BooKtable(models.Model):
    authors=models.ManyToManyField(Authortable)
    book_name=models.CharField(max_length=60)
    book_sr_no=models.IntegerField(unique=True)
    book_cate=models.CharField(max_length=70)
    book_published_year=models.DateField()
    rating=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0.0)
    available = models.BooleanField(default=True)
    
    def book_written_by(self):
        return ",".join([str(p) for p in self.authors.all()])
    
    def __str__(self):
        return self.book_name
    
    def total_likes(self):
        return self.likes.count()
    
class Borrow(models.Model):
    book=models.ForeignKey(BooKtable,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    issue_date = models.DateField(auto_now_add=True)
    return_date=models.DateField(null=True,blank=True)

        
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"

            
class Like_db(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BooKtable, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        unique_together = ('user', 'book') 

    def __str__(self):
        return f"{self.user.username} likes {self.book.book_name}"
    
   

    
