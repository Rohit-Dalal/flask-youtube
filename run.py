from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__, template_folder='template', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rohit:password@localhost/flask-youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Thisissecret'


db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__='Post'
    id = db.Column('S.NO.', db.Integer(), primary_key = True)
    title = db.Column('Title', db.String(400), nullable=False)
    author = db.Column('Author', db.String(50), nullable=False)
    post = db.Column('Post', db.Text(), nullable=False)
    date = db.Column('Date', db.VARCHAR(), nullable=False, default=datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%y'))

    def __repr__(self):
        return "<Post(id=%s, title=%s, author=%s, post=%s)" % (self.id, self.title, self.author, self.post)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_title = request.form['title']
        user_author = request.form['author']
        user_post = request.form['body']

        user_post = Post(title=user_title, author=user_author, post=user_post)
        db.session.add(user_post)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        posts = db.session.query(Post).all()
        return render_template('index.html', posts=posts)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    user_delete = db.session.query(Post).filter_by(id=user_id).first_or_404()
    db.session.delete(user_delete)
    db.session.commit()

    flash('Deleted succssfully!', 'success')
    return redirect(url_for('index'))


@app.route('/post/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_post(user_id):
    if request.method == 'POST':
        user_data = db.session.query(Post).filter_by(id=user_id).first()
        user_data.title =  request.form['title']
        user_data.author = request.form['author']
        user_data.post =  request.form['body']

        db.session.commit()
        posts = db.session.query(Post).all()
        return render_template('index.html', posts=posts)
        
    else:
        user_post = db.session.query(Post).filter_by(id=user_id).all()
        return render_template('edit.html', user_post=user_post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)