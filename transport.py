from flask import Blueprint, request
import json
import utils
import requests
import config

transport = Blueprint('transport', __name__)

@transport.route('/info/<int:sta_num>')
def station_info(sta_num):
    res = utils.db_execute(f'select sta_pre, sta_name, sta_next from station_info where sta_num={sta_num}').fetchone()
    if res:
        return json.dumps({
            "pre": res[0],
            "now": res[1],
            "next": res[2]
        })
    else:
        return '{"pre":null,"now":null,"next":null}'

@transport.route('/send_sms')
def send_sms():
    content = request.form.get('content')
    tel_number = request.form.get('telnum')
    if not content or not tel_number:
        return utils.error_page(['insufficient parameters'])
    return "yes" if requests.post("http://gbk.sms.webchinese.cn", form={
        **config.config["sms_creds"],
        "smsMob": tel_number,
        "smsText": content
    }).text == '1' else "no"
