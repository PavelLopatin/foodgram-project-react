from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# from backend.pagination import CustomPageNumberPaginator

from .filters import IngredientsFilter, RecipeFilter
from .models import (Ingredient, RecipeIngredients, Tag,
                     Recipe, Favorite, ShoppingList)
from .serializers import (IngredientsSerializer, TagsSerializer,
                          ShowRecipeFullSerializer, AddRecipeSerializer,
                          FavouriteSerializer, ShoppingListSerializer)
from .permissions import IsAuthorOrAdmin


class RetriveAndListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = None
    filterset_class = IngredientsFilter


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ShowRecipeFullSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(data=data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = get_object_or_404(ShoppingList,
                                          user=user, recipe=recipe)
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user_shopping_list = request.user.shopping_list.all()
        ingredients = {}
        for recipe in user_shopping_list:
            ingredient_filter = RecipeIngredients.objects.filter(recipe=recipe.recipe)
            for ingredient in ingredient_filter:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in ingredients:
                    ingredients[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    ingredients[name]['amount'] += amount
        purchase = []
        for item in ingredients:
            purchase.append(f'{item} - {ingredients[item]["amount"]} '
                          f'{ingredients[item]["measurement_unit"]} \n')
        response = HttpResponse(purchase, 'Content-Type: text/plain')
        response['Content-Disposition'] = f'attachment; filename=purchase.txt'
        return response

