from django import template
from django.forms import CheckboxInput

register = template.Library()


@register.filter()
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter()
def split_form_field(form, quantity):
    list_of_fields = form.visible_fields()
    splitted_list = []

    for i in range(0, len(list_of_fields), quantity):
        splitted_list.append(list_of_fields[i:i + quantity])
    return splitted_list
