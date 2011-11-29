from django.contrib.admin.options import ModelAdmin
from actions import model_delete_selected


class DeletePerObjectModelAdmin(ModelAdmin):
    actions = [model_delete_selected]

    def get_actions(self, request):
        actions = super(DeletePerObjectModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
