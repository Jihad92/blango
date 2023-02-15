# Generated by Django 4.1.6 on 2023-02-13 10:40

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_authorprofile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["slug"]},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"ordering": ["value"]},
        ),
        migrations.AddField(
            model_name="post",
            name="hero_image",
            field=versatileimagefield.fields.VersatileImageField(
                blank=True, null=True, upload_to="hero_images"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="ppoi",
            field=versatileimagefield.fields.PPOIField(
                blank=True, default="0.5x0.5", editable=False, max_length=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="value",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]