import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import uuid
import ai
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.config['DB_FILE'] = 'db.json'


def load_db():
   
    if not os.path.exists(app.config['DB_FILE']):
        return {}
    try:
        with open(app.config['DB_FILE'], 'r') as f:
            return json.load(f)
    except:
        return {}

def save_to_db(new_id, new_data):
    
    current_db = load_db()
    current_db[new_id] = new_data
    with open(app.config['DB_FILE'], 'w') as f:
        json.dump(current_db, f, indent=4)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}

PROPOSALS_DB = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    db_data = load_db()
   
    proposals_list = []
    for pid, data in db_data.items():
        proposals_list.append({
            "id": pid,
            "client_name": data.get("client_name", "Unknown Client"),
            "urgency": data.get("urgency_detected", 0),
            "total": data.get("final_total", 0.0),
            "summary": data.get("executive_summary", "")
        })
    
    proposals_list.reverse()
    
    return render_template('index.html', proposals=proposals_list)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    user_context = request.form.get('context_text', 'Standard new client interaction.')
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
    
        try:
            proposal_data = ai.call_gemi(filepath,user_context)
        except Exception as e:
            return f"AI Error: {str(e)}"
        
    
        proposal_id = str(uuid.uuid4())
        
        
        PROPOSALS_DB[proposal_id] = proposal_data
        save_to_db(proposal_id, proposal_data)
        
        
        return redirect(url_for('view_proposal', pid=proposal_id))
        
    return 'Invalid File'

@app.route('/upload_p', methods=['POST'])
def upload_pricing():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], "price.txt")
    file.save(filepath)
    return "Pricing Rules Updated Successfully! Now upload audio."



@app.route('/proposal/<pid>')
def view_proposal(pid):
    
    

    db_data = load_db()
    data = db_data.get(pid)
    
    if not data:
        return "Proposal Not Found (or server restarted)", 404
    
   
    return render_template('proposal.html', p=data)

if __name__ == '__main__':
    app.run(debug=True)

