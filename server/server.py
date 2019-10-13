import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import db

app = bottle.Bottle()



@enable_cors
@app.route("/api/tasks/")
def index():
    tasks = []
    total = db.count_todos()
    for i in db.return_todos():
        tasks.append({
            'description':i.description,
            'is_completed':i.is_completed,
            'uid':i.id
            })
    return {"tasks": tasks, "total": total}


@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET", "PUT", "DELETE"])
def show_or_modify_task(uid):
    if bottle.request.method == "GET":
        return tasks_db[uid].to_dict()
    elif bottle.request.method == "PUT":
        if "description" in bottle.request.json:
            db.modify_todo(uid, bottle.request.json['description'])
            if "is_completed" not in bottle.request.json:
                if db.is_completed(uid):
                    db.task_swap(uid)
        if "is_completed" in bottle.request.json:
            db.task_swap(uid)
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        db.delete_todo(uid)
        return f"Deleted task {uid}"


@enable_cors
@app.route("/api/tasks/", method="POST")
def add_task():
    desc = bottle.request.json['description']
    try:
        if bottle.request.json['is_completed'] == 'true':
            is_completed = True
    except:
        is_completed = False
    db.add(desc, is_completed)
    return "OK"

app.install(CorsPlugin(origins=['http://localhost:5000']))

if __name__ == "__main__":
    #Раскоментируйте для первоначального создания таблицы
    #db.init_db(db.default)

    bottle.run(app, host="localhost", port=5001)
