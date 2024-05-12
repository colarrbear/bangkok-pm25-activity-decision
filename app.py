"""for launching a visualization"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('plot.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
