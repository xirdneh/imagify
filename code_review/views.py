from dateutil.relativedelta import relativedelta
from rest_framework import viewsets
from rest_framework.response import *
import json


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

def create(self, request):
        if not request.user.is_authenticated():
            return Response("You should be authenticated")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = request.POST["comment"]
            user = User.objects.create(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                comment=comment,
            response = {'code': 200, 'success': True, 'id': user.id}
            return Response(response)
        else:
            print ('error on the creation')
            return Response('error')
