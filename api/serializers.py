from rest_framework import serializers
from professional_service.models import Professional_Service_Information, Client, User 
from professional.models import Professional_Information

# Serialization --> convert python data (from our database models) to JSON data

class ProfessionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional_Service_Information
        fields = '__all__'


# class ProjectSerializer(serializers.ModelSerializer):
#     owner = ProfileSerializer(many=False)
#     tags = TagSerializer(many=True)
#     reviews = serializers.SerializerMethodField()

#     class Meta:
#         model = Project
#         fields = '__all__'

#     def get_reviews(self, obj):
#         reviews = obj.review_set.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return serializer.data
