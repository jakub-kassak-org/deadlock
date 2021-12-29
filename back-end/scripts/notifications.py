import datetime
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError

from users import get_token, create_req


def get_logs(count, token):
    params = urllib.parse.urlencode({
        "limit": count,
        "offset": 0,
        "levelno": 0
    })
    req = create_req("http://localhost/log/" + "?" + params, token)
    res = urllib.request.urlopen(req)
    return res.read().decode("utf-8")


def notify_for_errors():
    try:
        token = get_token()
        params = urllib.parse.urlencode({
            "time_from": datetime.datetime.utcnow() - datetime.timedelta(days=1),
            "time_to": datetime.datetime.utcnow(),
            "levelno": 0
        })
        req = create_req("http://localhost/log/count/" + "?" + params, token)
        res = urllib.request.urlopen(req)
        count = int(json.loads(res.read())["count"])
        print(count)
        if count > 2:
            mail_body = f"There are too many errors - count = {count}.\n"
            for x in json.loads(get_logs(10, token)):
                mail_body += x["msg"].strip() + '\n'
            body = json.dumps({
                "title": "Deadlock log errors",
                "message": mail_body,
                "topic": "topic1"
            }).encode("utf-8")
            req = create_req("http://localhost/notify/", token)
            res = urllib.request.urlopen(req, body)
            print(json.loads(res.read()))
    except HTTPError as e:
        print(e, e.read())


if __name__ == '__main__':
    notify_for_errors()
