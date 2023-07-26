from flask import Flask, redirect, request, render_template, url_for
from flask import session as login_session
import pyrebase


app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)



config = {
  "apiKey": "AIzaSyC4_U8YiiTfot120IBRiFopvGhDGUCfEuU",
  "authDomain": "mini-project-38f3d.firebaseapp.com",
  "databaseURL": "https://mini-project-38f3d-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "mini-project-38f3d",
  "storageBucket": "mini-project-38f3d.appspot.com",
  "messagingSenderId": "59876948560",
  "appId": "1:59876948560:web:35a71b7c7ab464d7ec2f55"
}

firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db= firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

# Your code should be below
@app.route('/' , methods=['POST','GET'])
def home_page():
    return render_template( "home.html") 
    
@app.route('/product' , methods=['POST','GET'])
def prodoccts_page():
    return render_template("product.html") 

@app.route('/cart')
def cart_page():
    if not login_session['user']:
        return redirect(url_for('signin'))
    UID = login_session['user']['localId']
    pr = db.child('Users').child(UID).child("Products").get().val()
    print(pr)
    return render_template("cart.html", pr=pr) 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method== 'POST' :
        email = request.form['email']
        password = request.form['password']
        user_name=request.form['username']
        
        try: 
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['user']['localId']
            user = { "username" : user_name , 'password' :password}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('prodoccts_page'))

        except Exception as e:
            print("SIGN UP ERROR:", e)
            error = 'AUTHENTICATION FAILED'

    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('prodoccts_page'))
        except:
        # Exception as e:
        #      print("SIGN IN ERROR:", e)
            return redirect(url_for("signin"))
    return render_template("signin.html")



@app.route("/toy")
def toy():
    if not login_session['user']:
        return redirect(url_for('signin'))
    print(login_session['user'])
    UID = login_session['user']['localId']
    db.child('Users').child(UID).child("Products").push({"Product" : "Woodie doll"})
    return redirect(url_for( "cart_page"))


@app.route("/shoes")
def sh():
    if not login_session['user']:
        return redirect(url_for('signin'))
    UID = login_session['user']['localId']
    db.child('Users').child(UID).child("Products").push({"Product" : "Aifroce shoes"})
    return redirect(url_for( "cart_page"))

@app.route ("/signout")
def signout():
    login_session['user'] = None 
    auth.current_user = None 
    return redirect(url_for("signin"))
# Your code should be above

if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)
