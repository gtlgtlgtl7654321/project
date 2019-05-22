# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Attractionsinfo(models.Model):
    districts = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    dataid = models.CharField(db_column='dataId', max_length=64)  # Field name made lowercase.
    theme = models.CharField(max_length=255)
    level = models.CharField(max_length=255, blank=True, null=True)
    productstarlevel = models.CharField(db_column='productStarLevel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=255)
    intro = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    countid = models.CharField(db_column='countId', primary_key=True, max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attractionsinfo'


class Userinfo(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=255, blank=True, null=True)
    preference = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinfo'
