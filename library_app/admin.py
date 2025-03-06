from django.contrib import admin
from .models import Authortable,BooKtable #, BorrowedBooks
@admin.register(Authortable)
class AuthortableAdmin(admin.ModelAdmin):
    list_display=['id','author_name']
    
@admin.register(BooKtable)
class BooktableAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_cate','book_published_year','book_written_by','rating']

# @admin.register(BorrowedBooks)
# class BorrowAdmin(admin.ModelAdmin):
#     list_display=['user','book','borrow_date','return_date']