from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# Создаём настраиваемую модель User в Django, чтобы можно было бы использовать email в качестве основного идентификатора аутентификации вместо поля username.

# provides the helper functions for creating a user
class UserManager(BaseUserManager):
    # normalize_email is a fun from BaseUserManager
    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # support multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''Create and save a new superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that support using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Указываем, что все objects для класса происходят от UserManager
    objects = UserManager()
    # Задаем USERNAME_FIELD–для определения уникального идентификатора в модели User со значением email
    USERNAME_FIELD = 'email'
