from django.contrib import admin
from .models import Authortable,BooKtable,Borrow,Comment,Bookrating

@admin.register(Authortable)
class AuthortableAdmin(admin.ModelAdmin):
    list_display=['id','author_name']
    
@admin.register(BooKtable)
class BooktableAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_cate','book_published_year','book_written_by','rating','book_sr_no','available_copies','total_copies']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display=['id','user','book','issue_date','return_date','due_date','is_returned']

@admin.register(Comment)
class CommonAdmin(admin.ModelAdmin):
    list_display=['id','user','text','total_likes']

@admin.register(Bookrating)
class Bookrating(admin.ModelAdmin):
    list_display=['id','user','book','user_rating']