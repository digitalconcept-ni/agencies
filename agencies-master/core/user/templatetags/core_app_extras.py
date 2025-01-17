from django import template
from django.forms import CheckboxInput, Textarea, Select, ClearableFileInput

register = template.Library()


@register.filter()
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter()
def is_select(field):
    return field.field.widget.__class__.__name__ == Select().__class__.__name__


@register.filter()
def is_textarea(field):
    return field.field.widget.__class__.__name__ == Textarea().__class__.__name__

@register.filter()
def is_ClearableFileInput(field):
    return field.field.widget.__class__.__name__ == ClearableFileInput().__class__.__name__


@register.filter()
def split_form_field(form, request):
    if request.is_mobile:
        quantity = 1
    elif request.is_pc:
        quantity = 3
    list_of_fields = form.visible_fields()
    splitted_list = []

    for i in range(0, len(list_of_fields), quantity):
        splitted_list.append(list_of_fields[i:i + quantity])
    return splitted_list
