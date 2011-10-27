from django.forms import ClearableFileInput
from sorl.thumbnail.shortcuts import get_thumbnail
from django.utils.safestring import mark_safe


class ImageWidget(ClearableFileInput):
    """
    An ImageField Widget that shows a thumbnail for and link to the current image.
    """
    template_with_initial = u'%(clear_template)s %(input)s'
    template_with_clear = u'%(clear)s <label style="width:auto" for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None):
        output = super(ImageWidget, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            try:
                mini = get_thumbnail(value, 'x80', upscale=False)
            except Exception:
                pass
            else:
                output = (
                    u'<a style="width:%spx;" class="thumbnail fancybox" href="%s">'
                    u'<img alt="" src="%s"></a>%s'
                ) % (mini.width, value.url, mini.url, output)

        return mark_safe(output)
