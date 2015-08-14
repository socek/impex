from formskit.validators import NotEmpty
from implugin.formskit.models import PostForm

from impex.application.requestable import Requestable


class CreateForm(PostForm, Requestable):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.Orders.create(
            name=data['name'],
        )
