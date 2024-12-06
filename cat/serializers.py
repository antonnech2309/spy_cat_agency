import requests
from rest_framework import serializers
from .models import SpyCat


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ["id", "name", "experience", "breed", "salary"]

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative.")
        return value

    def validate_breed(self, value):
        response = requests.get("https://api.thecatapi.com/v1/breeds/")
        if response.status_code != 200:
            raise serializers.ValidationError("Unable to fetch breed data at the moment.")

        breeds = [breed['name'] for breed in response.json()]
        if value not in breeds:
            raise serializers.ValidationError(f"'{value}' is not a valid breed. Please provide a valid breed.")
        return value