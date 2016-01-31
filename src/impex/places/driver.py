from implugin.sqlalchemy.driver import ModelDriver

from .models import Place


class PlaceDriver(ModelDriver):
    model = Place

    def list(self):
        return self.find_all()
