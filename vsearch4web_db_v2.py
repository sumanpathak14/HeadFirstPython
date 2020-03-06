from flask import Flask, render_template, request, escape
import vsearch
from DBcm import UseDatabase, ConnectionError, CredentialsError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = { 'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'vsearch',
            'database': 'vsearchlogDB',}

def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results."""
    
    with UseDatabase(app.config['dbconfig']) as cursor:
        __SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""

        cursor.execute(__SQL, (req.form['phrase'],
                           req.form['letters'], 
                           req.remote_addr,
                           req.user_agent.browser,
                           res,))

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(vsearch.search4letters(phrase,letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('***** Logging failed with this error', str(err))
    return render_template('results.html',the_title=title,the_results=results,the_phrase=phrase,the_letters=letters)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            __SQL = """select phrase, letters, ip, browser_String, results from log"""
        
            cursor.execute(__SQL)
            contents = cursor.fetchall()
    
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'
    

if __name__ == '__main__':
    app.run(debug=True)

