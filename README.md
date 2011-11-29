A collection of Django templatetags, context processors, middleware, mixins and other reusable hacks.

* admin
    - actions.py: a new delete action for the admin interface, which does call the delete function per object
    - admin.py: base classes to subclass from
* forms
    - patch.py: patches Django forms to set default css classes on inputs (for client-side validation and styling)
    - widgets.py: useful widgets for forms and modelforms
    - imagewidget.py: an image widget which shows a thumbnail of the current image (needs sorl.thumbnail)
* views
    - mixins.py: handy mixins for Class Based Views (for Django 1.3)
* models
    - fields.py: new model fields, for example an integer field with support for min/max values
* templatetags
    - vrot.py: templatetags and -filters
