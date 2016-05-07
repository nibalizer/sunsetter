
from flask import Flask
from flask import json, request, jsonify, Response, send_from_directory
import shade
import json
import yaml
import shade.inventory

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
        output = inventory.list_hosts()
        js = json.dumps(output)
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
    except shade.OpenStackCloudException as e:
        sys.stderr.write(e.message + '\n')
        sys.exit(1)
    app.run()
