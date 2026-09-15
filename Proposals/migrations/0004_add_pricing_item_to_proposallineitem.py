from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Proposals", "0003_rename_apporved_by_proposal_approved_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposallineitem",
            name="pricing_item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="proposal_line_items",
                to="Proposals.pricingitem",
            ),
        ),
    ]
