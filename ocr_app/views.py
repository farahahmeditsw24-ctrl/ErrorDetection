import google.generativeai as genai
from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # لجلب المفتاح من settings.py

# إعداد Gemini باستخدام المفتاح الذي وضعناه في settings
genai.configure(api_key=settings.GEMINI_API_KEY)

def index(request):
    # اضيفي الكود هنا
    print("--- قائمة الموديلات المتاحة لحسابكِ هي: ---")
    try:
        available_models = genai.list_models()
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"الموديل المتاح هو: {m.name}")
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الموديلات: {e}")
    print("------------------------------------------")
    
    return render(request, 'index.html')

@csrf_exempt
def extract_text(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            img = Image.open(image_file)
            
            # الاسم الجديد حسب القائمة التي ظهرت في التيرمنال الخاص بكِ
            model_name = 'gemini-2.5-flash' 
            
            model = genai.GenerativeModel(model_name)
            
            # إرسال الصورة للمعالجة
            response = model.generate_content([
                "Extract all Arabic and English text from this image accurately. "
                "Keep the same line structure.", 
                img
            ])
            
            if response.text:
                return JsonResponse({'text': response.text})
            else:
                return JsonResponse({'error': 'لم يتم العثور على نص'}, status=200)

        except Exception as e:
            print(f"Detailed Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'No image uploaded'}, status=400)