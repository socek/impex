from datetime import datetime

from implugin.sqlalchemy.driver import ModelDriver

from .models import SliderEvent


class SliderEventDriver(ModelDriver):
    model = SliderEvent

    def list_for_command(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return self.find_all().filter(SliderEvent.when_created >= date)
