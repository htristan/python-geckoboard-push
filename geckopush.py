import requests, json

class Gecko(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, widget_key, data):
        ret = requests.post("https://push.geckoboard.com/v1/send/%s" % widget_key, json.dumps({'api_key' : self.api_key, 'data' : data}), verify=False)
        if not (ret.status_code == 200 and ret.json().get('success') == True):
            raise ValueError(ret.content)

    def number(self, widget_key, number1, number2=None):
        data = {'item' : []}
        if number1 is not None: data['item'].append({'value' : number1, 'text' : ''})
        if number2 is not None: data['item'].append({'value' : number2, 'text' : ''})
        return self.push(widget_key, data)

    def rag(self, widget_key, *items):
        data = {'item' : []}
        for item in items:
            data['item'].append({'value' : item[0], 'text' : item[1]})
        return self.push(widget_key, data)

    def line(self, widget_key, values, **kwargs):
        data = {'item' : [], 'settings' :kwargs}
        for item in values:
            data['item'].append(item)
        return self.push(widget_key, data)

    def text(self, widget_key, *texts):
        data = { "item" : [] }
        for text in texts:
            if isinstance(text, dict):
                data['item'].append(dict(text))
            else:
                data['item'].append({"text" : text, "type" : 0})
        return self.push(widget_key, data)

    def heartbeat(self, widget_key, utc=True, format="%H:%M / %d %b"):
        import datetime
        dt = (datetime.datetime.utcnow if utc else datetime.datetime.now)().strftime(format)
        return self.text(widget_key, dt)

    def beater(self, *args, **kwargs):
        return lambda: self.heartbeat(*args, **kwargs)


