# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BatchComparison(models.Model):
    batch = models.CharField(primary_key=True, max_length=9)
    shooting_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    model = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    stylist = models.CharField(max_length=60, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_comparison'


class SpuidComparison(models.Model):
    batch = models.ForeignKey(BatchComparison, models.DO_NOTHING, db_column='batch', blank=True, null=True)
    spuid = models.CharField(primary_key=True, max_length=12)
    store = models.CharField(max_length=40, blank=True, null=True)
    brand = models.CharField(max_length=10, blank=True, null=True)
    shelf_time = models.DateField(blank=True, null=True)
    style_coding = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spuid_comparison'


class StoreDailyData(models.Model):
    date = models.DateField()
    brand = models.CharField(max_length=10)
    terminal = models.CharField(max_length=10)
    spuid = models.CharField(primary_key=True, max_length=12)
    title = models.CharField(max_length=62, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    pv = models.IntegerField(db_column='PV', blank=True, null=True)  # Field name made lowercase.
    uv = models.IntegerField(db_column='UV', blank=True, null=True)  # Field name made lowercase.
    residence_time = models.FloatField(blank=True, null=True)
    bounce_rate = models.FloatField(blank=True, null=True)
    order_conversion_rate = models.FloatField(blank=True, null=True)
    conversion_rate_of_order_payment = models.FloatField(blank=True, null=True)
    conversion_rate_of_payment = models.FloatField(blank=True, null=True)
    single_amount = models.FloatField(blank=True, null=True)
    number_of_order_items = models.IntegerField(blank=True, null=True)
    number_of_buyers = models.IntegerField(blank=True, null=True)
    amount_of_payment = models.FloatField(blank=True, null=True)
    payment_of_goods = models.IntegerField(blank=True, null=True)
    number_of_additional_purchases = models.IntegerField(blank=True, null=True)
    average_visitor_value = models.FloatField(blank=True, null=True)
    number_of_clicks = models.IntegerField(blank=True, null=True)
    clicking_rate = models.FloatField(blank=True, null=True)
    exposure = models.IntegerField(blank=True, null=True)
    collection_number = models.IntegerField(blank=True, null=True)
    search_guided_payment_of_buyers = models.IntegerField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    search_conversion_rate = models.FloatField(blank=True, null=True)
    number_of_visitors_guided_by_search = models.IntegerField(blank=True, null=True)
    number_of_buyers_paid = models.IntegerField(blank=True, null=True)
    successful_refund_amount_after_sale_and_after_sale = models.FloatField(blank=True, null=True)
    successful_refund_of_sales_after_sale = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_daily_data'
        unique_together = (('spuid', 'date', 'terminal'),)
