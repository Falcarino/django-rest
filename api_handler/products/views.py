from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound, ParseError

from .models import Product
from .serializers import ProductSerializer

class IDNotFound(NotFound):
    def __init__(self, id):
        message = f'ID {id} not found.'
        super().__init__(message)

# Perhaps make a generic view metaclass?
class ProductsView(APIView):

    def __get_products_queryset(self, ids):
        """
        Collects all existing product ids provided in a request.
        If at least one provided id doesn't exists, returns error 404.
        Used for GET and DELETE handlers.

            Parameters:
            -----------
                ids : str
                    User ids to search for

            Returns:
            -----------
                products_qs : querySet
                    A query set, containing all found products
        """
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
        """
        GETs several or all products, depending on whether any ids were provided or not.

            Parameters:
            -----------
                ids : str
                    Product ids to search for. If none provided, GET all existing products.

            Returns:
            -----------
                A json array of found products.
        """
        if not ids:
            products = Product.objects.all()
        if ids:
            products = self.__get_products_queryset(ids)

        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, ids=None):
        """
        POSTs one or several products.

            Parameters:
            -----------
                request : http.HttpRequest
                    HTTP request from which the function gets json data.
                ids : None
                    There should no input for this function.

            Returns:
            -----------
                A json array of newly added products.
        """
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
        """
        PUTs a product.

            Parameters:
            -----------
                request : http.HttpRequest
                    HTTP request from which the function gets json data.
                ids : str
                    Id of an existing product.

            Returns:
            -----------
                Updated json data of the product.
        """
        if not ids:
            raise NotFound('Cannot update None.')
        if ids:
            try:
                id = int(ids)
            except:
                raise ParseError('Bad request. Only one product can be updated')

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
        """
        DELETEs several or all products.

            Parameters:
            -----------
                ids : str
                    Product ids up for removal. If none provided, DELETE all existing products.

            Returns:
            -----------
                An empty json array.
        """
        if not ids:
            products = Product.objects.all()
        if ids:
            products = self.__get_products_queryset(ids)

        serializer = ProductSerializer(products, many=True)
        products.delete()
        return JsonResponse(serializer.data, safe=False, status=200)

class UserProductsView(APIView):
    
    def get(self, request, user_id=None):
        """
        GETs all products tied to a specific user.

            Parameters:
            -----------
                user_id : int
                    Id of the user to look up

            Returns:
            -----------
                A json array of all products tied to the requested user.
        """
        if not user_id:
            raise ParseError('Bad request.') 
        if user_id:
            products = Product.objects.filter(user_id=user_id)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
