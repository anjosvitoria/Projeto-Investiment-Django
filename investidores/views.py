from django.shortcuts import render

# Create your views here.
def sugestao(request):
    if request.method == 'GET':
        return render(request, 'sugestao.html')
    
    
