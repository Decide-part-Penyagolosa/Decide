# Generated by Django 2.0 on 2022-01-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0012_auto_20220107_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='voting_type',
            field=models.SmallIntegerField(choices=[(0, 'Create your questions below'), (1, 'Dhont'), (2, 'Paridad'), (3, 'Borda')], default=0),
        ),
        migrations.AddField(
            model_name='questionoption',
            name='group',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.SmallIntegerField(choices=[(0, 'Create your questions below'), (1, 'Binary Question'), (2, 'Yes/No Question'), (3, 'Very Bad/ Very Good Question')], default=0),
        ),
    ]
