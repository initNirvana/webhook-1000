import os,sys
sys.path.insert(1, os.path.join(os.path.abspath("."), 'env/lib/python2.7/site-packages'))
from flask import Flask, render_template, request, redirect, url_for, jsonify
# http://pymotw.com/2/hmac/
import hmac
import hashlib
# http://techarena51.com/index.php/how-to-install-python-3-and-flask-on-linux/
import subprocess


app = Flask(__name__)
GITHUB_SECRET = "iam Marika Husband"


def verify_hmac_hash(data, signature):
    github_secret = bytes(GITHUB_SECRET, 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)



@app.route("/")
def Home():
    return "Hello"

@app.route("/payload", methods=['POST'])
def github_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct'] == True:
                try:
                    cmd_output = subprocess.check_output(
                        ['git', 'pull', 'origin', 'master'],)
                    return jsonify({'msg': str(cmd_output)})
                except subprocess.CalledProcessError as error:
                    return jsonify({'msg': str(error.output)})

    else:
        return jsonify({'msg': 'invalid hash'})


if __name__ == "__main__":
    # app.debug = True
    # app.run(host="127.0.0.1")
    app.run()