from re import M
from traceback import print_tb
from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)

conexion = sqlite3.connect('db/tecnoglass.db', check_same_thread=False)
consultas = conexion.cursor()

# TABLA DE USUARIOS
# conexion.execute('''
#                 CREATE TABLE IF NOT EXISTS usuarios
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 CEDULA TEXT NOT NULL,
#                 NOMBRE TEXT NOT NULL,
#                 DIRECCION TEXT NOT NULL,
#                 TELEFONO TEXT NOT NULL,
#                 NACIONALIDAD TEXT NOT NULL,
#                 CORREO TEXT NOT NULL);
#                 ''')

# print ('Tabla de usuarios creada')

# CREAR USUARIO
# @app.route('/usuario', methods=['POST'])
# def usuario():
#   CEDULA = request.json['CEDULA']
#   NOMBRE = request.json['NOMBRE']
#   DIRECCION = request.json['DIRECCION']
#   TELEFONO = request.json['TELEFONO']
#   NACIONALIDAD = request.json['NACIONALIDAD']
#   CORREO = request.json['CORREO']

#   consultas.execute("SELECT * FROM usuarios WHERE CEDULA =?", (CEDULA,))
#   usuarios_existe = consultas.fetchone()
#   if usuarios_existe:
#     return jsonify({'mensaje': "El usuario ya fue creado ⚠️"}), 400
  
#   consultas.execute("INSERT INTO usuarios (CEDULA, NOMBRE, DIRECCION, TELEFONO, NACIONALIDAD, CORREO) VALUES(?, ?, ?, ?, ?, ?)", (CEDULA, NOMBRE, DIRECCION, TELEFONO, NACIONALIDAD, CORREO))

#   conexion.commit()
#   return jsonify({'mensaje': "Usuario Creado exitosamente ✅"}), 200

# # LISTAR USUARIOS
# @app.route('/listar', methods=['GET'])
# def listar():
#   consultas.execute("SELECT * FROM usuarios")
#   listar_usarios = consultas.fetchall()
#   return jsonify(listar_usarios)

# # LISTAR USUARIO POR CEDULA | NOMBRE
# @app.route('/listar_usario',  methods=['POST'])
# def listar_usario():
#   CEDULA = request.json['CEDULA']
#   NOMBRE = request.json['NOMBRE']

#   consultas.execute("SELECT * FROM usuarios WHERE CEDULA=? OR NOMBRE=?", (CEDULA, NOMBRE))
#   lista = consultas.fetchall()
#   if not bool(lista):
#     return jsonify({"mensaje": "No se encontraron resultados ❌"}), 400
#   else:
#     return jsonify(lista)

# # ACTULIZAR USUARIO
# @app.route('/actualiar_usario', methods=['PUT'])
# def actuliar_usario():
#   ID = request.json['ID']
#   CEDULA = request.json['CEDULA']
#   NOMBRE = request.json['NOMBRE']
#   DIRECCION = request.json['DIRECCION']
#   TELEFONO = request.json['TELEFONO']
#   NACIONALIDAD = request.json['NACIONALIDAD']
#   CORREO = request.json['CORREO']

#   consultas.execute("SELECT * FROM usuarios WHERE CEDULA=?", (CEDULA,))
#   usuario_existe = consultas.fetchone()

#   if usuario_existe is not None:
#     return jsonify({'mensaje': "Usuario ya existe ❌"}), 400
#   else:
#       consultas.execute("UPDATE usuarios SET CEDULA=?, NOMBRE=?, DIRECCION=?, TELEFONO=?, NACIONALIDAD=?, CORREO=? WHERE ID=?", (CEDULA, NOMBRE, DIRECCION, TELEFONO, NACIONALIDAD, CORREO, ID))
#       conexion.commit()
#       return jsonify({'mensaje': 'Usuario actulizado correctamente ✅'})
  

# # ELIMINAR USIARIO
# @app.route('/eliminar_usuario', methods=['DELETE'])
# def eliminar_usuario():
#   ID = request.json['ID']
#   consultas.execute("DELETE FROM usuarios WHERE ID=?", (ID,)).fetchone()

#   conexion.commit()
#   return jsonify({'mensaje': "usuario eliminado con exito"})


# # ORDEN DE VIDRIOS DE UN CLIENTE

# # TABLA DE ORDENES
# # conexion.execute('''
# #                 CREATE TABLE IF NOT EXISTS ordenes
# #                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                 NUMERO_ORDEN TEXT NOT NULL,
# #                 CLIENTE INTEGER NOT NULL,
# #                 FECHA_ORDEN TEXT NOT NULL,
# #                 ESTADO TEXT NOT NULL DEFAULT 'SOLICITADO',
# #                 FOREIGN KEY(CLIENTE) REFERENCES usarios(ID));
# #                 ''')

