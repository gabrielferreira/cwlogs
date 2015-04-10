from flask import Flask, render_template, request
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

@app.route('/_get_regions'):
    return ''

@app.route('/_get_l_groups'):
    return ''

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
