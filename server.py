import json as json
import main as main
from flask import Flask, flash, request, redirect, render_template, url_for
from rauth.service import OAuth2Service


# Flask config
# SQLALCHEMY_DATABASE_URI = 'sqlite:///facebook.db'
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
DEBUG = True
FB_CLIENT_ID = '139079890034808'
FB_CLIENT_SECRET = '1d0e2ce535280f461398e3dbabcae697'

# Flask setup
app = Flask(__name__)
app.config.from_object(__name__)

# rauth OAuth 2.0 service wrapper
graph_url = 'https://graph.facebook.com/'
facebook = OAuth2Service(name='facebook',
                         authorize_url='https://www.facebook.com/dialog/oauth',
                         access_token_url=graph_url + 'oauth/access_token',
                         client_id=app.config['FB_CLIENT_ID'],
                         client_secret=app.config['FB_CLIENT_SECRET'],
                         base_url=graph_url)

# views
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/facebook/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    params = {'redirect_uri': redirect_uri}
    return redirect(facebook.get_authorize_url(**params))

def new_decoder(payload):
    return json.loads(payload.decode('utf-8'))

@app.route('/facebook/authorized')
def authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('authorized', _external=True)
    data = dict(code=request.args['code'], redirect_uri=redirect_uri)

    session = facebook.get_auth_session(data=data,decoder=new_decoder)

    # the "me" response
    # me = session.get('me').json()
    # # flash('Logged in as ' + me['access_token'])
    # print(session.__dict__)

    main.main(session.__dict__['access_token'])
    return redirect(url_for('index'))

  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
