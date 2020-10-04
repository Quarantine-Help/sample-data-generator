from drf_extra_fields import geo_fields
from rest_framework import serializers, fields


class DataPacifierSerializer(serializers.Serializer):
    type = fields.ChoiceField(choices=("AF", "HL", ), default="AF")
    position = geo_fields.PointField(str_points=True)
    amount = fields.IntegerField()
    target = fields.ChoiceField(choices=("staging", "production",))
