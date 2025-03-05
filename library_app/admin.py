from django.contrib import admin
from .models import Authortable,BooKtable,BorrowRecord
@admin.register(Authortable)
class AuthortableAdmin(admin.ModelAdmin):
    list_display=['id','author_name']
    
@admin.register(BooKtable)
class BooktableAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_cate','book_published_year','book_written_by','rating']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display=['id','user','borrow_date','book']