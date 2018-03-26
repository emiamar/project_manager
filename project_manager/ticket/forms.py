import datetime
from django import forms
from .models import Ticket, MileStone



def last_years():
    first_year = datetime.datetime.now().year - 1
    return list(range(first_year + 2, first_year, -1))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super (TaskForm, self).__init__ (*args, **kwargs)
        self.fields['due_date'].widget = forms.SelectDateWidget(
            years=last_years())

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