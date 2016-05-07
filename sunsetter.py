
from flask import Flask
from flask import json, request, jsonify, Response, send_from_directory
import shade
import json
import yaml
import shade.inventory
import datetime

app = Flask(__name__)
app.debug = True


def output_format_dict(data, use_yaml):
    if use_yaml:
        return yaml.safe_dump(data, default_flow_style=False)
    else:
        return json.dumps(data, sort_keys=True, indent=2)

@app.route("/")
def hello():
    return send_from_directory('static', 'index.html')


@app.route("/cloud")
def cloud():

    if 'application/json' in request.headers['Accept']:
        dt = datetime.timedelta(seconds=60)
        now = datetime.datetime.now()
        if caching_inventory['age'] + dt < now:
            output = caching_inventory['inventory_obj'].list_hosts()
            caching_inventory['cache'] = output

        js = json.dumps(caching_inventory['cache'])
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    else:
        message = {
            'status': 415,
            'message': 'Unsupported Media Type: ' + request.headers['Content-Type'],
        }
        resp = jsonify(message)
        resp.status_code = 415
        return resp


if __name__ == "__main__":
    try:
        shade.simple_logging(debug=True)
        inventory = shade.inventory.OpenStackInventory(
            refresh=True, private=True,
            cloud=None)
        caching_inventory = { 'inventory_obj': inventory, 'cache': {}, 'age': datetime.datetime.now()}
        output = caching_inventory['inventory_obj'].list_hosts()
        caching_inventory['cache'] = output
    except shade.OpenStackCloudException as e:
        sys.stderr.write(e.message + '\n')
        sys.exit(1)
    app.run()
