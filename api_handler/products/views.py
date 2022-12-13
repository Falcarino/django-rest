from django.http import JsonResponse
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class IDNotFound(NotFound):
    def __init__(self, id):
        message = f'ID {id} not found.'
        super().__init__(message)


# Perhaps make a generic view metaclass?
class ProductsView(APIView):

    def __get_products_queryset(self, ids):
        try:
            ids = ids.strip().split(',')
        except:
            raise NotFound("No products found.")

        products_qs = Product.objects.none()
        for id in ids:
            product = Product.objects.filter(product_id=id)
            if product.exists():
                products_qs = product | products_qs
            else:
                raise IDNotFound(id)
        return products_qs

    def get(self, request, ids=None):
        if not ids:
            products = Product.objects.all()
        if ids:
            products = self.__get_products_queryset(ids)

        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, ids=None):
        if not ids:
            parsed_data = JSONParser().parse(request)
            new_data = []
            for product in parsed_data['products']:
                serializer = ProductSerializer(data=product)
                if serializer.is_valid():
                    serializer.save()
                    new_data.append(serializer.data)

            return JsonResponse(new_data, safe=False, status=201)
        raise ParseError('Bad request.')

    def put(self, request, ids=None):
        if not ids:
            raise NotFound('Cannot update None.')
        if ids:
            try:
                id = int(ids)
            except:
                raise ParseError('Bad request. Only one user can be updated')

            try:
                product = Product.objects.get(product_id=id)
                new_data = JSONParser().parse(request)

                for field, value in new_data.items():
                    setattr(product, field, value)

                serializer = ProductSerializer(product, data=new_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=200)
            except:
                raise IDNotFound(id)
        raise ParseError('Bad request.')

    def delete(self, request, ids=None):
        if not ids:
            products = Product.objects.all()
        if ids:
            products = self.__get_products_queryset(ids)

        serializer = ProductSerializer(products, many=True)
        products.delete()
        return JsonResponse(serializer.data, safe=False, status=200)


class UserProductsView(APIView):

    def get(self, request, user_id=None):
        if not user_id:
            raise ParseError('Bad request.')
        if user_id:
            products = Product.objects.filter(user_id=user_id)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
