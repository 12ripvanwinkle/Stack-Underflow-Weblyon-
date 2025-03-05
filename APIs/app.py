from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
import mysql.connector
import random
import string
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)

# Base directory for all projects
BASE_STORAGE_DIR = 'projects'
os.makedirs(BASE_STORAGE_DIR, exist_ok=True)

# File type subdirectories
FILE_TYPES = ['js', 'css', 'html', 'images']

# Set allowed file extensions
ALLOWED_EXTENSIONS = {
    'js': {'js'},
    'css': {'css'},
    'html': {'html', 'htm'},
    'images': {'png', 'jpg', 'jpeg', 'gif', 'svg'}
}

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Stack"
    )

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '@gmail.com'  
app.config['MAIL_PASSWORD'] = ''  
app.config['MAIL_DEFAULT_SENDER'] = '@gmail.com'

mail = Mail(app)

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def ensure_project_folders(project_id, location):
    """Ensure project folders exist for all file types"""
    project_path = location or os.path.join(BASE_STORAGE_DIR, f'project_{project_id}')
    
    # Create main project directory if it doesn't exist
    os.makedirs(project_path, exist_ok=True)
    
    # Create subdirectories for file types if they don't exist
    for file_type in FILE_TYPES:
        os.makedirs(os.path.join(project_path, file_type), exist_ok=True)
    
    return project_path

# -------------------- USERS --------------------
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO User (Username, Password, Email) VALUES (%s, %s, %s)",
                   (data['Username'], data['Password'], data['Email']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User")

    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE User SET Password = %s WHERE UserID = %s", (data['Password'], id))

    conn.commit()
    conn.close()
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM User WHERE UserID = %s", (id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"})

# -------------------- USERS: ADVANCE --------------------
@app.route('/users/joincompany', methods=['POST'])
def join_company():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Companies WHERE CompanyID = %s AND Password = %s",
                     (data['CompanyID'], data['Password']))
    company = cursor.fetchone()

    if not company:
        return jsonify({"message": "Invalid company ID or password"})
    else:
        cursor.execute("INSERT INTO User_Company (UserID, CompanyID) VALUES (%s, %s)",
                   (data['UserID'], data['CompanyID']))
        
    conn.commit()
    conn.close()
    return jsonify({"message": "User joined company successfully"})

@app.route('/users/leavecompany', methods=['POST'])
def leave_company():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM User_Company WHERE UserID = %s AND CompanyID = %s",
                     (data['UserID'], data['CompanyID']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "User left company successfully"})

@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User WHERE Username = %s AND Password = %s",
                   (data['Username'], data['Password']))
    
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

