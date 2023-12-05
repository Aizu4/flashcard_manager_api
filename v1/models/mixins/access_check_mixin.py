from django.contrib.auth.models import User


class AccessCheckMixin:
    user: User
    public: bool

    def is_visible_for(self, user: User) -> bool:
        return user.is_superuser or self.user == user or self.public

    def is_editable_for(self, user: User) -> bool:
        return user.is_superuser or self.user == user
