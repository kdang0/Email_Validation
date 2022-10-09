from flask_app.model.email import Email
from flask_app import app
from flask import redirect, request, render_template, session

email_dict = {}
@app.route('/register', methods=['POST'])
def register():
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.insert(request.form)
    if "emails" not in session:
        session["emails"] = email_dict
    an_email = Email.getCreatedEmail()
    email_dict[an_email.id] = an_email.email_address
    session["emails"] = email_dict
    print("SESSION:", session['emails'])
    return redirect('/success')

@app.route('/')
def index():
    if 'emails' in session:
        print("CURRENT SESSION VAL",session['emails'])
    return render_template('index.html')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        "id" : id
    }
    print("DELETING")
    Email.delete(data)
    print(email_dict)
    del email_dict[id]
    session["emails"] = email_dict
    return redirect('/success')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

@app.route('/success')
def success():
    a_email  = Email.getCreatedEmail()
    emails = Email.get_all()
    if emails:
        return render_template("success.html", emails=emails, a_email = a_email)  #Change THIS
    return redirect('/')