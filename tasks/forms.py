from django import forms
from tasks.models import Event, Category
from django.utils import timezone


class StyleFormMixin:
    default_class = "w-full border-2 border-gray-300 p-3 rounded-md shadow-sm mb-5"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_widgets()

    def style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                        "placeholder": f"Enter {field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                        "placeholder": f"Enter {field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                        "placeholder": f"Enter {field.label.lower()}",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update(
                    {"class": "border-2 border-gray-300 p-1 rounded-md shadow-sm mb-5"}
                )
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({"class": "space-y-2"})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({"class": "space-y-2"})
            else:
                field.widget.attrs.update({"class": self.default_class})


class EventModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "location",
            "asset",
            "category",
        ]

        labels = {
            "name": "Event Name",
            "description": "Event Description",
            "date": "Date",
            "location": "Location Name",
            "asset": "Image",
        }

        widgets = {
            "name": forms.TextInput(),
            "description": forms.Textarea(),
            "date": forms.SelectDateWidget(),
            "location": forms.TextInput(),
            "category": forms.RadioSelect(),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is not None and date < timezone.now().date():
            raise forms.ValidationError("The event date can not be in the past.")
        return date


# class ParticipantModelForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ["name", "email", "event"]

#         labels = {
#             "name": "Participant Name",
#             "email": "Participant Email",
#             "event": "Event Name",
#         }

#         widgets = {
#             "name": forms.TextInput(),
#             "email": forms.EmailInput(),
#             "event": forms.CheckboxSelectMultiple(),
#         }


class CategoryModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

        labels = {"name": "Category Name", "description": "Category Description"}

        widgets = {"name": forms.TextInput(), "description": forms.Textarea()}
