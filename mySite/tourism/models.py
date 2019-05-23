from django.db import models
# Create your models here.
class attractionsInfo(models.Model):
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

    # class Meta:
    #     managed = True
    #     db_table = 'attractionsinfo'


class userInfo(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    age = models.IntegerField(max_length=255)
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=255, blank=True, null=True)
    preference = models.TextField(blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'userinfo'