from js.jquery import jquery
from js.bootstrap import bootstrap
from impex.home.resources import home

statics = {
    'jquery': jquery,
    'bootstrap': bootstrap,
    'home': home,
}


def static_need(name):
    statics[name].need()
    return ''
