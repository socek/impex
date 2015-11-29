from implugin.formskit.models import PostForm as BasePostForm

from impex.application.requestable import Requestable


class PostForm(BasePostForm, Requestable):
    pass
