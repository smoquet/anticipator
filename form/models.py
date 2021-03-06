from __future__ import unicode_literals

from django.db import models

# Custom field created for storing lists in the field
# for tests to see the input in the db

# class SeparatedValuesField(models.TextField):
#     __metaclass__ = models.SubfieldBase
#
#     def __init__(self, *args, **kwargs):
#         self.token = kwargs.pop('token', ',')
#         super(SeparatedValuesField, self).__init__(*args, **kwargs)
#
#     def to_python(self, value):
#         if not value: return
#         if isinstance(value, list):
#             return value
#         return value.split(self.token)
#
#     def get_db_prep_value(self, value, *args, **kwargs):
#         if not value: return
#         assert(isinstance(value, list) or isinstance(value, tuple))
#         return self.token.join([unicode(s) for s in value])
#
#     def value_to_string(self, obj):
#         value = self._get_val_from_obj(obj)
#         return self.get_db_prep_value(value)
#



class Events(models.Model):
    # By default, Django gives each model instantance an ID
    name = models.CharField(max_length=100, default='0000000')
    date = models.DateField()
    line_up = models.CharField(max_length=10000, default='0000000')
    source = models.CharField(max_length=1000, default='0000000')
    source_id = models.IntegerField(default='0000000')
