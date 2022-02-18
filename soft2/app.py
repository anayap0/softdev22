from flask import Flask, render_template, request, redirect
import shelve

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

# password page
@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    with shelve.open('logins') as s:
      try:
        if s[request.form['username']] == request.form['password']:
            user = request.form['username']
            return render_template('index.html')
        else:
          return render_template('login.html', error="Login Failed")
      except KeyError:
        return render_template('login.html', error="Sign Up First!")
      s.sync()
      s.close()
  return render_template('login.html')

# signup 
@app.route('/signup', methods=['POST', 'GET'])
def signup():
  error = None
  if request.method == 'POST':
      s = shelve.open('logins')
      try:
        s[request.form['username']]
        error = "Invalid username or password. Please try again!"
      except KeyError:
        s[request.form['username']] = request.form['password']
        return redirect(url_for('login'))
      s.close()
  return render_template('signup.html', error=error)

if __name__ == '__main__':
  app.run(
  host='0.0.0.0',
  debug=True,
  port=8080
  )
