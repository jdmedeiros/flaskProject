import hashlib
import socket
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Compute the hash of the text provided using the hash algorithm provided
def calculate_hash(text, algorithm="SHA-256"):
    if algorithm == "MD5":
        return True, hashlib.md5(text).hexdigest()
    elif algorithm == "SHA-1":
        return True, hashlib.sha1(text).hexdigest()
    elif algorithm == "SHA-224":
        return True, hashlib.sha224(text).hexdigest()
    elif algorithm == "SHA-256":
        return True, hashlib.sha256(text).hexdigest()
    elif algorithm == "SHA-384":
        return True, hashlib.sha384(text).hexdigest()
    elif algorithm == "SHA-512":
        return True, hashlib.sha512(text).hexdigest()
    else:
        return False, 'Invalid algorithm. The algorithm must be one of [MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512]'


@app.route('/')
def welcome():
    requesturl = request.url
    message = {
        "message": "Valid endpoints are: status, algorithms, and hash",
        "link_algorithms": requesturl + 'algorithms',
        "link_hash": requesturl + 'hash?text=ABCDEFG&algorithm=SHA-512',
        "hash_algorithm_options": "Hash algorithm must be one of: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512. It "
                                  "defaults to SHA-512."
    }
    return jsonify(message)


@app.get("/algorithms")
def functions():
    return jsonify(algorithms=["MD5", "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512"])


@app.get("/hash")
def compute():
    text = request.args.get('text')
    algorithm = request.args.get('algorithm')
    status, result = calculate_hash(text.encode(), algorithm)
    if status:
        return jsonify(text=text, algorithm=algorithm, hash=result)
    else:
        return jsonify(Error=result)


@app.get("/status")
def system_status():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    os_info = {
        "platform": os.uname().sysname,
        "release": os.uname().release,
        "version": os.uname().version,
        "machine": os.uname().machine,
    }

    return jsonify(
        hostname=hostname,
        ip=ip,
        os=os_info,
        release="v1.0.5"
    )


if __name__ == '__main__':
    app.run(debug=True)

