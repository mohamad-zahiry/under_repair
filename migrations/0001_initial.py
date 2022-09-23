# Generated by Django 4.1.1 on 2022-09-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnderRepairRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='A short desctription about the rule', max_length=200)),
                ('is_active', models.BooleanField(default=False, help_text='Status of the rule')),
                ('admin_url', models.CharField(default='127.0.0.1:8000/admin', help_text='The admin page url without protocol and www.\ne.g: yahoo.com/admin', max_length=200)),
                ('view_path', models.CharField(default='under_repair.views.under_repair_view', help_text='Absolute path to your view.\ne.g: PROJECT_ROOT.APP.views.VIEW_NAME', max_length=200)),
            ],
            options={
                'verbose_name': 'Under Repair Rule',
                'verbose_name_plural': 'Under Repair Rules',
            },
        ),
    ]
