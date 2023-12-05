""" Views module. """
import string
import markdown
from django import forms
from django.views.generic.edit import FormView
from dictionary.models import Entry


MAX_LOOKUPS = 100


def is_cjk(char):
    """ Return true if the character is tr38 Unihan. """
    try:
        codepoint = ord(char)
    except TypeError:
        return False

    # A slightly cheaper test up front.
    if char in string.printable:
        return False

    # https://www.unicode.org/reports/tr38/#BlockListing
    # https://www.unicode.org/reports/tr38/#SortingAlgorithm

    result = False
    match codepoint:
        # CJK Unified Ideographs
        case codepoint if 0x4E00 <= codepoint <= 0x9FFF:
            result = True
        # CJK Unified Ideographs Extension A
        case codepoint if 0x3400 <= codepoint <= 0x4DBF:
            result = True
        # CJK Unified Ideographs Extension B
        case codepoint if 0x20000 <= codepoint <= 0x2A6DF:
            result = True
        # CJK Unified Ideographs Extension C
        case codepoint if 0x2A700 <= codepoint <= 0x2B739:
            result = True
        # CJK Unified Ideographs Extension D
        case codepoint if 0x2B740 <= codepoint <= 0x2B81D:
            result = True
        # CJK Unified Ideographs Extension E
        case codepoint if 0x2B820 <= codepoint <= 0x2CEA1:
            result = True
        # CJK Unified Ideographs Extension F
        case codepoint if 0x2CEB0 <= codepoint <= 0x2EBE0:
            result = True
        # CJK Unified Ideographs Extension G
        case codepoint if 0x30000 <= codepoint <= 0x3134A:
            result = True
        # CJK Unified Ideographs Extension H
        case codepoint if 0x31350 <= codepoint <= 0x323AF:
            result = True
        # CJK Unified Ideographs Extension I
        case codepoint if 0x2EBF0 <= codepoint <= 0x2EE5D:
            result = True
        # CJK Compatibility Ideographs
        case codepoint if 0xF900 <= codepoint <= 0xFAD9:
            result = True
        # CJK Compatibility Supplement
        case codepoint if 0x2F800 <= codepoint <= 0x2FA1D:
            result = True
    return result


def get_cjk_chars(text):
    """ Return a string of CJK characters. """
    chars = ''
    for char in text:
        if is_cjk(char):
            chars += char
    return chars


def get_cjk_map(chars):
    """ Return a map of characters to Eentry objects. """
    entries = {}
    not_found = []
    lookups = 0
    for char in chars:
        if lookups >= MAX_LOOKUPS or char in entries or char in not_found:
            continue
        try:
            lookups += 1
            entry = Entry.objects.get(pk=char)
            entry.html_defs = markdown.markdown(entry.definitions)
            entries[char] = entry
        except Entry.DoesNotExist:
            not_found.append(char)
    return entries


class DictForm(forms.Form):
    """ Dictionary form. """
    field = forms.CharField(
        widget=forms.Textarea(attrs={'autofocus': True}),
        max_length=2500
    )


class DictFormView(FormView):
    """ Dictionary lookup form view. """
    form_class = DictForm
    template_name = 'dictionary/form.html'

    def form_valid(self, form):
        """ Return the same form. """
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """ Insert template context data. """
        context = super().get_context_data(**kwargs)
        if context['form'].is_valid():
            context['cjk_chars'] = get_cjk_chars(
                context['form'].cleaned_data['field']
            )
            context['cjk_map'] = get_cjk_map(context['cjk_chars'])
        else:
            context['cjk_chars'] = ''
            context['cjk_map'] = {}
        return context
