from . import multitemplate_processor
from . import templates_split
from . import filtering

processors_plugins = {
    "multitemplate": multitemplate_processor.process,
    "templates_split": templates_split.process,
    "filtering": filtering.process
}