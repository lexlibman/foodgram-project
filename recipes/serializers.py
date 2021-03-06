from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Favorite, Ingredient, Purchase, Subscription


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return self.Meta.model.objects.create(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class SubscriptionSerializer(CustomModelSerializer):
    class Meta:
        fields = ('author', )
        model = Subscription

    def validate_author(self, value):
        user = self.context['request'].user
        if user.id == value:
            raise ValidationError('Попытка подписаться на себя')
        return value


class FavoriteSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Favorite


class PurchaseSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Purchase
