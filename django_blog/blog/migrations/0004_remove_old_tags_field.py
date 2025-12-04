# blog/migrations/0004_remove_old_tags_field.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_tag_alter_comment_post_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
    ]
