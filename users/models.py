import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
                Creates and saves a User with the given email, name
                and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        first_name = first_name
        last_name = last_name

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, names
        and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    """
        This model contains the user data.
        Its a custom user model that extends of django abstract user.
        """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identity
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Sobrenome")

    # Authentication
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Senha")

    # Status and permitions
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    is_staff = models.BooleanField(default=False, verbose_name="Pode acessar o Admin?")
    is_superuser = models.BooleanField(default=False, verbose_name="Super Usuário?")

    # Monitoring
    last_login = models.DateTimeField(null=True, verbose_name="Ultimo login")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultima atualização")

    # Associations
    groups = models.ManyToManyField(
        blank=True,
        help_text="Grupo ao qual o usuário pertence. O usuário recebe todas as permissões dos grupos ao qual ele pertence.",
        related_name="user_groups",
        related_query_name="user",
        to="auth.Group",
        verbose_name="Grupos de usuário",
    )

    user_permissions = models.ManyToManyField(
        blank=True,
        help_text="Permissões específicas do usuário.",
        related_name="user_permissions",
        related_query_name="user",
        to="auth.Permission",
        verbose_name="Permissões do usuário",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f'{self.first_name} - {self.email}'
