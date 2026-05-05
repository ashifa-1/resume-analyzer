from django.shortcuts import render
import os
from django.conf import settings
import PyPDF2

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('resume')
        if uploaded_file:
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            text = ""

            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()

            return render(request, 'home.html', {
                'message': 'File uploaded successfully',
                'text': text
            })

    return render(request, 'home.html')