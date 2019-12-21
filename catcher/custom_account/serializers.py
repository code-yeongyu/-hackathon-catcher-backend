from rest_framework import serializers
from custom_account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(Account.CHOICES)

    class Meta:
        model = Account
        fields = ("id", "role", "family_id", "phone_number", "notifications")