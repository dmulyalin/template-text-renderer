from . import file_returner
from . import terminal_returner
from . import self_returner

returners_plugins = {
    "self": self_returner.dump,
    "file": file_returner.dump,
    "terminal": terminal_returner.dump
}