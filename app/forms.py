from django import forms


class TopicClassificationForm(forms.Form):
    post_url = forms.CharField()
    label_n = forms.IntegerField(min_value=1, max_value=100)


class TextClassificationForm(forms.Form):
    text = forms.Textarea()
    label_n = forms.IntegerField(min_value=1, max_value=100)
