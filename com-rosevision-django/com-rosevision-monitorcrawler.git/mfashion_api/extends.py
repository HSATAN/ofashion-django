__author__ = 'Zephyre'

from django.db import models
from datetime import datetime
from time import strftime


#
# Custom field types in here.
#

class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """

    def __init__(self, null=False, blank=False, **kwargs):
        if 'auto_updated' in kwargs:
            self.auto_updated = kwargs['auto_updated']
            kwargs.pop('auto_updated')
        else:
            self.auto_updated = False

        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True  # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ = ['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            if self.auto_updated:
                typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
            else:
                typ += ['default CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        return datetime.from_timestamp(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return None
        return strftime('%Y%m%d%H%M%S', value.timetuple())

        # def to_python(self, value):
        # return value