# # print ('Tabla de Orden creada')

# # INGRESAR UNA ORDEN
# @app.route('/orden', methods=['POST'])
# def orden():
#   NUMERO_ORDEN = request.json['NUMERO_ORDEN']
#   CLIENTE = request.json['CLIENTE']
#   FECHA_ORDEN = request.json['FECHA_ORDEN']

#   consultas.execute("SELECT * FROM ordenes WHERE NUMERO_ORDEN=?", (NUMERO_ORDEN,))
#   orden_existe = consultas.fetchone()

#   if orden_existe: 
#     return jsonify({'mensaje': "Numero de orden ya existe ⚠️"}), 400

#   consultas.execute("INSERT INTO ordenes (NUMERO_ORDEN, CLIENTE, FECHA_ORDEN) VALUES (?, ?, ?)", (NUMERO_ORDEN, CLIENTE, FECHA_ORDEN))

#   conexion.commit()
#   return jsonify({'mensaje': "Orden creada con existo ✅"}), 200

# # ACUTLIZAR EL ESTADO DE UNA ORDEN
# @app.route('/actulizar_orden', methods=['PUT'])
# def actulizar_orden():

#   NUMERO_ORDEN = request.json['NUMERO_ORDEN']
#   ESTADO = request.json['ESTADO']

#   consultas.execute("SELECT COUNT(*) FROM ordenes WHERE NUMERO_ORDEN=?", (NUMERO_ORDEN,))
#   orden_existe = consultas.fetchone()[0] == 0
#   if orden_existe:
#     return jsonify({'mensaje': "Numero de orden no existe"}), 400

#   if ESTADO == "APROBADA":
#     consultas.execute("UPDATE ordenes SET ESTADO =? WHERE NUMERO_ORDEN=?", (ESTADO, NUMERO_ORDEN))
#     conexion.commit()
#     return  jsonify({'mensaje': "Oreden aprobada con exito ✅"}), 200
#   elif ESTADO == "ANULADA":
#     consultas.execute("UPDATE ordenes SET ESTADO =? WHERE NUMERO_ORDEN=?", (ESTADO, NUMERO_ORDEN))   
#     conexion.commit()
#     return jsonify({'mensaje': "Oreden anulada ⚠️"}), 200
#   else:
#     return jsonify({'mensaje': "Ingresar un estado correcto"}), 400


#TABLA DETALLE DE ORDENES
conexion.execute('''
                CREATE TABLE IF NOT EXISTS detalles_orden
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_ORDEN TEXT NOT NULL,
                DESCRIPCION TEXT NOT NULL,
                CANTIDAD INTEGER NOT NULL DEFAULT 0,
                PRECIO INTEGER NOT NULL DEFAULT 1,
                TOTAL INTEGER NULL,
                FOREIGN KEY(ID_ORDEN) REFERENCES ordenes(ID));
                ''')

print ('Tabla de detalle orden creada')

# AGREGAR ITEMS O DETALLES
@app.route('/detalle_orden', methods=['PUT'])
def detalle_orden():
  ID_ORDEN = request.json['ID_ORDEN']
  DESCRIPCION = request.json['DESCRIPCION']
  CANTIDAD = request.json['CANTIDAD']
  PRECIO = request.json['PRECIO']

  consultas.execute("SELECT ESTADO FROM ordenes WHERE ID=?", (ID_ORDEN,))
  orden = consultas.fetchone()
  if orden is None:
    return jsonify({'mensaje': "La orden especificada no existe ⚠️"})
  estado_orden = orden[0]
  print(estado_orden)
  if estado_orden == 'ANULADA':
    return jsonify({'mensaje': "La orden espefcificada esta anualda ⚠️"})

  consultas.execute("INSERT INTO detalles_orden (ID_ORDEN, DESCRIPCION, CANTIDAD, PRECIO) VALUES (?,?,?,?)", (ID_ORDEN, DESCRIPCION, CANTIDAD, PRECIO))
  
  consultas.execute("SELECT SUM(cantidad * precio) FROM detalles_orden WHERE ID_ORDEN=?", (ID_ORDEN,))
  TOTAL = consultas.fetchone()[0]
  consultas.execute('''UPDATE detalles_orden SET TOTAL=? WHERE id=?''', (TOTAL, ID_ORDEN))

  conexion.commit()
  return jsonify({'mensaje': "Detalles de la orden guardados con exito ✅"})

if __name__ == '__main__':
  app.run()