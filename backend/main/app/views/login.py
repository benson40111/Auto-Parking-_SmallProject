from app import app, jinja
from sanic_auth import Auth
from sanic import response


app.config.AUTH_LOGIN_ENDPOINT = 'login'

auth = Auth(app)
app.auth = auth

class User:
    def __init__(self, username, password):
        self.name = username
        self.id = username
        self.password = password

user = User('admin', 'password')

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user.name and password == user.password:
            auth.login_user(request, user)
            return response.redirect('/')
    return jinja.render('login.html', **locals())


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/logout')
