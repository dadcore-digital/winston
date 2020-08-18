from tortoise.models import Model
from tortoise import fields

class Stream(Model):
    
    class Meta:
        table = 'streaming_stream'

    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255)
    user_name = fields.CharField(max_length=255)
    started_at = fields.DatetimeField(max_length=255)
    viewer_count = fields.IntField()
    twitch_id = fields.IntField()
    thumbnail_url = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
