import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mariadb+mariadbconnector://" + os.environ["MARIADB_USER"] + ":" + os.environ[
    "MARIADB_ROOT_PASSWORD"] + "@" + os.environ["MARIADB_DATABASE"]
db = SQLAlchemy(app)


class Paste(db.Model):
    __tablename__ = 'pastebin'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=100))
    content = Column(Text)
    createdAt = Column(DateTime, default=datetime.now)


def __init__(self, id, title, content, createdAt):
    self.id = id
    self.title = title
    self.content = content
    self.createdAt = createdAt


db.create_all()


# def selectById(Id):
#    return Paste.query.get(Id)
#
#
# def selectRecents():
#    recents = Paste.query.order_by(Paste.id.desc()).limit(100)
#    toReturn = []
#    for p in recents:
#        toReturn.append(({"title": p.title, "content": p.content, "createdAt": str(p.createdAt)}))
#    return toReturn


@app.route('/')
def index():
    return "Hello World"


@app.route('/api/paste', methods=['POST'])
def addPaste():
    try:
        title = request.json["title"]
        content = request.json["content"]
        newPaste = Paste(title=title, content=content)
        db.session.add(newPaste)
        db.session.commit()
        return jsonify({"id": newPaste.id})
    except:
        toReturn = None
    if toReturn is None:
        return jsonify({"error": "No title or content"}), 400
    else:
        return toReturn, 200


@app.route('/api/<Id>', methods=["GET"])
def getId(Id):
    paste = Paste.query.get(Id)
    if paste is None:
        return '', 404
    else:
        return json.dumps({
            "title": paste.title,
            "content": paste.content,
            "createdAt": str(paste.createdAt)
        }), 200


@app.route('/api/recents', methods=["POST"])
def getRecents():
    recents = Paste.query.order_by(Paste.id.desc()).limit(100)
    toReturn = []
    for p in recents:
        toReturn.append(({"title": p.title, "content": p.content, "createdAt": str(p.createdAt)}))
    return json.dumps(toReturn)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
