from flask import Flask, request

from webapp.model import Task
from jinja2 import Environment, PackageLoader

app = Flask(__name__)
env = Environment(autoescape=True, loader=PackageLoader('webapp', 'templates'))

PAGE_SIZE = 5


def render_tasks(page=0, search=None):
    tasks = None
    if search is not None:
        tasks = Task.objects(name__contains=search)[page*PAGE_SIZE:(page+1)*PAGE_SIZE]
    else:
        tasks = Task.objects[page*PAGE_SIZE:(page+1)*PAGE_SIZE]
    template = env.get_template('tasks.html')
    return template.render(tasks=tasks, page=page)


@app.route('/', methods=['GET'])
def show_tasks():
    page = int(request.args.get('page', 0))
    search = request.args.get('search')

    return render_tasks(page, search)


@app.route('/', methods=['POST'])
def edit_tasks():
    name = request.form['name']
    action = request.form['action']
    if action == 'ADD':
        Task(name).save()

    if action == 'REMOVE':
        tasks = request.form.getlist('tasks')
        Task.objects(id__in=tasks).delete()


    return show_tasks()


# This is for debugger
def port_check(hostname, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((hostname, port))
    except socket.gaierror:
        sock.close()
        return False
    sock.close()
    return result == 0


if __name__ == '__main__':
    # This is for debugger
    debug_port = 5678
    if port_check('debug_host', debug_port):
        import pydevd
        pydevd.settrace('debug_host', port=debug_port, stdoutToServer=True, stderrToServer=True)

    app.run(host='0.0.0.0')
