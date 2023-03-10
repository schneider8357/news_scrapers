from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise, run_async


class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    profile_url = fields.TextField()

class Tag(Model):
    name = fields.TextField(pk=True)

class NewsArticle(Model):
    id = fields.IntField(pk=True)
    url = fields.TextField()
    author = fields.ManyToManyField('models.Author', related_name='author_name')
    tags = fields.ManyToManyField('models.Tag', related_name='tag_name')
    title = fields.TextField()
    subtitle = fields.TextField(null=True)
    lead = fields.TextField(null=True)
    section = fields.TextField()
    created_at = fields.DatetimeField()
    accessed_at = fields.DatetimeField()
    content_html = fields.TextField(null=True)
    content_txt = fields.TextField()



async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ["__main__"]}
    )
    await Tortoise.generate_schemas()

run_async(init())
