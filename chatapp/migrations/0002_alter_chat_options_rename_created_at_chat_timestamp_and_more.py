# Generated by Django 5.1.3 on 2024-12-01 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['timestamp']},
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='recipient',
        ),
        migrations.AlterField(
            model_name='chat',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='chatapp.group'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sender', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatapp.group')),
            ],
        ),
    ]