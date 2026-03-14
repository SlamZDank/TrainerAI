import uuid
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_userprofile_id'),
    ]

    operations = [
        # Fix choice values (choice strings only, no schema change)
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('prefer_not_to_say', 'Prefer Not To Say')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fitness_goal',
            field=models.CharField(max_length=20, choices=[('lose_weight', 'Lose Weight'), ('build_muscle', 'Build Muscle'), ('improve_endurance', 'Improve Endurance'), ('general_wellness', 'General Wellness')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='activity_level',
            field=models.CharField(max_length=20, choices=[('sedentary', 'Sedentary'), ('lightly_active', 'Lightly Active'), ('moderately_active', 'Moderately Active'), ('very_active', 'Very Active')]),
        ),
        # Remove null=True from weight/height fields (table is empty in dev)
        migrations.AlterField(
            model_name='userprofile',
            name='current_weight_kg',
            field=models.DecimalField(max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(500)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height_cm',
            field=models.DecimalField(max_digits=5, decimal_places=1, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(300)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='target_weight_kg',
            field=models.DecimalField(max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(500)]),
        ),
        # Add dietary_preferences default and health_notes
        migrations.AlterField(
            model_name='userprofile',
            name='dietary_preferences',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='health_notes',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        # Add related_name to user FK
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=models.CASCADE, related_name='profile', to='authentication.user'),
        ),
    ]
