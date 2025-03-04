from django.db import models
from django.urls import reverse
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
    average_rating=models.DecimalField(max_digits=3,decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(5)],default=0)
    
    def book_written_by(self):
        return ",".join([str(p) for p in self.authors.all()])
    
    