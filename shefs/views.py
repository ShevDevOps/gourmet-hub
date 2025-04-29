from django.shortcuts import render

# Create your views here.
def shefs(request):
    return render(request, 'shefs.html')

def shef_detail(request, shef_id):
    return render(request, 'shef_detail.html', {'shef_id': shef_id})