from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        # Logic for handling GET requests to the home page
        return render(request, "frontend/home.html")
