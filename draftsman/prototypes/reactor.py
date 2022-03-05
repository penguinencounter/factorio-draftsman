# reactor.py

from draftsman.prototypes.mixins import Entity
from draftsman.errors import InvalidEntityID
from draftsman.utils import warn_user

from draftsman.data.entities import reactors


class Reactor(Entity):
    def __init__(self, name: str = reactors[0], **kwargs):
        if name not in reactors:
            raise InvalidEntityID("'{}' is not a valid name for this type"
                                  .format(name))
        super(Reactor, self).__init__(name, **kwargs)

        for unused_arg in self.unused_args:
            warn_user("{} has no attribute '{}'".format(type(self), unused_arg))