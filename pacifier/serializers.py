from rest_framework import serializers, fields


class DataPacifierSerializer(serializers.Serializer):
    type = fields.CharField()
    amount = fields.IntegerField()
