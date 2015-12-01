from implugin.sqlalchemy.driver import ModelDriver

from .models import Event


class EventDriver(ModelDriver):
    model = Event

    def list_for_user(self):
        return (
            self.list_for_admin()
            .filter(self.model.is_visible.is_(True))
        )

    def list_for_admin(self):
        return (
            self.find_all()
            .order_by('-start_date')
        )
