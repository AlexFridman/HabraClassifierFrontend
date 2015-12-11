from django import forms


class TopicClassificationForm(forms.Form):
    topic_id = forms.IntegerField(min_value=1, max_value=300000)
    label_n = forms.IntegerField(min_value=1, max_value=100)


class TextClassificationForm(forms.Form):
    name = forms.CharField(required=False)
    text = forms.Textarea()
    label_n = forms.IntegerField(min_value=1, max_value=100)
