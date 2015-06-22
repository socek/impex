from implugin.sqlalchemy.driver import ModelDriver

from .models import SampleData


class SampleDataDriver(ModelDriver):
    model = SampleData
