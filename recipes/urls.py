from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import views
from recipes.views.api_views import (FavoriteViewSet, IngredientViewSet,
                                     PurchaseViewSet, SubscriptionViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register(
    'subscriptions',
    SubscriptionViewSet,
    basename='subscriptions',
)
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('purchases', PurchaseViewSet, basename='purchases')

recipes_urls = [
    path('new/', views.recipe_new, name='recipe_new'),
    path(
        '<int:recipe_id>/<slug:slug>/edit/',
        views.recipe_edit,
        name='recipe_edit',
    ),
    path(
        '<int:recipe_id>/<slug:slug>/delete/',
        views.recipe_delete,
        name='recipe_delete',
    ),
    path(
        '<int:recipe_id>/<slug:slug>/',
        views.recipe_view_slug,
        name='recipe_view_slug',
    ),
    path(
        '<int:recipe_id>/',
        views.recipe_view_redirect,
        name='recipe_view_redirect',
    ),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/', include(router.urls)),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path(
        'purchases/download/',
        views.purchases_download,
        name='purchases_download'
    ),
    path('recipe/', include(recipes_urls)),
    path('<str:username>/', views.profile_view, name='profile_view'),
]
