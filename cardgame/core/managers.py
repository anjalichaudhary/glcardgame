from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given username and password
        """
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        # using=self.db is required in case of handling multiple databases
        user.save(using=self.db)

        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user
