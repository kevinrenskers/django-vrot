import re
from django import template
from django.contrib import messages
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

@register.simple_tag
def active(request, pattern, exact_match_only=False, extra_pattern=''):
    """
    Check if current url is active according to pattern or extra pattern.

    Args:
        request: a Django <Request> object
        pattern: either a string of a relative url, or a regular expression pattern
        exact_match_only: bool, set to true if `pattern` can only be seen as an url, not as a regex
        extra_pattern: see `pattern`. The `exact_match_only` arg does not apply to this one

    Example:
        {% load vrot %}
        {% url my_page as uri %} <a href="{{ uri }}"{% active request uri %}>My Page</a>
    """
    if pattern == '/' or exact_match_only:
        if pattern == request.path:
            return ' class="selected"'
    else:
        if re.search(pattern, request.path):
            return ' class="selected"'

    if extra_pattern:
        if extra_pattern == '/':
            if extra_pattern == request.path:
                return ' class="selected"'
        else:
            if re.search(extra_pattern, request.path):
                return ' class="selected"'

    return ''


@register.filter
def getitem(array, i):
    """
    Get a value from a list or dict

    Example:
        {% load vrot %}
        {{ my_dict|getitem:my_key }}
    """
    try:
        return array[i]
    except:
        return ''
