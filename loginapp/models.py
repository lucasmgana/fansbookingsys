from django.db import models
from django.contrib.auth.models import AbstractUser, User

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )


    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Club(models.Model):
    name = models.CharField(max_length=244)
    location = models.CharField(max_length=244)
    fans_no = models.PositiveIntegerField()

    def __str__(self):
        return self.name


FAN_STATUS = (
    ('SAFE', 'SAFE'),
    ('BURNED', 'BURNED'),
)


class FanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=255, null=True, choices=FAN_STATUS)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        club = Club.objects.get(name=self.club)
        club.fans_no += 1
        club.save()
        return super().save(*args, **kwargs)


class Match(models.Model):
    home_team = models.CharField(max_length=244, null=True, blank=True)
    away_team = models.CharField(max_length=244, null=True, blank=True)
    date = models.DateTimeField()
    stadium = models.CharField(max_length=244, null=True, blank=True)

    def __str__(self):
        return str(self.home_team) + ' vs ' + str(self.away_team)


class MatchEntrace(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    vip_price = models.PositiveIntegerField()
    mzunguko_price = models.PositiveIntegerField()
    platnum_price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.match) + ' - VIP TSH.' + str(self.vip_price) + '/-, price '  + ' - MZUNGUKO TSH.' + str(self.mzunguko_price)  + '/-, PLATNUM TSH.' + str(self.platnum_price) + '/-'



class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    ticket_number = models.CharField(max_length=255)
    amount = models.PositiveIntegerField(null=True, blank=True)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.ticket_number) + " done by " + str(self.user)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    due_data  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Tsh." + str(self.amount) + '/- payed by ' + str(self.user)

