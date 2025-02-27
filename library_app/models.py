from django.db import models

class Authortable(models.Model):
    author_name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.author_name

class BooKtable(models.Model):
    authors=models.ManyToManyField(Authortable)
    book_name=models.CharField(max_length=60)
    book_cate=models.CharField(max_length=70)
    book_published_year=models.DateField()
    
    def book_written_by(self):
        return ",".join([str(p) for p in self.authors.all()])