from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_alter_chatmessage_options_alter_chatsession_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatsession",
            name="title",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
    ]
