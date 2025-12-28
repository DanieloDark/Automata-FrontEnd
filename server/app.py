import os
from flask import Flask, render_template

# Point to the root directory (one level up from /server)
base_dir = os.path.abspath('..')
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)