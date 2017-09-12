from implugin.formskit.models import PostForm
from formskit.validators import NotEmpty


class FirstForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('room', label='Pokoje')

    def on_success(self):
        pass
