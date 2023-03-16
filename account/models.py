# from django.db import models

# # Create your models here.


# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser
# from django.utils.crypto import get_random_string # функция которая будет гененрировать рандомную стороку



# class UserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email fields is requirement')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password) # хеширование пароля под капотом
#         user.create_activation_code()
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()
#         return user


# class User(AbstractBaseUser):
#     username = None # если мы хотим чтобы логинились через емецл
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=10, blank=True)# поле для ввода кода


#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [] # запрашивает поле для заполнения

#     def __str__(self) -> str:
#         return f'{self.email} -> {self.id}'

#     # джейсон токен - уменьшает количество запрросов в базу данных, также дживити токен получет 2 токена - аутентициакаяция и обнговление предыдущего токена, также мы можем указать срок его жизни(боллее защищенный)

#     def create_activation_code(self):
#         code = get_random_string(length=10, allowed_chars='1234567890)(*&^%$#@!') # длинна кода и из каких символов
#         self.activation_code = code
#         self.save()


from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email fields is requirement')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_superuser(self,email, password, **extra_fields):
        if not email:
            raise ValueError(
                'Email is required'
            )

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def str(self):
        return f'{self.email} -> {self.id}'

    def create_activation_code(self):
        code = get_random_string(
            length=10,
            allowed_chars='1234568@$%^&&*_'
        )
        self.activation_code = code