import csv

from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from ipware.ip import get_real_ip
from netaddr import IPNetwork, IPAddress

from .models import EnvironmentalSampleType, HostSampleType


def messages_to_json(request):
    json = {'messages': []}
    for message in messages.get_messages(request):
        json['messages'].append({
            "level": message.level,
            "level_tag": message.level_tag,
            "message": message.message,
        })
    json['messages_html'] = render_to_string(
        'includes/messages.html',
        {'messages': messages.get_messages(request)})
    return json


def request_should_post_to_slack(request):
    ip = get_real_ip(request)
    if not ip:
        return True  # do post for dev server (no 'real' external ip)
    try:
        ignore_networks = getattr(settings, 'SLACK_LOG_IGNORE_NETWORKS', None)
    except AttributeError:
        return True
    return not any(IPAddress(ip) in IPNetwork(n) for n in ignore_networks)


def load_environmentalsampletype_data(file_path):
    """clear and reload EnvironmentalSampleType data from csv"""
    EnvironmentalSampleType.objects.all().delete()
    reader = csv.DictReader(open(file_path))
    for row in reader:
        obj = EnvironmentalSampleType(name=row['name'])
        obj.save()


def load_hostsampletype_data(file_path):
    """clear and reload HostSampleType data from csv"""
    HostSampleType.objects.all().delete()
    reader = csv.DictReader(open(file_path))
    for row in reader:
        obj = HostSampleType(name=row['name'])
        obj.save()
