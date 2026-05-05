from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('resume')
        if uploaded_file:
            return render(request, 'home.html', {'message': 'File uploaded successfully'})
    return render(request, 'home.html')