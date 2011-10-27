"""
Monkey patches Django forms to automatically give fields validation classes
for use with client side validation using jquery.validate and jquery.metadata

Use:
# in urls.py:
from vrot.forms import patch
"""

from django.forms.forms import BoundField
from django.forms.fields import *
from django.forms.widgets import TextInput, PasswordInput

original_function = BoundField.as_widget

def as_widget(self, widget=None, attrs=None, only_initial=False):
    """
    Renders the field by rendering the passed widget, adding any HTML
    attributes passed as attrs.  If no widget is specified, then the
    field's default widget will be used.

    This patched version adds css classes to the field, used
    for client side validation.
    """
    attrs = attrs or {}
    validate = []
    extra_classes = []

    opts = self.field.__dict__

    if opts.get('required'):
        validate.append('required:true')

    if opts.get('min_length'):
        validate.append('minlength:%d' % self.field.max_length)

    if opts.get('max_length'):
        validate.append('maxlength:%d' % self.field.max_length)

    if opts.get('min_value'):
        validate.append('min:%d' % self.field.min_value)

    if opts.get('max_value'):
        validate.append('max:%d' % self.field.max_value)

    if isinstance(self.field, (IntegerField,)):
        validate.append('digits:true')
        extra_classes.append('numericonly')

    if isinstance(self.field, (FloatField,)) or isinstance(self.field, (DecimalField,)):
        validate.append('number:true')
        extra_classes.append('decimalonly')

    if isinstance(self.field, (EmailField,)):
        validate.append('email:true')

    if isinstance(self.field, (URLField,)):
        validate.append('url:true')

    if isinstance(opts.get('widget'), (TextInput,PasswordInput)):
        extra_classes.append('input_type_text')

    if validate:
        if not widget:
            widget = self.field.widget

        current = widget.attrs.get('class') or ''
        if current:
            extra_classes.append(current)

        extra_classes.append('{validate: {%s}}' % ', '.join(validate))

        attrs['class'] = ' '.join(extra_classes)

    # Call the original, unaltered function with the updated attrs parameter
    return original_function(self, widget, attrs, only_initial)

# Monkey patch the original function
BoundField.as_widget = as_widget
