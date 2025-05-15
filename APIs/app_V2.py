import sys
import os
sys.path.append(os.path.abspath("../Python files"))  
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pgpt import generate_portfolio_reply
from flask_mail import Mail, Message

import mysql.connector
import random
import string
from werkzeug.utils import secure_filename
import shutil
import jwt
import datetime
import base64



SECRET_KEY = "your-secret"


 
app = Flask(__name__)
CORS(app) 

# Base directory for all projects
BASE_STORAGE_DIR = 'stored_projects'
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

from dotenv import load_dotenv
import os

load_dotenv()  # Loads the .env file

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')

print(db_username)
print(db_password)


# Database connection
def get_db_connection():
    return mysql.connector.connect(user=db_username, 
    password=db_password, host=db_host, 
    port=3306, database="stack", ssl_ca="DigiCertGlobalRootCA.crt (1).pem", ssl_disabled=False)


mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')
mail_default_sender = os.getenv('MAIL_DEFAULT_SENDER')

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail_username 
app.config['MAIL_PASSWORD'] = mail_password  
app.config['MAIL_DEFAULT_SENDER'] = mail_default_sender

mail = Mail(app)

def create_storage_structure(company_name):
    # Create a directory for the company
    company_dir = os.path.join(BASE_STORAGE_DIR, company_name)
    os.makedirs(company_dir, exist_ok=True)

    # Create subdirectories for each file type
    for file_type in FILE_TYPES:
        os.makedirs(os.path.join(company_dir, file_type), exist_ok=True)

    return company_dir


def create_company(userID, companyName, Password, cursor):
    cursor.execute("INSERT INTO Company (CompanyName, Password) VALUES (%s, %s)",
                   (companyName, Password))
    
    cursor.execute("Select CompanyID from Company where CompanyName = %s", (companyName,))
    companyID = cursor.fetchone()[0]

    cursor.execute("INSERT INTO User_Company (userID, CompanyID) VALUES (%s, %s)",
                   (userID, companyID))
    

def create_preference(userID, cursor):
    fontSize = 12
    colorMode = "light"

    cursor.execute("INSERT INTO Preference (FontSize, ColorMode, UserID) VALUES (%s, %s, %s)", (fontSize, colorMode, userID))

def delete_project_helper(project_id, cursor):
    cursor.execute("SELECT URI FROM Project WHERE ProjectID = %s", (project_id,))
    uri = cursor.fetchone()



    cursor.execute("DELETE FROM Project WHERE ProjectID = %s", (project_id,))

    project_dir = os.path.join(os.getcwd(), uri[0])
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    else: 
        return jsonify({'error': 'Project directory not found'}), 404


def delete_all_projects(company_id ,cursor):
    cursor.execute("SELECT ProjectID FROM Company_Project WHERE CompanyID = %s", (company_id,))
    projects = cursor.fetchall()

    for (project_id,) in projects:

        delete_project_helper(project_id, cursor)




