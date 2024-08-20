from django.db import models
import datetime


# Create your models here.
class Users(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    class Meta:
        db_table = "pereval_users"
        constraints = [
            models.UniqueConstraint(
                fields=["email", "phone"], name="unique_email_phone"
            )
        ]


class Coords(models.Model):
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    hight = models.IntegerField()

    class Meta:
        db_table = "pereval_coords"


class Levels(models.Model):
    winter = models.CharField(max_length=20, blank=True, null=True)
    summer = models.CharField(max_length=20, blank=True, null=True)
    autumn = models.CharField(max_length=20, blank=True, null=True)
    spring = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "pereval_levels"


class Pereval(models.Model):
    new = "new"
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"
    STATUS = [
        (new, "новая"),
        (pending, "в ожидании"),
        (confirmed, "подтверждена"),
        (rejected, "отклонена"),
    ]

    beauty_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    other_titles = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user")
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default=new, blank=False, choices=STATUS)
    connect = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "pereval"


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, blank=True)
    data = models.ImageField(upload_to="project/media", null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "pereval_images"