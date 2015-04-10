from boto import ec2
import os
s_key = os.environ.get('AWS_SECRET_ACCESS_KEY_ID') if os.environ.has_key('AWS_SECRET_ACCESS_KEY_ID') else None
a_key = os.environ.get('AWS_ACCESS_KEY_ID') if os.environ.has_key('AWS_ACCESS_KEY_ID') else None
region = os.environ.get('REGION') if os.environ.has_key('REGION') else 'us-east-1'

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/_export')
def export():
    lGroup = request.args.get('l_group')
    lStreamPrefix = None
    region = request.args.get('region')
    daysAgo = request.args.get('d_ago', 0, type=int)

@app.route('/_get_regions', methods=['POST', 'GET'])
def get_regions():
    regions = ec2.regions(aws_access_key_id=a_key, aws_secret_access_key=s_key)
    return jsonify(regions=[r.name for r in regions])

@app.route('/_get_l_groups')
def get_log_groups():
    return ''

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
