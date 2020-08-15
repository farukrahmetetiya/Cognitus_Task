from django.urls import path

from .views import DataDetail, DataList, Prediction, Train


urlpatterns = [
    path('data/<int:pk>/', DataDetail.as_view()),
    path('data/', DataList.as_view()),
    path('prediction/', Prediction.as_view()),
    path('train/', Train.as_view()),
]
