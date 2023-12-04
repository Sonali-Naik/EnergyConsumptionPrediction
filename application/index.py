from flask import Flask, render_template      

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def main():
    return render_template("home.html")

@app.route("/AboutUs")
def aboutus():
    return render_template("group8.html")
    
@app.route("/output")
def output():
    return render_template("output.html")
    
if __name__ == "__main__":
    app.run(debug=True)