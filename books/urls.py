from django.urls import path
from .views import BookListView, BookDetailView, AddReview


app_name = 'books'
urlpatterns = [
    path('<int:id>/', BookDetailView.as_view(), name='detail' ),
    path('<int:id>/reviews/' , AddReview.as_view() , name='reviews') ,
    path('', BookListView.as_view(),  name='list'),
]
