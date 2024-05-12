"""for launching a visualization"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
<<<<<<< HEAD
    return render_template('plot.html')
=======
    # return 'Hello, World!'
    df = pd.read_csv('response_clean.csv')
    plt.figure(figsize=(8, 6))
    plt.plot(df['X'], df['Y'])
    plt.title('Data Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)

    # Save the plot to a file
    plot_path = 'static/plot.png'
    plt.savefig(plot_path)
    plt.close()

    # Render the HTML template with the plot
    # return render_template('index.html', plot_path=plot_path)

>>>>>>> 0f29128c3dfe9e356fc9f4a700f44d6d37d20a72


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
<<<<<<< HEAD


=======
>>>>>>> 0f29128c3dfe9e356fc9f4a700f44d6d37d20a72
