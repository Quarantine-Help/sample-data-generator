from drf_extra_fields import geo_fields
from rest_framework import serializers, fields


class DataPacifierSerializer(serializers.Serializer):
    type = fields.ChoiceField(choices=("AF", "HL"), default="AF")
    position = geo_fields.PointField(str_points=True)
    amount = fields.IntegerField(max_value=20, min_value=1, default=1)
    target = fields.ChoiceField(choices=("staging", "production", "local"))
    authKey = fields.CharField()
