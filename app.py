from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import date
from config import user, task, app, send_mail


@app.route('/',methods=['GET','POST'])
def logar():
    
    if request.method == 'POST':
        usuario = request.form["usuario"]
        senha = str(request.form["senha"])
        
        try: 
            usuario = user.find_one({"usuario":usuario})

            if usuario['senha'] == senha:
                
                return redirect(url_for(".listar_tarefas", id_usuario=usuario['_id']))
            
            else:

                flash("Usuário ou Senha Invalidos")
                return redirect(url_for(".logar"))

        except:
            
            flash("Usuário ou Senha Invalidos")
            return redirect(url_for(".logar"))

    return render_template('login.html')


@app.route('/registrar',methods=['GET','POST'])
def registrar():
    
    if request.method == 'POST':
        data = str(date.today())
        usuario = {
            "nome": request.form["nome"],
            "usuario": request.form["usuario"],
            "senha": request.form["senha"],
            "email": request.form["email"],
            "criacao": data
        }

        user.insert_one(usuario)
        msg = "<h1>Ola, {} </h1>".format(request.form["nome"])

        send_mail(request.form["email"],msg)

        return redirect(url_for(".logar"))

    return render_template('registrar.html')


@app.route('/listar-tarefas/<string:id_usuario>',methods=['GET','POST'])
def listar_tarefas(id_usuario):
        

    if request.method == 'POST':
        data = str(date.today())
        tarefa = {
            "dono": id_usuario,
            "nome": request.form["tarefa"],
            "status": 0,
            "criacao": data
        }

        task.insert_one(tarefa)

        return redirect(url_for(".listar_tarefas", id_usuario=id_usuario))

    tarefas = task.find({"dono":id_usuario})

    return render_template('lista_tarefas.html', tarefas=tarefas,id_usuario=id_usuario)

@app.route('/finalizar/<string:nome_tarefa>/<string:id_usuario>',methods=['GET','POST'])
def finalizar_tarefa(nome_tarefa,id_usuario):

    data = str(date.today())
    tarefa = task.find_one({"nome":nome_tarefa})

    task.replace_one({'_id':tarefa['_id']}, {
        "_id":tarefa['_id'],
        "dono": id_usuario,
        "nome": tarefa['nome'],
        "status": 1,
        "criacao": data
        })

    return redirect(url_for(".listar_tarefas", id_usuario=id_usuario))


@app.route('/deletar/<string:nome_tarefa>/<string:id_usuario>',methods=['GET','POST'])
def deletar_tarefa(nome_tarefa,id_usuario):

    tarefa = task.find_one({"nome":nome_tarefa})
    task.remove({"nome":nome_tarefa})

    return redirect(url_for(".listar_tarefas", id_usuario=id_usuario))


if __name__ =="__main__":
    app.run(debug=True)
    
