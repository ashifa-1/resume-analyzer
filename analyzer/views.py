from django.shortcuts import render
import os
from django.conf import settings
import PyPDF2
import re

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
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            # Clean text
            text = text.replace('\n', ' ')
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\s*-\s*', '-', text)

            # Skill list
            skills_list = [
                'python', 'java', 'c++', 'django', 'react', 'node.js',
                'machine learning', 'deep learning', 'nlp',
                'data structures', 'algorithms',
                'sql', 'mongodb', 'fastapi', 'docker'
            ]

            detected_skills = []
            text_lower = text.lower()

            for skill in skills_list:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    detected_skills.append(skill)

            preview_text = text[:1000]

            return render(request, 'home.html', {
                'message': 'File uploaded successfully',
                'text': preview_text,
                'skills': detected_skills
            })

    return render(request, 'home.html')