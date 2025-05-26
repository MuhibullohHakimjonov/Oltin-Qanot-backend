from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
	def create_user(self, phone_number, password=None, **extra_fields):
		if not phone_number:
			raise ValueError('Phone number is required')
		user = self.model(phone_number=phone_number, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	phone_number = models.CharField(max_length=15, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.phone_number


class Investor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
	company_name = models.CharField(max_length=255)
	inn = models.CharField(max_length=12, unique=True)
	address = models.TextField()
	company_owner = models.CharField(max_length=255, blank=True, null=True)
	company_email = models.EmailField(blank=True, null=True)
	company_website = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.company_name


class Volunteer(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
	profile_pic = models.ImageField(upload_to='images', blank=True, null=True)
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	address = models.TextField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	email = models.EmailField(blank=True, null=True)
	passport_num = models.CharField(max_length=9)

	def __str__(self):
		return f"{self.name} {self.surname}"


class PhoneVerification(models.Model):
	phone_number = models.CharField(max_length=20, unique=True)
	code = models.CharField(max_length=6)
	is_verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
