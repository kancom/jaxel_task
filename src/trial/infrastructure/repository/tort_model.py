from tortoise import fields, models


class QuoteModel(models.Model):
    quote_id = fields.IntField(pk=True)
    pair = fields.CharField(max_length=50, null=True)
    ts = fields.DatetimeField(auto_now_add=True)
    rate = fields.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        table = "quote"
