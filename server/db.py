import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///todos.sqlite3"
Base = declarative_base()

#дефолтные значения
default = [
    "написать код",
    "покормить морскую свинку",
    "постирать кроссовки",
    "поесть еды",
]

class Todo(Base):
    """
    Описывает структуру таблицы todos для хранения записей
    """

    __tablename__ = "todos"

    id = sa.Column(sa.INTEGER, primary_key=True)
    description = sa.Column(sa.TEXT)
    is_completed = sa.Column(sa.BOOLEAN)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def return_todos():
    """
    возваращает все записи
    """
    session = connect_db()
    todos = session.query(Todo).all()
    return todos

#проверяет есть ли запись в базе с таким id
def in_db(id):
    session = connect_db()
    indb = session.query(Todo).filter(Todo.id == id).all()
    if indb:
        return True
    return False

#добавляет запись в базу
def add(desc, is_compl):
    session = connect_db()
    todo = Todo(
        description = desc,
        is_completed = is_compl
        )
    session.add(todo)
    session.commit()

#Проверка выполнено или нет
def is_completed(id):
    if in_db(id):
        session = connect_db()
        td = session.query(Todo).filter(Todo.id == id).first()
        if td.is_completed == False:
            return False
        else:
            return True

def delete_todo(id):
    if in_db(id):
        session = connect_db()
        td = session.query(Todo).filter(Todo.id == id).first()
        session.delete(td)
        session.commit()

#Изменяет статус задания (выполнено/не выполнено/выполено...)
def task_swap(id):
    if in_db(id):
        session = connect_db()
        td = session.query(Todo).filter(Todo.id == id).first()
        if td.is_completed == False:
            td.is_completed = True
        else:
            td.is_completed = False
        session.flush()
        session.commit()

def modify_todo(id,desc):
    if in_db(id):
        session = connect_db()
        td = session.query(Todo).filter(Todo.id == id).first()
        td.description = desc
        session.flush()
        session.commit()

def count_todos():
    """
    возвращает список, [0] - всего задач, [1] - выполнено
    """
    result = []
    session = connect_db()
    result.append(len(session.query(Todo).all()))
    result.append(len(session.query(Todo).filter(Todo.is_completed == True).all()))
    return result


#Создает дефолтные записи в таблице
def init_db(default):
    for todo in default:
        add(todo, False)
