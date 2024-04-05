from rest_framework import serializers
from service_provider.models import ServiceProvider, Client, User 
from professional.models import Professional_Information

# Serialization --> convert python data (from our database models) to JSON data

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
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
