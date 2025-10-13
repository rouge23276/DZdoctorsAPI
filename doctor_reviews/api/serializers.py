from django.db.models import Count, Avg
from rest_framework import serializers 
from reviews.models import Doctor, Review

class DoctorSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialty', 'created_at', 'review_count', 'average_rating']

    def get_average_rating(self, obj):
        agg = obj.reviews.aggregate(avg=Avg('rating'))
        return agg['avg'] or 0

class ReviewSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'author_name', 'rating', 'text', 'created_at', 'parent', 'replies']
        read_only_fields = ['id', 'created_at']
    
    def get_replies(self, obj):
        """Рекурсивно получаем ответы на отзыв"""
        replies = obj.replies.all()
        if replies:
            return ReviewSerializer(replies, many=True).data
        return []
    
    def validate_rating(self, value):
        """Валидация рейтинга (1-5)"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value