# -------------------- COMPANIES --------------------
@app.route('/companies', methods=['POST'])
def create_company():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Companies (CompanyName, Password) VALUES (%s, %s)", 
                   (data['CompanyName'], data['Password']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Company created successfully"})

@app.route('/companies', methods=['GET'])
def get_companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Companies")
    companies = cursor.fetchall()

    conn.close()
    return jsonify(companies)

@app.route('/companies/delete', methods=['PUT'])
def delete_company():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Companies WHERE CompanyID = %s AND Password = %s",
                   (data['CompanyID'], data['Password']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Company deleted successfully"})

# -------------------- USER COMPANIES --------------------
@app.route('/usercompanies/<int:user_id>', methods=['GET'])
def get_user_companies(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User_Company WHERE UserID = %s", (user_id,))
    user_companies = cursor.fetchall()

    conn.close()
    return jsonify(user_companies)

@app.route('/usercompanies/<int:user_id>', methods=['DELETE'])
def delete_user_company(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM User_Company WHERE UserID = %s AND CompanyID = %s",
                   (user_id, data['CompanyID']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "User company deleted successfully"})

# -------------------- PROJECTS --------------------
@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create a project directory
    project_path = os.path.join(BASE_STORAGE_DIR, f"project_{data.get('CompanyID')}_{data.get('ProjectName')}")
    os.makedirs(project_path, exist_ok=True)
    
    # Create subdirectories for each file type
    for file_type in FILE_TYPES:
        os.makedirs(os.path.join(project_path, file_type), exist_ok=True)

    cursor.execute("INSERT INTO Project (ProjectName, ProjectIcon, Location, CompanyID) VALUES (%s, %s, %s, %s)",
                   (data['ProjectName'], data['ProjectIcon'], project_path, data['CompanyID']))
    
    # Get the newly created project ID
    project_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "message": "Project created successfully",
        "projectId": project_id,
        "location": project_path
    })

@app.route('/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Project")
    projects = cursor.fetchall()

    conn.close()
    return jsonify(projects)

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get project location before deleting
    cursor.execute("SELECT Location FROM Project WHERE ProjectID = %s", (id,))
    project = cursor.fetchone()
    
    if project and project['Location']:
        # Delete the project directory
        if os.path.exists(project['Location']):
            shutil.rmtree(project['Location'])
    
    # Delete from database
    cursor.execute("DELETE FROM Project WHERE ProjectID = %s", (id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Project deleted successfully"})

# -------------------- PROJECT FILES --------------------
@app.route('/projects/<int:project_id>/upload/<file_type>', methods=['POST'])
def upload_project_file(project_id, file_type):
    if file_type not in FILE_TYPES:
        return jsonify({"error": f"Invalid file type: {file_type}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get project location
    cursor.execute("SELECT Location FROM Project WHERE ProjectID = %s", (project_id,))
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        return jsonify({"error": "Project not found"}), 404
    
    # Ensure project folders exist
    project_path = ensure_project_folders(project_id, project['Location'])
    file_path = os.path.join(project_path, file_type)
    
    # Check if the post request has the file part
    if 'file' not in request.files:
        conn.close()
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser submits an empty part without filename
    if file.filename == '':
        conn.close()
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename, file_type):
        filename = secure_filename(file.filename)
        file_save_path = os.path.join(file_path, filename)
        file.save(file_save_path)
        
        # Record the file in the Media table
        cursor.execute(
            "INSERT INTO Media (Filename, Type, Location, ProjectID) VALUES (%s, %s, %s, %s)",
            (filename, file_type, os.path.join(file_type, filename), project_id)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": "File uploaded successfully",
            "project_id": project_id,
            "file_type": file_type,
            "filename": filename,
            "path": f"/projects/{project_id}/{file_type}/{filename}"
        }), 201
    
    conn.close()
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/projects/<int:project_id>/upload-folder/<file_type>', methods=['POST'])
def upload_project_folder(project_id, file_type):
    if file_type not in FILE_TYPES:
        return jsonify({"error": f"Invalid file type: {file_type}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get project location
    cursor.execute("SELECT Location FROM Project WHERE ProjectID = %s", (project_id,))
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        return jsonify({"error": "Project not found"}), 404
    
    # Ensure project folders exist
    project_path = ensure_project_folders(project_id, project['Location'])
    file_path = os.path.join(project_path, file_type)
    
    if 'files[]' not in request.files:
        conn.close()
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files[]')
    
    if len(files) == 0:
        conn.close()
        return jsonify({"error": "No files selected"}), 400
    
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            continue
        
        if allowed_file(file.filename, file_type):
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(file_path, filename)
            file.save(file_save_path)
            
            # Record the file in the Media table
            cursor.execute(
                "INSERT INTO Media (Filename, Type, Location, ProjectID) VALUES (%s, %s, %s, %s)",
                (filename, file_type, os.path.join(file_type, filename), project_id)
            )
            
            uploaded_files.append({
                "filename": filename,
                "path": f"/projects/{project_id}/{file_type}/{filename}"
            })
    
    conn.commit()
    conn.close()
    
    if len(uploaded_files) == 0:
        return jsonify({"error": "No valid files uploaded"}), 400
    
    return jsonify({
        "message": f"{len(uploaded_files)} files uploaded successfully",
        "project_id": project_id,
        "file_type": file_type,
        "files": uploaded_files
    }), 201

@app.route('/projects/<int:project_id>/files/<file_type>', methods=['GET'])
def list_project_files(project_id, file_type):
    if file_type not in FILE_TYPES:
        return jsonify({"error": f"Invalid file type: {file_type}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get project location and files from Media table
    cursor.execute(
        "SELECT m.* FROM Media m WHERE m.ProjectID = %s AND m.Type = %s",
        (project_id, file_type)
    )
    
    files = cursor.fetchall()
    conn.close()
    
    return jsonify({
        "project_id": project_id,
        "file_type": file_type,
        "count": len(files),
        "files": files
    })

@app.route('/projects/<int:project_id>/<file_type>/<path:filename>', methods=['GET'])
def serve_project_file(project_id, file_type, filename):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get project location
    cursor.execute("SELECT Location FROM Project WHERE ProjectID = %s", (project_id,))
    project = cursor.fetchone()
    conn.close()
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    directory = os.path.join(project['Location'], file_type)
    return send_from_directory(directory, filename)

# -------------------- PREFERENCES --------------------
@app.route('/preferences', methods=['POST'])
def create_preferences():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Preferences (FontSize, ColorMode, UserID) VALUES (%s, %s, %s)",
                   (data['FontSize'], data['ColorMode'], data['UserID']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Preferences set successfully"})

@app.route('/preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Preferences WHERE UserID = %s", (user_id,))
    preferences = cursor.fetchone()

    conn.close()
    return jsonify(preferences)

@app.route('/preferences/<int:user_id>', methods=['PUT'])
def update_preferences(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Preferences SET FontSize = %s, ColorMode = %s WHERE UserID = %s",
                   (data['FontSize'], data['ColorMode'], user_id))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Preferences updated successfully"})

# -------------------- CHAT HISTORY --------------------
@app.route('/chat', methods=['POST'])
def create_chat():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO ChatHistory (Text, ProjectID) VALUES (%s, %s)", (data['Text'], data['ProjectID']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Chat message added"})

@app.route('/chat/<int:project_id>', methods=['GET'])
def get_chat_history(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ChatHistory WHERE ProjectID = %s", (project_id,))

    chat_history = cursor.fetchall()
    conn.close()
    return jsonify(chat_history)

# -------------------- MEDIA --------------------
@app.route('/media', methods=['POST'])
def upload_media():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Media (Filename, Type, Location, ProjectID) VALUES (%s, %s, %s, %s)",
                   (data['Filename'], data['Type'], data['Location'], data['ProjectID']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Media uploaded successfully"})

@app.route('/media/<int:project_id>', methods=['GET'])
def get_media(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Media WHERE ProjectID = %s", (project_id,))
    media = cursor.fetchall()

    conn.close()
    return jsonify(media)

@app.route('/media/<int:id>', methods=['DELETE'])
def delete_media(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get media info before deleting
    cursor.execute("SELECT m.*, p.Location as ProjectLocation FROM Media m JOIN Project p ON m.ProjectID = p.ProjectID WHERE m.MediaID = %s", (id,))
    media = cursor.fetchone()
    
    if media:
        # Delete the file if it exists
        file_path = os.path.join(media['ProjectLocation'], media['Type'], media['Filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Delete from database
    cursor.execute("DELETE FROM Media WHERE MediaID = %s", (id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Media deleted successfully"})

# -------------------- PASSWORD RESET --------------------
@app.route('/users/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.json
    email = data.get('Email')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"message": "User not found"}), 404

    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    cursor.execute("UPDATE User SET ResetCode = %s WHERE Email = %s", (reset_code, email))

    conn.commit()
    conn.close()

    msg = Message("Password Reset Code", recipients=[email])
    msg.body = f"Your password reset code is: {reset_code}"
    mail.send(msg)

    return jsonify({"message": "Reset code sent to your email"})

@app.route('/users/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('Email')
    reset_code = data.get('ResetCode')
    new_password = data.get('NewPassword')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User WHERE Email = %s AND ResetCode = %s", (email, reset_code))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "Invalid reset code"}), 400

    cursor.execute("UPDATE User SET Password = %s, ResetCode = NULL WHERE Email = %s", (new_password, email))

    conn.commit()
    conn.close()

    return jsonify({"message": "Password updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)