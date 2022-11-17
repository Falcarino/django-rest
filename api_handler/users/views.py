from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


class UsersView(APIView):
    def get(self, request, ids=None):
        if not ids:
            return Response({'user': 'All Users'}, status=HTTP_200_OK)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) == 1:
                return Response({'error': 'This user doesn\'t exist'}, status=HTTP_404_NOT_FOUND)
        return Response({'users': [{'id': uuid} for uuid in ids]})
