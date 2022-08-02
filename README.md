# Getting started with Box OAuth 2.0 using Python & Flask
> This is the companion app to illustrate [this medium article](https://medium.com/@barbosa-rmv/getting-started-with-box-oauth-2-0-using-python-flask-77607441170d). Check it out.

## Installation

> Get the code
```bash
git clone git@github.com:barduinor/ui-elements-python.git
cd ui-elements-python
```

> Set up your virtual environment
```bash
python3.10 -m venv venv
source ./venv.bin/activate
pip install -r requirements.txt
```

> Create your application environment
```bash
cp .env.example .env
```

> Generate a secret key for your app
```bash
python -c "import os; print(os.urandom(24).hex())"
```

> Generate a fernet (encryption) key for your app
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key()"
```

> Edit your .env file and fill in the information
```
# True for development, False for production
DEBUG=True

# Flask ENV
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY='YOUR_SECRET_KEY'
FERNET_KEY='YOU_ENCRYPTION_KEY'

# Box OAuth
CLIENT_ID='YOUR_CLIENT_ID'
CLIENT_SECRET='YOUR_CLIENT_SECRET'
REDIRECT_URI='http://localhost:5000/oauth/callback'
```

> Run your server
```bash
flask run
```

> Point your browser to the server (e.g http://127.0.0.1:5000).
> Inspect your browser console to see the javascript events.
> Server events will be printed on the terminal.