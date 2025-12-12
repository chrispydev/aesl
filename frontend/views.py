from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        context = {
            'title': "HomePage"
        }
        return render(request, "frontend/home.html", context)
