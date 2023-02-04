from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from .models import Books, BookReview
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.

class BookListView(LoginRequiredMixin, View):
    def get(self, request):
        books = Books.objects.all().order_by('-id')
        search = request.GET.get('q')
        if search:
            books = Books.objects.filter(title__icontains=search)
        paginator = Paginator(books, 7)
        page = request.GET.get('page', 1)
        pages = paginator.get_page(page)
        return render(request, "books/book-list.html", {"pages":pages})

class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Books.objects.get(id=id)
        form = ReviewForm()
        return render(request, "books/detail.html", {"book":book , "form":form})

class AddReview(LoginRequiredMixin, View):
    def post(self, request, id):
        form = ReviewForm(data=request.POST)
        book = Books.objects.get(id=id)
        if form.is_valid():
            BookReview.objects.create(
                user = request.user,
                book = book,
                comment = form.cleaned_data['comment'],
                stars_given = form.cleaned_data['stars_given']
            )
            return redirect(reverse('books:detail', kwargs={'id':book.id}))
        else:
            return render(request, "books/detail.html", {"book":book , "form":form})
