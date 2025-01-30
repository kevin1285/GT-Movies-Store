from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import YourModel  # Replace with your actual model
from django.views import View

# Function-based view
def home(request):
    return render(request, 'home.html')

def get_data(request):
    data = list(YourModel.objects.values())  # Convert queryset to list of dicts
    return JsonResponse({"data": data})

# Class-based view
class DetailView(View):
    def get(self, request, pk):
        obj = get_object_or_404(YourModel, pk=pk)
        return render(request, 'detail.html', {'object': obj})
