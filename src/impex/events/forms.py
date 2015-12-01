from formskit.converters import ToBool
from formskit.converters import ToDatetime
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreateEventForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('start_date', label='Data rozpoczęcia',
                       convert=ToDatetime())
        self.add_field('end_date', label='Data zakończenia',
                       convert=ToDatetime())
        self.add_field('is_visible', label='Widoczne', convert=ToBool())

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.events.create(
            name=data['name'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            is_visible=data['is_visible'],
        )
        self.database().commit()


class EditEventForm(CreateEventForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.instance.start_date = data['start_date']
        self.instance.end_date = data['end_date']
        self.instance.is_visible = data['is_visible']
        self.drivers.events.update(self.instance)

    def read_from(self, event):
        self.set_value('name', event.name)
        self.set_value('start_date', event.start_date)
        self.set_value('end_date', event.end_date)
        self.set_value('is_visible', event.is_visible)
        self.instance = event
