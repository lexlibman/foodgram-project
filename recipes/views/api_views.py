from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Subscription
from recipes.permissions import IsOwnerOrAdmin
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 PurchaseSerializer, SubscriptionSerializer)


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):

    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            **kwargs,
        }

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response(
            {'success': bool(success)},
            status=status.HTTP_204_NO_CONTENT,
        )


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title',)


class SubscriptionViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    lookup_field = 'author'


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    lookup_field = 'recipe'


class PurchaseViewSet(mixins.ListModelMixin, CreateDestroyViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe'

    def get_queryset(self):
        return self.request.user.purchases.all()
