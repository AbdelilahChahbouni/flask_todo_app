from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import ToDo
from .forms import ToDoForm
from . import db

main = Blueprint('main', __name__)
@main.route('/test')
def test():
    return '''
        <html>
            <head>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <h1>Hello</h1>
            </body>
        </html>
    '''




@main.route('/test-style')
def test_style():
    return render_template('test.html')


@main.route('/')
def home():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    todos = ToDo.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', todos=todos)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(title=form.title.data, description=form.description.data,
                    completed=form.completed.data, owner=current_user)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('todo_form.html', form=form, action='Add')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    todo = ToDo.query.get_or_404(id)
    if todo.owner != current_user:
        return redirect(url_for('main.dashboard'))
    form = ToDoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.completed = form.completed.data
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('todo_form.html', form=form, action='Edit')

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = ToDo.query.get_or_404(id)
    if todo.owner == current_user:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('main.dashboard'))
