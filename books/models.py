from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# ========= Books table goes here ========
class Books(models.Model):
    title       =models.CharField(max_length=200)
    description =models.TextField()
    isbn        =models.CharField(max_length=13)
    def __str__(self):
        return self.title
    


# ========= Author table goes here ===========
class Author(models.Model):
    first_name  =models.CharField(max_length=200)
    last_name   =models.CharField(max_length=200)
    email       =models.EmailField()
    bio         =models.TextField()
    def __str__(self):
        return self.first_name
    


# ========= BookAuthor table goes here =======
class BookAuthor(models.Model):
    author  =models.ForeignKey(Author, on_delete=models.CASCADE)
    book    =models.ForeignKey(Books, on_delete=models.CASCADE)


# ========= BookReview table goes here =======
class BookReview(models.Model):
    user        =models.ForeignKey(User, on_delete=models.CASCADE)
    book        =models.ForeignKey(Books, on_delete=models.CASCADE)
    comment     =models.TextField()
    stars_given =models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.user.username} rated {self.stars_given} for {self.book.title }"
    