from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # option 1
    # e.g Staff, Client, Manager, etc.
    # user_type = models.CharField(max_length=100)

    # # option 2
    # is_client = models.BooleanField(default=True)
    # is_manager = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username


# option 3
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # fields, properties, user types
    user_type = models.CharField(
        max_length=100,
        choices=(
            ("Reader", "Reader"),
            ("Writer", "Writer"),
            ("Coordinator", "Coordinator"),
            ("Moderator", "Moderator"),
        ),
        default="Reader",
    )

    def __str__(self):
        return self.user.username


class Column(models.Model):
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)
    writers = models.ManyToManyField(User, related_name="writers_columns")
    moderators = models.ManyToManyField(User, related_name="moderators_columns")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Column"
        verbose_name_plural = "Columns"

    def __str__(self):
        return self.name


class Post(models.Model):
    column = models.ForeignKey(
        Column, related_name="column_post", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """This is the link between a user and a column that they're subscripted to"""

    reader = models.ForeignKey(
        User, related_name="user_subscription", on_delete=models.CASCADE
    )
    column = models.ForeignKey(
        Column, related_name="column_subscription", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return self.reader.username + self.column.name


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_save_user_receiver, sender=User)
