from django.contrib import admin
from .models import Books, Author, BookAuthor, BookReview

# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    list_display = ("title" , "isbn")
    search_fields = ("title", )
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name" , "last_name")
    search_fields = ("first_name", "last_name",)

class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ("title", )

admin.site.register(Books, BooksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(BookAuthor)

