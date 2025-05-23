from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class ToDoList(Base):
    __tablename__ = 'todo_lists'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    items = relationship("ToDoItem", backref="todo_list", cascade="all, delete")

class ToDoItem(Base):
    __tablename__ = 'todo_items'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    date = Column(Date)
    completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey('todo_lists.id'), nullable=False)
    important = Column(Boolean, default=False)


# Conexão com SQLite
engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
