from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import extractor, youtube

SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_master.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    keywords = db.Column(db.String(200), nullable=True)
    videoUrl = db.Column(db.Text, nullable=True)
    video_thumbnail = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        
        task_keywords = extractor.get_keywords(task_content)
        task_keywords = ' '.join([str(elem) for elem in task_keywords])
        task_yt = youtube.get_video(task_keywords)


        new_task = Todo(content=task_content, keywords=task_keywords, videoUrl=task_yt[0], video_thumbnail=task_yt[1])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task_keywrds = ' '.join([str(elem) for elem in extractor.get_keywords(task.content)])
        task.keywords = task_keywrds
        task_yt = youtube.get_video(task_keywrds)
        task.videoUrl = task_yt[0]
        task.video_thumbnail = task_yt[1]
        

        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)