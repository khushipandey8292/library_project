from django.contrib import admin
from .models import Authortable,BooKtable,Borrow,Like_db
@admin.register(Authortable)
class AuthortableAdmin(admin.ModelAdmin):
    list_display=['id','author_name']
    
@admin.register(BooKtable)
class BooktableAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_cate','book_published_year','book_written_by','rating','book_sr_no','total_likes','available']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display=['id','user','book','issue_date','return_date']

@admin.register(Like_db)
class Like_dbAdmin(admin.ModelAdmin):
    list_display=['id','user','book','created_at']