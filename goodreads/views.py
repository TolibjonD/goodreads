from django.shortcuts import render
from books.models import BookReview
from django.core.paginator import Paginator

def landing_page(request):
    return render(request, "landing_page.html")

def error_403(request, exception):
        return render(request,'403.html')

def error_404(request, exception):
    return render(request,'404.html')

def home_page(request):
    reviews = BookReview.objects.all().order_by('-created_at')
    search = request.GET.get('q' , '')
    if search:
        reviews = BookReview.objects.all().filter(comment__icontains=search)
    paginator = Paginator(reviews, 5)
    current_page = request.GET.get('page' , 1)
    pages = paginator.get_page(current_page)
    return render(request, "home.html", {'pages':pages, "search":search})