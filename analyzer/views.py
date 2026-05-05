from django.shortcuts import render
import os
from django.conf import settings
import PyPDF2
import re

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('resume')
        job_desc = request.POST.get('job_desc')

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

            # Clean resume text
            text = text.replace('\n', ' ')
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\s*-\s*', '-', text)

            preview_text = text[:1000]

            matched_keywords = []
            score = 0

            if job_desc:
                jd_text = job_desc.lower()
                jd_text = re.sub(r'\s+', ' ', jd_text)

                # remove common words
                stopwords = {'and', 'the', 'with', 'for', 'in', 'of', 'to', 'a', 'on', 'is', 'are'}

                jd_keywords = [word for word in jd_text.split() if word not in stopwords and len(word) > 2]

                jd_keywords = list(set(jd_keywords))  # remove duplicates

                resume_text = text.lower()

                for word in jd_keywords:
                    if word in resume_text:
                        matched_keywords.append(word)

                if len(jd_keywords) > 0:
                    score = int((len(matched_keywords) / len(jd_keywords)) * 100)

            return render(request, 'home.html', {
                'message': 'File uploaded successfully',
                'text': preview_text,
                'score': score,
                'matched_keywords': matched_keywords[:20]
            })

    return render(request, 'home.html')