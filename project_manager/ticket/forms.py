from django import forms
from .models import Ticket, MileStone


class TaskForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"


class MileStoneForm(forms.ModelForm):
    class Meta:
        model = MileStone
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        # user = kwargs.pop ('user')
        super (MileStoneForm, self).__init__ (*args, **kwargs)
        self.fields['user'].widget = HiddenInput ()
        self.fields['ticket'].widget = HiddenInput()