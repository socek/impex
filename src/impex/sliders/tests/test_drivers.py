from time import mktime

from impex.application.testing import DriverCase

from ..driver import SliderEvent
from ..driver import SliderEventDriver


class TestDriverSliderEvent(DriverCase):
    _object_cls = SliderEventDriver

    def test_list_for_command(self):
        self.flush_table_from_object(SliderEvent)
        event = self.object().create(name='one', value='two')
        self.database().commit()

        data = [obj.id for obj in self.object().list_for_command(0)]
        assert data == [event.id]

        data = [
            obj.id
            for obj in self.object().list_for_command(
                mktime(event.when_created.timetuple()) + 1
            )
        ]
        assert data == []
