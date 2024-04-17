from rest_framework import serializers
from .models  import Appartement

class AppartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appartement
        fields = '__all__'