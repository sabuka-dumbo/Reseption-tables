from django.shortcuts import render

def reception_table(request):
    return render(request, 'index.html')