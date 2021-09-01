from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack
# Create your tests here.
class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="leenhazaimeh94@gmail.com", password="0000"
        )

        self.snack = Snack.objects.create(
            title="purger", description='beef and toast', purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "purger")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "purger")
        self.assertEqual(f"{self.snack.purchaser}", "admin")
        self.assertEqual(f"{self.snack.description}", "beef and toast")

    def test_Snack_list_view(self):
        response = self.client.get(reverse("snacks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "purger")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_Snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser: admin")
        self.assertTemplateUsed(response, "snack_detail.html")

         

    def test_Snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "purger",
                "purchaser": self.user.id,
                "description": "beef and toast",
                
            }, follow=True
        )

       
        self.assertContains(response, "Details about purger")
    def test_thing_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated title","description":"purger with salat","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))
    def test_thing_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)