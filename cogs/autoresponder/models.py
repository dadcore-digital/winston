from tortoise.models import Model
from tortoise import fields

class Response(Model):
    
    class Meta:
        table = 'autoresponder_response'

    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=1024)
    shortcut = fields.CharField(max_length=64, unique=True)
