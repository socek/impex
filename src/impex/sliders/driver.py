from datetime import datetime

from implugin.sqlalchemy.driver import ModelDriver

from .models import SliderEvent
from .models import TabData


class SliderEventDriver(ModelDriver):
    model = SliderEvent

    def list_for_command(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return self.find_all().filter(SliderEvent.when_created >= date)


class TabDataDriver(ModelDriver):
    model = TabData

    def list(self):
        return self.find_all().filter(TabData.is_visible.is_(True))

    def admin_list(self):
        return self.find_all().order_by(TabData.id)
