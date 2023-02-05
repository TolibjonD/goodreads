from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
# ========= Books table goes here ========
class Books(models.Model):
    title       =models.CharField(max_length=200)
    description =models.TextField()
    isbn        =models.CharField(max_length=13)
    photo       =models.ImageField(upload_to='books/', default='book.png')
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
    def full_name(self):
        return f"{self.author.first_name} {self.author.last_name}"
# ========= BookReview table goes here =======
class BookReview(models.Model):
    user        =models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book        =models.ForeignKey(Books, on_delete=models.CASCADE)
    comment     =models.TextField()
    stars_given =models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at  =models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user.username} rated {self.stars_given} for {self.book.title }"
    