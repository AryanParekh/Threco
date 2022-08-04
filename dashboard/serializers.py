from rest_framework import serializers
from .models import (SocietyCollection)


class SocietyCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyCollection
        fields = [
            "id",
            "society_name",
            "contact_person_name",
            "contact_no",
            "society_location",
            "employee_username",
            "glass",
            "paper",
            "metal",
            "mix_plastic",
            "pet_bottles",
            "mlp_packaging",
            "tetrapack",
            "cartons",
            "e_waste",
            "hazardous_waste",
            "other_waste",
            "date_of_activity",
        ]
