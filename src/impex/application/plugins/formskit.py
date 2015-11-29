from implugin.formskit.models import PostForm as BasePostForm
from implugin.formskit.widget import FormWidget as BaseFormWidget

from impex.application.requestable import Requestable


class PostForm(BasePostForm, Requestable):
    pass


class FormWidget(BaseFormWidget):

    class Templates(BaseFormWidget.Templates):
        text = 'impex.application:templates/formskit/text.haml'
