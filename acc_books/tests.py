from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Book

class TestBook(TestCase): 
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user('testuser','test@example.com','testpass1234')
        
        cls.book = Book.objects.create(
            abbr = "TB",
            name = "Test Book",
            guideline = "guideline for test book",
            currency_sign = "#",
            created_by = cls.user
        )
    
    def setUp(self):
        login = self.client.login(username='testuser',password='testpass1234')
        self.data = {
            abbr = "TB1",
            name = "Test Book1",
            guideline = "guideline for test book 1",
            currency_sign = "#1",
            created_by = cls.user
        }
        
    def test_book_content(self):
        self.assertEqual(self.book.abbr,"TB")
        self.assertEqual(self.book.name,"Test Book")
        self.assertEqual(self.book.guideline,"guideline for test book")
        self.assertEqual(self.book.currency_sign,"#")
        self.assertEqual(self.book.created_by.username,"testuser")
    
    def test_book_listview(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "General Ledger GL")

    def test_book_createview(self):
        response = self.client.get(reverse("book_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Book")

    def test_book_create(self):
        response = self.client.post(reverse("book_create", self.data))
        self.assertEqual(Book.objects.last().created_by.username, 'testuser')
    
    def test_book_updateview(self):
        response = self.client.get(reverse("book_update",kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update Book")

    def test_book_deleteview(self):
        response = self.client.get(reverse("book_delete",kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Book")