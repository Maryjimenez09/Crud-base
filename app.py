from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_unica'



def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='domestica',
        cursorclass=pymysql.cursors.DictCursor,
        ssl_disabled=True
    )

@app.route('/')
def index():
        
    return render_template('index.html')


@app.route('/tarea',methods=["GET","POST"])
def tarea():
    if request.method=="POST":
        nombre=request.form["nombre"]
        prioridad=request.form["prioridad"]
        fecha_inicio=request.form["fecha_inicio"]
        fecha_fin=request.form["fecha_fin"]
        hora=request.form["hora"]
        tipo=request.form["tipo"]
        
        
        try:
            conn = connect_to_db()
            cur = conn.cursor() 
            cur.execute("INSERT INTO tarea (nombre, tipo, fecha_inicio, fecha_fin, hora, prioridad  ) VALUES (%s, %s, %s, %s, %s, %s)",
                        (nombre, tipo, fecha_inicio, fecha_fin, hora, prioridad))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('consulta'))
        except Exception:
            return redirect(url_for('index'))
    return render_template('formu.html')



@app.route('/consulta')
def consulta():
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tarea")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('reporte.html', vertarea=data)
    except Exception:
        return render_template('reporte.html', vertarea=[])
    
# Ruta para agregar una nueva categoría
@app.route('/agregar_categ', methods=['GET', 'POST'])
def agregar_categ():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Consultamos todas las tareas creadas para mostrarlas en el formulario
        cur.execute("SELECT id, nombre, hora FROM tarea")
        vertarea = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener tareas: {e}")
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_tarea = request.form['id_tarea']
        tipo_prioridad = request.form['tipo_prioridad']
        categoria = request.form['categoria']
     

        try:
            conn = connect_to_db()
            cur = conn.cursor()
            # Insertamos los datos en la tabla `categoria`
            cur.execute( "INSERT INTO categoria (id_tarea, tipo_prioridad, categoria) VALUES (%s, %s, %s)",
                        (id_tarea, tipo_prioridad, categoria ))
            conn.commit()
            cur.close()
            conn.close()
            
            flash("Categoría agregada con éxito", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error al agregar la categoría: {e}")
            return redirect(url_for('index'))
    
    return render_template('categoria.html', vertarea=vertarea)


@app.route('/datos')
def datos():
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM categoria")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('reportecategoria.html', vertarea=data)
    except Exception:
        return render_template('reportecategoria.html', vertarea=[])

# Ruta para eliminar una tarea
@app.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_tarea(id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM tarea WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('consulta'))
    except Exception as e:
        return redirect(url_for('index'))
    

# Ruta para editar una tarea existente
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_tarea(id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarea WHERE id=%s", (id,))
        tarea = cur.fetchone()
        cur.close()
        conn.close()

    except Exception as e:

        return redirect(url_for('index'))
    if request.method=="POST":
        nombre=request.form["nombre"]
        prioridad=request.form["prioridad"]
        fecha_inicio=request.form["fecha_inicio"]
        fecha_fin=request.form["fecha_fin"]
        hora=request.form["hora"]
        tipo=request.form["tipo"]
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""UPDATE tarea SET nombre=%s,  prioridad=%s, fecha_inicio=%s,  fecha_fin=%s,  hora=%s,  tipo=%s  WHERE id=%s""", 
                (nombre, prioridad, fecha_inicio, fecha_fin, hora, tipo, id))
    
            conn.commit()
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('consulta'))
        except Exception as e:
                return redirect(url_for('index'))
    return render_template('editar.html', tarea=tarea)



if __name__ == '__main__':
    app.run(debug=True)


