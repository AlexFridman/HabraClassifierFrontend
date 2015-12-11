from django.views import generic
from .forms import TextClassificationForm, TopicClassificationForm
from django.forms import Form
from HabraClassifier.code import TopicDownloader, TopicCleaner, TopicParser
from HabraClassifier.code.topic_downloader import NotFoundError
from urllib import parse
from requests import request
import json
import logging
from django.shortcuts import render_to_response


# Create your views here.
def send_classify_request(uri: str, text: str, label_n: int):
    encode = str.encode(text)
    params = {'text': encode, 'label_n': label_n}
    data = parse.urlencode(params)
    return request('POST', uri, data=data)


class TopicClassificationView(generic.FormView):
    template_name = 'app/topic_classification.html'
    form_class = TopicClassificationForm

    parser = TopicParser()
    cleaner = TopicCleaner()

    def get_raw_point(self, topic_id: int) -> (list, list, str):
        topic_html = TopicDownloader.download_topic(topic_id)
        raw_topic = self.parser.parse(topic_html)
        labels = raw_topic.hubs + raw_topic.tags
        raw_text = raw_topic.text
        name = raw_topic.name

        return raw_text, labels, name

    def form_valid(self, form: Form):
        topic_id = int(form.data['topic_id'])
        label_n = form.data['label_n']

        try:
            raw_text, labels, name = self.get_raw_point(topic_id)
        except NotFoundError:
            logging.debug('Cannot download topic')
            return render_to_response('app/error.html', {'error_message': 'Cannot download topic'})

        try:
            resp = send_classify_request('http://localhost:8000', raw_text, label_n)
            prediction = json.loads(resp.headers['prediction'])
        except Exception as e:
            logging.debug('Server is down')
            return render_to_response('app/error.html', {'error_message': 'Server is down'})

        return render_to_response('app/result.html', {'name': name,
                                                      'actual': labels, 'predicted': prediction})


class TextClassificationView(generic.FormView):
    template_name = 'app/text_classification.html'
    form_class = TextClassificationForm

    def form_valid(self, form):
        raw_text = form.data['text']
        label_n = form.data['label_n']
        name = form.clean_data['name']

        try:
            resp = send_classify_request('http://localhost:8000', raw_text, label_n)
            prediction = json.loads(resp.headers['prediction'])
        except Exception as e:
            logging.debug('Server is down')
            return render_to_response('app/error.html', {'error_message': 'Server is down'})

        return render_to_response('app/result.html', {'name': name,
                                                      'predicted': prediction})
