from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appartement
from .serializers import AppartementSerializer
from Reservation.serializers import ReservationSerializer
from Reservation.models import Reservation
from Users.models import User
import re
import json
from django.http import JsonResponse , Http404
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated])
class AppartementListCreateView(APIView):
    def get(self, request):
        search_term = request.data.get('search', None)
        if search_term is not None:
            appartements = Appartement.objects.filter(adresse__icontains=search_term )
        else:
            appartements = Appartement.objects.all()
        serializer = AppartementSerializer(appartements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppartementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(proprietaire=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class AppartementRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Appartement.objects.get(pk=pk)
        except Appartement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        appartement = self.get_object(pk)
        serializer = AppartementSerializer(appartement)
        return Response(serializer.data)

    def put(self, request, pk):
        appartement = self.get_object(pk)
        serializer = AppartementSerializer(appartement, data=request.data)
        if request.user != appartement.proprietaire :
            return Response({"message": "You can not access to this appartement "}, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appartement = self.get_object(pk)
        if request.user != appartement.proprietaire :
            return Response({"message": "You can not access to this appartement "}, status=status.HTTP_403_FORBIDDEN)
        
        appartement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@permission_classes([IsAuthenticated])
class ReservationCreateView(APIView):
    def post(self, request ,pk):
        appartement = Appartement.objects.filter(pk=pk).first()
        if appartement is None:
            return Response({"message": "Appartement not found"}, status=status.HTTP_404_NOT_FOUND
        )
        if appartement.proprietaire == request.user :
            return Response({"message": "You can not reserve your own appartement "}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the client to the user making the request
            serializer.save(client=request.user,appartement=appartement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)