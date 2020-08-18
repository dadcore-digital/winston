from tortoise.models import Model
from tortoise import fields

class Response(Model):
    
    class Meta:
        table = 'streaming_live'

    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=1024)
    shortcut = fields.CharField(max_length=64)
