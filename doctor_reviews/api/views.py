from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from reviews.models import Doctor, Review
from .serializers import DoctorSerializer, ReviewSerializer
from rest_framework import viewsets

class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_id):
    """GET: детали отзыва, PUT: обновление, DELETE: удаление"""
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_reply(request, review_id):
    """Создание ответа на отзыв"""
    parent_review = get_object_or_404(Review, id=review_id)
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        # Сохраняем ответ с привязкой к родительскому отзыву и тому же врачу
        serializer.save(parent=parent_review, doctor=parent_review.doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
