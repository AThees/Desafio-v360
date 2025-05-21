import streamlit as st
from sqlalchemy import func 
from models import Session, ToDoList, ToDoItem


session = Session()
st.set_page_config(page_title="ToDo App", layout="centered")

st.title("📝 ToDo")

def checkSameNamelist(name):
    return session.query(ToDoList).filter_by(title=name).first() is not None

# Sidebar para criar nova lista
with st.sidebar:
    st.header("Nova Lista")
    new_list = st.text_input("Nome da Lista")
    if st.button("Criar Lista"):
        if(new_list.strip() == ""):
            st.error("O nome da lista não pode estar vazio.")
        else:
            if checkSameNamelist(new_list):
                st.error("Já existe uma lista com esse nome.")
            else:
                session.add(ToDoList(title=new_list))
                session.commit()
                st.rerun()

# Listar listas existentes
lists = session.query(ToDoList).all()
list_titles = [l.title for l in lists]
if not list_titles:
    st.warning("Nenhuma lista criada ainda.")
    st.stop()

# current_list = session.query(ToDoList).filter_by(title=selected).first()

with st.sidebar:
    st.header("Listas Criadas")
    selected = st.pills(
        "Listas",
        options=list_titles,
        format_func=lambda x: x,
        selection_mode="single",
    )
    
    if selected is None:
        selected = list_titles[-1]
        
    date = st.date_input("Data", format="DD/MM/YYYY", value="today")
        
    current_list = session.query(ToDoList).filter_by(title=selected).first()
    

# Adicionar nova tarefa
new_task = st.text_input("Nova tarefa")
col1, col2 = st.columns([0.85, 0.20])
with col1:
    if st.button("Adicionar Tarefa"):
        if new_task.strip() != "":
            session.add(ToDoItem(content=new_task, list_id=current_list.id, date=date))
            session.commit()
            st.rerun()
with col2:
    if st.button("Deletar lista"):
        session.delete(current_list)
        session.commit()
        st.rerun()

# Mostrar itens da lista
st.subheader(f"Tarefas de: {current_list.title} para o dia {date.strftime("%d/%m/%Y")}")
items = session.query(ToDoItem).filter(ToDoItem.list_id == current_list.id, func.date(ToDoItem.date) == date).all()
for item in items:
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        if st.checkbox(item.content, value=item.completed, key=item.id):
            item.completed = not item.completed
            session.commit()

    with col2:
        if st.button("🗑", key=f"del{item.id}"):
            session.delete(item)
            session.commit()
            st.rerun()


