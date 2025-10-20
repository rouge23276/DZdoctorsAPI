from django.db.models import Count, Avg
from rest_framework import serializers 
from reviews.models import Doctor, Review, MedicalOrganization, PhoneNumberField

class MedicalOrganizationBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalOrganization
        fields = ('id', 'name')


class DoctorSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()  # Заменяем стандартное поле на пользовательский тип
    organizations = MedicalOrganization(many=True)  # Вложенный сериализатор для организаций

    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'specialization', 'phone_number', 'organizations')

    def get_full_name(self, obj):
        """Метод для получения полного имени врача."""
        return f"{obj.first_name} {obj.last_name}"
    

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
    
class PhoneNumberField(serializers.Field):
    def to_representation(self, value):
        """Форматирует телефонный номер для вывода."""
        if value:
            # Форматирование номера: (123) 456-7890
            return f"({value[:3]}) {value[3:6]}-{value[6:]}"
        return None

    def to_internal_value(self, data):
        """Проверяет и преобразует входное значение."""
        # Убираем все ненужные символы и проверяем длину
        value = data.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
        if len(value) == 10 and value.isdigit():
            return value
        raise serializers.ValidationError("Номер телефона должен быть в формате: 1234567890")
