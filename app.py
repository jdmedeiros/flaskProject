import hashlib

from flask import Flask, jsonify, request

app = Flask(__name__)


# Compute the hash of the text provided using the hash algorithm provided
def calculate_hash(text, algorithm="SHA-256"):
    if algorithm == "MD5":
        return hashlib.md5(text).hexdigest()
    elif algorithm == "SHA-1":
        return hashlib.sha1(text).hexdigest()
    elif algorithm == "SHA-224":
        return hashlib.sha224(text).hexdigest()
    elif algorithm == "SHA-256":
        return hashlib.sha256(text).hexdigest()
    elif algorithm == "SHA-384":
        return hashlib.sha384(text).hexdigest()
    elif algorithm == "SHA-512":
        return True, hashlib.sha512(text).hexdigest()
    else:
        return False, 'Invalid algorithm. Must be one of [MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512]'


@app.route('/')
def welcome():
    requesturl = request.url
    return 'Valid endpoints are: <a href="' + requesturl + 'algorithms">algorithms</a> and <a href="' \
           + requesturl + 'hash?text=ABCDEFG&algorithm=SHA-512 ' \
                          '">hash</a><BR><P> Hash algorithm must be one of: <B>MD5, SHA-1, ' \
                          'SHA-224, SHA-256, SHA-384, SHA-512.</B> It defaults to SHA-512.'


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


if __name__ == '__main__':
    app.run(debug=True)

