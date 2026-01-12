from django.urls import path
from . import views # استيراد ملف views الذي سنضع فيه كود Gemini

urlpatterns = [
    path('', views.index, name='index'), # لفتح الصفحة الرئيسية
    path('extract-text/', views.extract_text, name='extract_text'), # الرابط الذي سينادي عليه الـ Javascript
]