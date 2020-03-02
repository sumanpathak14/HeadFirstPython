from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return 'Hello from the simple webapp.'
    
@app.route('/page1')
def page1() -> str:
    return 'This is page 1.'
    
@app.route('/page2')
def page1() -> str:
    return 'This is page 2.'
    
@app.route('/page3')
def page1() -> str:
    return 'This is page 3.'
    
if __name__ == '__main__':
    app.run(debug=True)
