# Generated manually for school_year field addition

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0004_gradesummary_equivalent_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='school_year',
            field=models.CharField(default='25-1', help_text='Current active school year (e.g., 25-1)', max_length=20),
        ),
    ]