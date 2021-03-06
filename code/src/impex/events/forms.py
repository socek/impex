from formskit.converters import ToBool
from formskit.converters import ToDate
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreateEventForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('start_date', label='Data rozpoczęcia',
                       convert=ToDate())
        self.add_field('end_date', label='Data zakończenia',
                       convert=ToDate())
        self.add_field('is_visible', label='Opublikowane', convert=ToBool())
        self.add_field(
            'enable_twtitter',
            label='Włącz twittera',
            convert=ToBool(),
        )

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.events.create(
            name=data['name'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            is_visible=data['is_visible'],
            enable_twtitter=data['enable_twtitter'],
        )
        self.database().commit()


class EditEventForm(CreateEventForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.instance.start_date = data['start_date']
        self.instance.end_date = data['end_date']
        self.instance.is_visible = data['is_visible']
        self.instance.enable_twtitter = data['enable_twtitter']
        self.drivers.events.update(self.instance)
        self.database().commit()

    def read_from(self, event):
        self.set_value('name', event.name)
        self.set_value('start_date', event.start_date)
        self.set_value('end_date', event.end_date)
        self.set_value('is_visible', event.is_visible)
        self.set_value('enable_twtitter', event.enable_twtitter)
        self.instance = event
