# app.py
# Required Imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "database-52a8d",
  "private_key_id": "8e4edd03ed34a5e7068cd8afed95ca6a06890cca",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4GPB4xUCMzEDk\n2hVTMtHG0kWMIUupy3m0DQs0cCFcV38A34q4QU0kJ+RrSHIv+tGjy2PMkdJXDxu2\nelUKpcvX63EBCO6ZTfJUgdIiJOEYFb221dmzZRs2YbOxfsw6Q7DZzRc1ySPGf65D\nxuH4n4dNR0FWr7TlbmYyQJZGQd10gfv1sJAxiGR9wmrnvl732htC2Jku2gah/ivQ\nDMNX/18kqXnN8xatB7XHNha+0+vmq2oW9DbVsfuGxnIbi1GPFp6NqnIEAvM0pE3Q\nuNPDx75SEtD7Due1/87VLW2lh9P/IpPt09MWdQckHyNSgoobPoyLJN6FSLkPN3TE\nga9QwWITAgMBAAECggEAUzRSWwMrrXcTTVuTj8rELQwUCsVxoQgptUq/6a9UJJwW\n9poR5Dz/VHwDLMnNcgn2fgUK0gaF/nsBl3Oqw+kzPB9ZL5KN5BPqlm8mPfBVG8GX\nwO7eOcpUhjuaL3qTazH02DttZg3GcYx7gn582xWe3Tp7OWaoZ5mB7uxp/s79/A2O\n2l2F5dQPt2trcNmQYYr4BMJeQGs03XNnoe99lm73NLwoFYyilAlvtT9D/PbIEuQa\nRvMD87eKSkIVx6YD6I8VgP2AUl5zSOHnIDHv0RzhjzxuZiOcjVF0kyt5IzlSDjv6\nZBoihiYDayTSFZ+8AaGTUNro8FvAfjv3RYqcysRSoQKBgQDoF14yZ0wXYGLFGcBn\nj4lK+RBk91EV+rlJLxgT1sFsJoLb7jZ0YKrqUCqvn9+kd7dBdEhwhByWNX4/GXTZ\nF/SybZ+abCJ/Y1CdeV6sp90Z5B0EJ+mGHtiBTZ6SgYzMwlrDZylUg6pJ6tHPEr6E\nzQ4Jfpj53dlfnMal/NpQqPGRDwKBgQDLD+TF9W7DCq2UwjqpsvXpj+gNeRqctXDi\nlSPYSEOJGooSMQHyvWAvWkpG97n7o4j6UXO1qpMHD48R6JNzDMzTIShAPdRNudfA\nOdGzMy1On2oVZvSLGjr1IB7Xsdb1nCUd7irwPb34BP5kcR4iQ6qKSbfjCRe9EG1f\nRk53iO4WvQKBgQCaOh0QZXA9AIHh9FDVAJ79QTDRxz8M2gWSSkc3t7fkxFqlB1EM\nWMh62DbladnVkvAmAL26dy//6SAxkhsBwFeM0igDF+R8vmRtoJ93ID1e3SUjA9q8\nk3bPxeKf/JKx5l0mCEGAtdXNNMujTRNpcFHpoUTKlc/DJ40h9Dqm6v1LpQKBgQCI\nqaKzZDHuTGJ0ap/mlA4S6gon/yhc7XQS2oLsTf496MGh6p/ACZoRZHf2+USPSgmn\nRmhUjH81UlBcoiWSWbwEIB2h1rrqsLe2pHMwYrIMZxeTXd4ZPEcPsFVxnzvnwvXs\nBd2aIEOZB2tamBLKxrWhKmn6/6SdVs/1PjETG/H5FQKBgGAhRxze/1nV0eWnpCgT\ntHSo/lorWqfor1AB14A1MqJb1xRPBEKaoeHm8wmkDSvv4GtDiT3tnmsaVu9zlGZr\ngXCRUbu/a17nh3u6p9iuZdXRBEZSBtpbJs/BwKQ+IA7RNcFXUof3d0zr0v8+Ux5e\n4kCEju4NXQ8mM9jYvQqyhPrh\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1szbr@database-52a8d.iam.gserviceaccount.com",
  "client_id": "106669837730544331965",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1szbr%40database-52a8d.iam.gserviceaccount.com"
})
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')
@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)