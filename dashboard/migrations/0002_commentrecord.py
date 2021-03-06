# Generated by Django 3.2.5 on 2021-11-26 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('usercomment', models.TextField()),
                ('likecount', models.SmallIntegerField()),
                ('commentid', models.CharField(max_length=50)),
                ('publishingdate', models.DateTimeField()),
            ],
        ),
    ]
