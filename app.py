from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

username = ""

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():

    global username

    if request.method == 'POST':

        username = request.form['username']

        return redirect('/home')

    return render_template('login.html')

# Home Page
@app.route('/home')
def home():

    search = request.args.get('search')

    if search:
        filtered_tasks = []

        for task in tasks:
            if search.lower() in task['title'].lower():
                filtered_tasks.append(task)

    else:
        filtered_tasks = tasks

    total = len(tasks)

    completed = 0

    pending = 0

    for task in tasks:

        if task['status'] == 'Completed':
            completed += 1
        else:
            pending += 1

    return render_template(
        'home.html',
        tasks=filtered_tasks,
        username=username,
        total=total,
        completed=completed,
        pending=pending
    )

# Add Task
@app.route('/add', methods=['POST'])
def add_task():

    title = request.form['title']

    category = request.form['category']

    priority = request.form['priority']

    task = {
        'title': title,
        'category': category,
        'priority': priority,
        'status': 'Pending'
    }

    tasks.append(task)

    return redirect('/home')

# Complete Task
@app.route('/complete/<int:index>')
def complete(index):

    tasks[index]['status'] = 'Completed'

    return redirect('/home')

# Delete Task
@app.route('/delete/<int:index>')
def delete(index):

    tasks.pop(index)

    return redirect('/home')

# Run Flask
if __name__ == '__main__':
    app.run(debug=True)