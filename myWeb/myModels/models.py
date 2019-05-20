from django.db import models

# Create your models here.

class attrationsInfo(models.Model):
    districts = models.TextField()
    name = models.TextField()
    category = models.TextField()
    dataId = models.TextField()
    theme = models.TextField()
    level = models.TextField()
    productStarLevel = models.TextField()
    address = models.TextField()
    intro = models.TextField()
    price = models.TextField()
    count = models.TextField()

    class Meta:
        managed = False  #如果设置为 False ，Django 将不会为当前 model 创建或者删除数据库表。如果你的测试中包含非托管 model (managed=False)，那么在测试之前，你应该要确保在测试创建时已经创建了正确的数据表。
        db_table = 'attrationsInfo'

class userPreference(models.Model):
    userId = models.TextField()
    preference = models.TextField()

    class Meta:
        managed = False
        db_table = 'userPreference'


class userInfo(models.Model):
    userId = models.TextField()
    password = models.TextField()
    name = models.TextField()
    sex = models.TextField()
    age = models.TextField()
    address = models.TextField()
    tel = models.TextField()

    class Meta:
        managed = False
        db_table = 'userInfo'
