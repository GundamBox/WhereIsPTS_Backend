from flask_marshmallow import Marshmallow
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter

from .channel import Channel
from .store import Store
from .vote import Vote

ma = Marshmallow()


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.List
    })


class GeoSerializationField(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if isinstance(value, WKBElement):
                geo_json = to_shape(value)
                return [geo_json.x, geo_json.y]
            else:
                return None


class VoteSchema(ma.ModelSchema):
    class Meta:
        model = Vote
        fields = ('cid', 'vote_count')
        exclude = ('sid', 'channel', 'store')


class ChannelSchema(ma.ModelSchema):
    class Meta:
        model = Channel
        fields = ('cid', 'name')
        exclude = ('stores',)


class StoreSchema(ma.ModelSchema):
    class Meta:
        model = Store
        model_converter = GeoConverter
        fields = ('sid', 'name', 'location', 'address',
                  'switchable', 'last_modified', 'votes')
        exclude = ('enable', 'disable_vote', 'last_ip')

    location = GeoSerializationField(attribute='location')
    votes = fields.Nested(VoteSchema, many=True)


channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)
store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)
vote_schema = VoteSchema()
votes_schema = VoteSchema(many=True)
