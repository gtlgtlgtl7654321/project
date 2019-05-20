from django.db import models

# Create your models here.

class attrationsInfo(models.Model):
    districts = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    dataId = models.CharField(max_length=64)
    theme = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    productStarLevel = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    count = models.CharField(max_length=64)

    class Meta:
        managed = False  #如果设置为 False ，Django 将不会为当前 model 创建或者删除数据库表。如果你的测试中包含非托管 model (managed=False)，那么在测试之前，你应该要确保在测试创建时已经创建了正确的数据表。
        db_table = 'attrationsInfo'

# class userPreference(models.Model):
#     userId = models.CharField(max_length=255)
#     preference = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'userPreference'


class userInfo(models.Model):
    #userId = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=25)
    sex = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=25)
    preference = models.CharField(max_length=255)

    # class Meta:
    #     managed = True
    #     db_table = 'userInfo'
