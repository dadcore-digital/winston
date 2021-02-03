from tortoise.models import Model
from tortoise import fields

class Stream(Model):
    
    class Meta:
        table = 'streaming_stream'

    id = fields.IntField(pk=True)
    stream_id = fields.IntField()
