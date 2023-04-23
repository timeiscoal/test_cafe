from rest_framework import serializers
from menus.models import Menu

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ["id","price","cost","name","description","barcode","expiration_date","categories","size",]


class MenuCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ["price","cost","name","description","barcode","expiration_date","categories","size",]