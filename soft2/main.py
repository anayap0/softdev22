from flask import Flask, render_template, request
import shelve

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

  if __name__ == '__main__':
  app.run(
  host='0.0.0.0',
  debug=True,
  port=8080
  )