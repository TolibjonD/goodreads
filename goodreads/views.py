from django.shortcuts import render

def landing_page(request):
    return render(request, "landing_page.html")

def error_403(request, exception):
        return render(request,'403.html')

def error_404(request, exception):
    return render(request,'404.html')