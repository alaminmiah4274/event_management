from django import forms
from tasks.models import Event, Participant, Category


class StyleFormMixin:
	default_class = "w-full border-2 border-gray-300 p-3 rounded-md shadow-sm mb-5"

	def style_widgets(self):
		for field_name, field in self.fields.items():
			if isinstance(field.widget,  forms.TextInput):
				field.widget.attrs.update({
					"class": self.default_class,
					"placeholder": f"Enter {field.label.lower()}"
				})
			elif isinstance(field.widget, forms.Textarea):
				field.widget.attrs.update({
					"class": self.default_class,
					"placeholder": f"Enter {field.label.lower()}",
					"rows": 5
				})
			elif isinstance(field.widget, forms.SelectDateWidget):
				field.widget.attrs.update({
					"class": "border-2 border-gray-300 p-1 rounded-md shadow-sm mb-5"
				})
			elif isinstance(field.widget, forms.RadioSelect):
				field.widget.attrs.update({
					"class": "space-y-2"
				})
			elif isinstance(field.widget, forms.CheckboxSelectMultiple):
				field.widget.attrs.update({
					"class": "space-y-2"
				})
			else:
				field.widget.attrs.update({
					"class": self.default_class
				})


class EventModelForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = Event
		fields = ["name", "description", "date", "location", "category"]

		widgets = {
			"name": forms.TextInput(),
			"description": forms.Textarea(),
			"date": forms.SelectDateWidget(),
			"location": forms.TextInput(),
			"category": forms.RadioSelect()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.style_widgets()
		self.fields["name"].label = "Event Name"
		self.fields["description"].label = "Event Description"
		self.fields["location"].label = "Event Location"
		self.fields["category"].label = "Category Name"



class ParticipantModelForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = Participant
		fields = ["name", "email", "event"]

		widgets = {
			"name": forms.TextInput(),
			"email": forms.EmailInput(),
			"event": forms.CheckboxSelectMultiple()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.style_widgets()
		self.fields["name"].label = "Participant Name"
		self.fields["email"].label = "Participant Email"
		self.fields["event"].label = "Event Name"



class CategoryModelForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = Category
		fields = ["description"]

		widgets = {
			"description": forms.Textarea()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.style_widgets()
		self.fields["description"].label = "Category Description"