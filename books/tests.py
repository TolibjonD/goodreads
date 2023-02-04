from django.test import TestCase
from django.urls import reverse
from books.models import Books

# Create your tests here.
class BookListTest(TestCase):
    def test_no_books_found(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, "No books found.")


    def test_books_list(self):
        book1 = Books.objects.create(title='title1' ,description= 'description1' ,isbn= '212132')
        book1 = Books.objects.create(title='title2' ,description= 'description2' ,isbn= '212132')
        book1 = Books.objects.create(title='title3' ,description= 'description3' ,isbn= '212132')
        response = self.client.get(reverse('books:list'))
        book_count = Books.objects.count()
        self.assertEqual(book_count, 3)
        books = Books.objects.all()
        for book in books:
            self.assertContains(response, book.title)
            self.assertContains(response, book.description)
            self.assertContains(response, book.isbn)
     
    def test_book_detail(self):
        book1 = Books.objects.create(title='title1' ,description= 'description1' ,isbn= '212132')
        response = self.client.get(reverse('books:detail', kwargs={"id":book1.id}))

        self.assertContains(response, book1.title)
        self.assertContains(response, book1.description)
        self.assertContains(response, book1.isbn)