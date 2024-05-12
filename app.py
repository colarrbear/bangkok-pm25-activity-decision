from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_csv('response_clean.csv')
    plt.figure(figsize=(8, 6))
    plt.scatter(df['concern_level'], df['change_behavior'])
    plt.title('Change in Behavior vs Concern Level')
    plt.xlabel('Concern Level')
    plt.ylabel('Change in Behavior')
    # plt.grid(True)
    plot_path = 'static/plot.png'
    plt.savefig(plot_path)
    return render_template('index.html', plot_path=plot_path)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)