def generate_jwt(name, password):
    payload = {
        'name': name,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['name'], decoded['password']
    except jwt.ExpiredSignatureError:
        return None, None  # Token expired
    except jwt.InvalidTokenError:
        return None, None  # Invalid token
    

# def get_user_id(email, password):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT UserID FROM User WHERE Email = %s AND Password = %s", (email, password))
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return user[0] if user else None

def get_user_id(email, password, cursor):
    cursor.execute("SELECT UserID FROM User WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()
    return user[0] if user else {'error': 'Invalid email or password'}
    


def get_company_id(email, password, company_name, company_password, cursor):
    userID = get_user_id(email, password, cursor)
    if type(userID) is dict:
        return userID
    
    cursor.execute("SELECT CompanyID FROM User_Company WHERE userID = %s", (userID,))
    companies_id = cursor.fetchall()
    for company_id in companies_id:
        cursor.execute("SELECT CompanyID, CompanyName, Password FROM Company WHERE CompanyID = %s", (company_id[0],))
        company = cursor.fetchone()
        if company and company[1] == company_name and company[2] == company_password:
            return company[0]
        
    return {'error': 'Invalid company name or company_password'}

def get_project_id(email, password, company_name, company_password, project_name, cursor):
    company_id = get_company_id(email, password, company_name, company_password, cursor)
    if type(company_id) is dict:
        return company_id
    
    cursor.execute("SELECT ProjectID FROM Project WHERE ProjectName = %s", (project_name,))
    project_id = cursor.fetchone()
    if not project_id:
        return {'error': 'Project not found'}
    
    cursor.execute("SELECT * FROM Company_Project WHERE CompanyID = %s AND ProjectID = %s", (company_id, project_id[0]))
    company_project = cursor.fetchone()
    if not company_project:
        return {'error': 'Project not found in the company'}
    
    return project_id[0]

    



@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        if not email or not password or not username:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        

        if ' ' in password:
            return jsonify({'error': 'Password cannot contain spaces'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Email already exists'}), 400
        
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400

        cursor.execute("INSERT INTO User (Email, Password, username) VALUES (%s, %s, %s)",
                    (email, password, username))
        
        cursor.execute("SELECT UserID FROM User WHERE Email = %s", (email,))
        userID = cursor.fetchone()[0]

        create_company(userID, username, "My Company", cursor)

        create_preference(userID, cursor)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()



@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Email = %s AND Password = %s",
                    (email, password))    
        
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401

        cursor.close()
        conn.close()

        user = {
            'userID': user[0],
            'email': user[3],
            'username': user[1],
        }
        return jsonify(user)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()



@app.route('/send_email/<string:email>', methods=['GET'])
def send_email(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cursor.execute("UPDATE User SET ResetCode = %s WHERE Email = %s", (reset_code, email))
        conn.commit()
        cursor.close()
        conn.close()


        msg = Message("Password Reset Code", recipients=[email])
        msg.body = f"Your password reset code is: {reset_code}"
        mail.send(msg)


        return jsonify({"message": "Reset code sent to email"})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()





@app.route('/reset_password', methods=['PUT'])
def reset_password():
    try:    
        data = request.json
        email = data.get('email')
        reset_code = data.get('resetCode')
        new_password = data.get('newPassword')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Email = %s AND ResetCode = %s", (email, reset_code))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"message": "Invalid reset code"}), 400

        cursor.execute("UPDATE User SET Password = %s, ResetCode = NULL WHERE Email = %s", (new_password, email))

        conn.commit()
        conn.close()



        return jsonify({"message": "Password updated successfully"})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()


@app.route('/joincompany', methods=['POST']) 
def join_company():
    try:
        data = request.get_json()

        company_code = data.get('companyCode')
        email = data.get('email')
        password = data.get('password')

        decoded_company_code = decode_jwt(company_code)
        print(decoded_company_code)

        if not decoded_company_code:
            return jsonify({'error': 'Invalid company code'}), 400
        company_name, company_password = decoded_company_code

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password and company code are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Username = %s", (company_name,))
        personal_company = cursor.fetchone()
        if personal_company:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Failed to join company'}), 400
        
        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        cursor.execute("SELECT CompanyID FROM Company WHERE CompanyName = %s AND Password = %s", (company_name, company_password))
        company = cursor.fetchone()
        if not company:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid company name or password'}), 401
        company_id = company[0]


        

        cursor.execute("INSERT INTO User_Company (userID, CompanyID) VALUES (%s, %s)",
                    (user_id, company_id))
        

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User added to company successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()
 
    
@app.route('/getcompanycode', methods=['POST'])
def get_company_code():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password, company name, and company password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        company_id = get_company_id(email, password, company_name, company_password, cursor)
        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        





        token = generate_jwt(company_name, company_password)

        return jsonify({'companyCode': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/companies', methods=['POST'])
def get_Companies():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401

        cursor.execute("SELECT CompanyID FROM User_Company WHERE UserID = %s", (user_id,))
        companies = cursor.fetchall()
        company_list = []
        for company in companies:
            cursor.execute("SELECT CompanyName, Password FROM Company WHERE CompanyID = %s", (company[0],))
            company_name_password = cursor.fetchone()
            if company_name_password:
                company_list.append({ "name": company_name_password[0], "password": company_name_password[1]})
        cursor.close()
        conn.close()
        return jsonify({'companies': company_list})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()


@app.route('/getcompany', methods=['POST'])
def get_Company():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401

        cursor.execute("SELECT c.CompanyName, c.Password FROM User_Company uc JOIN Company c ON uc.CompanyID = c.CompanyID WHERE uc.UserID = %s AND c.CompanyName = %s", (user_id , company_name))
        company = cursor.fetchone()

        if not company:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid company name'}), 401
        company_name, password = company

        return jsonify({'companyName': company_name, 'password': password})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()





@app.route('/createcompany', methods=['POST'])
def create_company_route():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password, company name, and company password are required'}), 400
        
        if ' ' in company_password:
            return jsonify({'error': 'Company password cannot contain spaces'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)

        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        cursor.execute("SELECT * FROM Company WHERE CompanyName = %s", (company_name,))
        existing_company = cursor.fetchone()

        if existing_company:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Company already exists'}), 400
        
        cursor.execute("INSERT INTO Company (CompanyName, Password) VALUES (%s, %s)",
                    (company_name, company_password))
        cursor.execute("SELECT CompanyID FROM Company WHERE CompanyName = %s", (company_name,))
        company_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO User_Company (userID, CompanyID) VALUES (%s, %s)",
                    (user_id, company_id))
    
        

        
        company_id = get_company_id(email, password, company_name, company_password, cursor)
        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Failed to create company'}), 500


 
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Company created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()



@app.route("/createproject", methods=["POST"])
def create_project():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        project_name = data.get('projectName')

        if not email or not password or not company_name or not company_password or not project_name:
            return jsonify({'error': 'Email, password, company name, company password, and project name are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        company_id = get_company_id(email, password, company_name, company_password, cursor)
    


        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        
    
        cursor.execute("SELECT * FROM User_Company WHERE UserID = %s AND CompanyID = %s",
                    (user_id, company_id))
        user_company = cursor.fetchone()

        if not user_company:
            cursor.close()
            conn.close()
            return jsonify({'error': 'User is not part of the company'}), 401
        
        cursor.execute("SELECT * FROM Project WHERE ProjectName = %s", (project_name,))
        existing_project = cursor.fetchone()

        if existing_project:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project already exists'}), 400
        
        uri = create_storage_structure(project_name)

        cursor.execute("INSERT INTO Project (ProjectName, URI) VALUES (%s, %s)",
                    (project_name, uri))
        
        cursor.execute("SELECT ProjectID FROM Project WHERE ProjectName = %s", (project_name,))
        project_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Company_Project (CompanyID, ProjectID) VALUES (%s, %s)",
                    (company_id, project_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Project created successfully'}), 201
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/getprojects", methods=["POST"])
def get_projects():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password, company name, and company password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()


        
        company_id = get_company_id(email, password, company_name, company_password, cursor)

        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        
        cursor.execute("SELECT ProjectID FROM Company_Project WHERE CompanyID = %s", (company_id,))
        projects = cursor.fetchall()

        project_list = []
        for project in projects:
            cursor.execute("SELECT ProjectName FROM Project WHERE ProjectID = %s", (project[0],))
            project_name = cursor.fetchone()
            if project_name:
                project_list.append(project_name[0])
        
        cursor.close()
        conn.close()
        
        return jsonify({'projects': project_list})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/getproject", methods=["POST"])
def get_project():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        project_name = data.get('projectName')

        if not email or not password or not company_name or not company_password or not project_name:
            return jsonify({'error': 'Email, password, company name, company password, and project name are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        project_id = get_project_id(email, password, company_name, company_password, project_name, cursor)
        if type(project_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(project_id), 401


        cursor.execute("SELECT URI FROM Project WHERE ProjectID = %s", (project_id,))
        uri = cursor.fetchone()
        if not uri:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project URI not found'}), 404

        # Modify URI to be the absolute path
        uri = os.path.join(os.getcwd(), uri[0])
        
        if not os.path.exists(uri):
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project directory not found'}), 404

        cursor.close()
        conn.close()

        return jsonify({'uri': uri})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()


@app.route("/addtoproject", methods=["POST"])
def addtoproject():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        project_name = data.get('projectName')
        edited_folders = data.get('editedFolders')  # This should be a dict of {folder_name: {filename: base64_string, ...}}

        if not all([email, password, company_name, company_password, project_name, edited_folders]):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        project_id = get_project_id(email, password, company_name, company_password, project_name, cursor)
        if type(project_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(project_id), 401


        cursor.execute("SELECT URI FROM Project WHERE ProjectID = %s", (project_id,))
        uri_row = cursor.fetchone()
        if not uri_row:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project URI not found'}), 404

        project_path = os.path.join(os.getcwd(), uri_row[0])
        if not os.path.exists(project_path):
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project directory not found'}), 404

        # Now update only the edited folders
        for folder, files in edited_folders.items():
            folder_path = os.path.join(project_path, folder)
            os.makedirs(folder_path, exist_ok=True)

            for filename, file_content_base64 in files.items():
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'wb') as f:
                        f.write(base64.b64decode(file_content_base64))
                except Exception as e:
                    cursor.close()
                    conn.close()
                    return jsonify({'error': f'Failed to write file {filename}: {str(e)}'}), 500

        cursor.close()
        conn.close()
        return jsonify({'message': 'Edited folders updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/createchat", methods=["POST"])
def create_chat():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        project_name = data.get('projectName')

        chat_text = data.get('text')
        author = data.get('author')

        if not chat_text or not author :
            return jsonify({'error': 'text and author are required'}), 400


        if not email or not password or not company_name or not company_password or not project_name:
            return jsonify({'error': 'Email, password, company name, company password, and project name are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        project_id = get_project_id(email, password, company_name, company_password, project_name, cursor)
        if type(project_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(project_id), 401


        cursor.execute("INSERT INTO Chat (Text, Author, ProjectID) VALUES (%s, %s, %s)", (chat_text, author, project_id))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Chat created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()


@app.route("/getchats", methods=["POST"])
def get_chats():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        project_name = data.get('projectName')



        if not email or not password or not company_name or not company_password or not project_name:
            return jsonify({'error': 'Email, password, company name, company password, and project name are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        project_id = get_project_id(email, password, company_name, company_password, project_name, cursor)
        if type(project_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(project_id), 401


        cursor.execute("SELECT Text, Author, Time FROM Chat WHERE ProjectID = %s", (project_id,))
        chats = cursor.fetchall()
        chat_list = []
        for chat in chats:
            chat_list.append({
                'text': chat[0],
                'author': chat[1],
                'time': chat[2].strftime('%Y-%m-%d %H:%M:%S')})

        cursor.close()
        conn.close()
        return jsonify({'chats': chat_list})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()
    

@app.route("/getPreference", methods=["POST"])
def getPreference():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        cursor.execute("SELECT FontSize, ColorMode FROM Preference WHERE UserID = %s", (user_id,))
        preference = cursor.fetchone()

        if not preference:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Preference not found'}), 404
        
        font_size, color_mode = preference
        cursor.close()
        conn.close()

        return jsonify({'fontSize': font_size, 'colorMode': color_mode})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/updatePreference", methods=["PUT"])
def updatePreference():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        font_size = data.get('fontSize')
        color_mode = data.get('colorMode')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        cursor.execute("Select FontSize, ColorMode FROM Preference WHERE UserID = %s", (user_id,))
        existing_preference = cursor.fetchone()
        if not existing_preference:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Preference not found'}), 404
        
        if font_size is None:
            font_size = existing_preference[0]

        if color_mode is None:
            color_mode = existing_preference[1]


        cursor.execute("UPDATE Preference SET FontSize = %s, ColorMode = %s WHERE UserID = %s", (font_size, color_mode, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'fontSize': font_size, 'colorMode': color_mode})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()


@app.route("/user", methods=["DELETE"])
def delete_user():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = get_user_id(email, password, cursor)
        if type(user_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(user_id), 401
        
        cursor.execute("SELECT Username FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        

        cursor.execute("SELECT CompanyID FROM User_Company WHERE UserID = %s", (user_id,))
        company_ids = cursor.fetchall()
        for (company_id,) in company_ids:
            cursor.execute("SELECT COUNT(*) FROM User_Company WHERE CompanyID = %s", (company_id,))
            count = cursor.fetchone()[0]

            if count == 1:
                delete_all_projects(company_id, cursor)
                cursor.execute("DELETE FROM Company WHERE CompanyID = %s", (company_id,))


        
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))

        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()



@app.route("/company", methods=["DELETE"])
def delete_company():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password, company name, and company password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        
        company_id = get_company_id(email, password, company_name, company_password, cursor)
        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        
        delete_all_projects(company_id, cursor)
        
        
        cursor.execute("DELETE FROM Company WHERE CompanyID = %s", (company_id,))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Company deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/project", methods=["DELETE"])
def delete_project():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        project_name = data.get('projectName')

        if not email or not password or not company_name or not company_password or not project_name:
            return jsonify({'error': 'Email, password, company name, company password, and project name are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()


        project_id = get_project_id(email, password, company_name, company_password, project_name, cursor)
        if type(project_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(project_id), 401

        
        delete_project_helper(project_id, cursor)
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Project deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/deletecompanyuser", methods=["DELETE"])
def delete_company_user():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')
        user_id = data.get('userID')

        if not email or not password or not company_name or not company_password or not user_id:
            return jsonify({'error': 'Email, password, company name, company password, and user ID are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        
        company_id = get_company_id(email, password, company_name, company_password, cursor)
        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        
        
        cursor.execute("DELETE FROM User_Company WHERE UserID = %s AND CompanyID = %s", (user_id, company_id))


        cursor.execute("SELECT COUNT(*) FROM User_Company WHERE CompanyID = %s", (company_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            delete_all_projects(company_id, cursor)
            cursor.execute("DELETE FROM Company WHERE CompanyID = %s", (company_id,))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User removed from company successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route("/getcompanyusers", methods=["POST"])
def get_company_users():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        company_name = data.get('companyName')
        company_password = data.get('companyPassword')

        if not email or not password or not company_name or not company_password:
            return jsonify({'error': 'Email, password, company name, and company password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        
        company_id = get_company_id(email, password, company_name, company_password, cursor)
        if type(company_id) is dict:
            cursor.close()
            conn.close()
            return jsonify(company_id), 401
        
        
        cursor.execute("SELECT UserID FROM User_Company WHERE CompanyID = %s", (company_id,))
        users = cursor.fetchall()
        user_list = []
        for (user,) in users:

            cursor.execute("SELECT Username FROM User WHERE UserID = %s", (user,))
            user_name = cursor.fetchone()
            if user_name:
                user_list.append({ "userID": user ,"userName": user_name[0]})
        cursor.close()
        conn.close()
        return jsonify({'users': user_list})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json() or {}
    prompt = payload.get('prompt', '')
    print(f"\n🟡 Received prompt: {prompt}")

    try:
        reply, templates = generate_portfolio_reply(prompt)
        print("🟢 AI reply:", reply)
        print("🟢 Templates:", templates)

        return jsonify({
            'reply': reply or "⚠️ No reply generated.",
            'templates': [{'label': t} for t in templates] if templates else []
        })
    except Exception as e:
        print("🔴 Error in /chat:", e)
        return jsonify({
            'reply': '⚠️ Error processing your request.',
            'templates': []
        }), 500

if __name__ == '__main__':
    app.run(debug=True)









    







        










