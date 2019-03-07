
from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
import time
from django.template import Context, Template
from alerta import send_msg
from os import environ as env
import sys
import json
from django.conf import settings
from pprint import pprint
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#Service = "{{service.name}}"
#Link = "{{ scheme }}://{{ host }}{% url 'service' pk=service.id %}"
#Status="{% if service.overall_status == service.WARNING_STATUS %}warning{% if service.overall_status == service.ERROR_STATUS %}critical{% if service.overall_status == service.PASSING_STATUS %}normal"
check_error_template = "Failing checks:{% for check in service.all_failing_checks %} {{ check.last_result.error | safe }} {% endfor %}"
check_name_template = "{% for check in service.all_failing_checks %}{{ check.name }}{% endfor %}"
#check_category_template = "{% for check in service.all_failing_checks %}{{ check.check_category }}{% endfor %}"

class AlertaAlertUserData(AlertPluginUserData):
    name = "Alerta Plugin"
    alerta_text = models.CharField(max_length=50, blank=True)
    
class AlertaAlert(AlertPlugin):
    name = "Alerta Alert"
    author = "Suntek Ma"    


    def send_alert(self, service, users, duty_officers):

        #({{ scheme }}://{{ host }}{% url 'service' pk=service.id %})"
        linkstr = settings.WWW_SCHEME + "://"+settings.WWW_HTTP_HOST+"/service/pk="+ str(service.id)
        link = "<a href="+ linkstr +" target='_blank'>Cabot Link</a>"
        """Implement your send_alert functionality here."""

        if service.overall_status == service.WARNING_STATUS:
            status = 'warning'
        elif service.overall_status == service.ERROR_STATUS:
            status = 'major'
        elif service.overall_status == service.CRITICAL_STATUS:
            status = 'critical'
        elif service.overall_status == service.PASSING_STATUS:
            status = 'normal'

        t = Template(check_error_template)
        c = Context({
            'service': service
        })
        text = t.render(c)
        tname = Template(check_name_template)
        checkname = tname.render(c)
       
        alerta_template = {
              "attributes": {
                "region": "Newegg-cabot",
                "link": link
              },
              "environment": "Production",
              "event": checkname,
              "group": service.name,
              "origin": "curl",
              "resource": service.name,
              "service": [
                service.name
              ],
              "severity": status,
              "value": checkname,
              "type": "exceptionAlert",
              "text": text
            } 

        alerta_templatejson=json.dumps(alerta_template)
        send_msg(alerta_templatejson)
        return