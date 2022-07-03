from unicodedata import name
from django.urls import path
from .views import getQuizes, getSingleQuiz, ResultsAPIView

urlpatterns = [
    path('', getQuizes, name='all-quizes'),
    path('<pk>', getSingleQuiz, name='single-quiz'),
    path('<pk>/save', ResultsAPIView.as_view(), name='save-results-view'),
]
