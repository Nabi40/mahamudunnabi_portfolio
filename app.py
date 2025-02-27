from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder=".")  # Use the current directory for templates
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Email Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not all([fname, lname, email, subject, message]):
            flash("All fields are required!", "danger")
            return redirect(url_for("contact"))

        try:
            msg = Message(
                subject=f"New Contact: {subject}",
                sender=app.config["MAIL_DEFAULT_SENDER"],
                recipients=["mahamudunn2245@gmail.com"],
                body=f"Name: {fname} {lname}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

        return redirect(url_for("contact"))

    return render_template("index.html")  # Flask will now find it in the same directory

if __name__ == "__main__":
    app.run(debug=True)
