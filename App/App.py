# --- 1. Importacion de librerias ---
import os
import math
import uuid
import json
import MySQLdb
from flask import Flask, flash, render_template, request, jsonify, redirect, url_for,session
from flask_mysqldb import MySQL
# Login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
# Cargar variables de entorno desde el archivo .env
from dotenv import load_dotenv
from datetime import datetime
# Usar Waitress para producción (mejora el rendimiento)
from waitress import serve
from datetime import timedelta

load_dotenv()
# Diccionario para trackear sesiones activas (username: session_id)

# --- 2. Configuración inicial de Flask y seguridad ---
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=30)

# Evitar que el usuario pueda ingresar por el botón "atrás" del navegador una vez que haya cerrado sesión
@app.after_request
def add_header(response):
    # El navegador que no guarde en caché las páginas y que siempre solicite la versión más reciente
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# --- Incio de sesión y seguridad ---
# Llave secreta para las sesiones mas seguras
app.secret_key = os.environ.get('SECRET_KEY')

# Inicializamos el administrador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None

# Clase Usuario para que Flask-Login controle al usuario actual cuando inicie sesión
class Usuario(UserMixin):
    def __init__(self, id, username, nombre):
        self.id = id
        self.username = username
        self.nombre = nombre

# Archivo para guardar usuarios persistentemente
USUARIOS_FILE = os.path.join(os.path.dirname(__file__), 'usuarios.json')

# Usuarios fijos iniciales (sin base de datos)
USUARIOS_INICIALES = {
    'AdmCGA': {'password': 'Aceros2025*', 'nombre': 'Admin_APP_CGA'},
    'IvanPatinioP': {'password': 'Aceros123*', 'nombre': 'Usuario 1'},
    'FabioRodriguez': {'password': 'CGA_Aceros123*', 'nombre': 'Usuario 2'},
    'UsuarioAlternativo': {'password': 'User_CGA_123*', 'nombre': 'Usuario 3'}
}

# Función para cargar usuarios desde archivo JSON
def cargar_usuarios():
    """Cargar usuarios desde archivo JSON, o crear archivo con usuarios iniciales si no existe"""
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
                # Asegurar que los usuarios iniciales siempre estén presentes
                for username, datos in USUARIOS_INICIALES.items():
                    if username not in usuarios:
                        usuarios[username] = datos
                return usuarios
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            return USUARIOS_INICIALES.copy()
    else:
        # Crear archivo con usuarios iniciales si no existe
        guardar_usuarios(USUARIOS_INICIALES)
        return USUARIOS_INICIALES.copy()

# Guardar usuarios en archivo JSON
def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

# Cargar usuarios al iniciar
USUARIOS = cargar_usuarios()

# Función para verificar si un usuario es administrador
def es_admin():
    """Verifica si el usuario actual es administrador (cualquier nivel)"""
    return current_user.is_authenticated and (
        current_user.id == 'AdmCGA' or 
        USUARIOS.get(current_user.id, {}).get('es_admin', False)
    )

# Función para verificar si el usuario es administrador principal
def es_admin_principal():
    """Verifica si el usuario actual es administrador principal (AdmCGA o AdmTI)"""
    return current_user.is_authenticated and current_user.id in ['AdmCGA', 'AdmTI']

# Función para verificar si el usuario es administrador con permisos de gestión
def es_admin_gestion():
    """Verifica si el usuario actual puede gestionar usuarios (AdmCGA, AdmTI o admin con permisos)"""
    if not current_user.is_authenticated:
        return False
    
    # AdmCGA y AdmTI tienen todos los permisos
    if current_user.id in ['AdmCGA', 'AdmTI']:
        return True
    
    # Verificar si es administrador con permisos de gestión
    usuario = USUARIOS.get(current_user.id, {})
    return usuario.get('es_admin', False) and usuario.get('puede_gestionar', False)

@login_manager.user_loader
def load_user(user_id):
    if user_id in USUARIOS:
        return Usuario(user_id, user_id, USUARIOS[user_id]['nombre'])
    return None

# Ruta de login para iniciar sesión
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_form = request.form.get('username')
        clave_form = request.form.get('password')

        # Validación con usuarios
        if usuario_form in USUARIOS and clave_form == USUARIOS[usuario_form]['password']:

            user_obj = Usuario(
                usuario_form,
                usuario_form,
                USUARIOS[usuario_form]['nombre']
            )

            # Iniciar sesión del usuario
            login_user(user_obj)

            # ✅ ACTIVAR TIEMPO DE EXPIRACIÓN DE SESIÓN
            session.permanent = True

            return redirect(url_for('seleccion_db')) 
        
        flash('Usuario o contraseña incorrectos. Pruebe de nuevo.')
            
    return render_template('ingreso.html')

# Ruta para el manifest.json de la PWA
@app.route('/manifest.json')
def manifest():
    manifest_data = {
        "name": "Visualización de Tablas CGA",
        "short_name": "Tablas CGA",
        "description": "Aplicativo corporativo para visualización de tablas de Cía. General de Aceros S.A.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0d2a7a",
        "orientation": "any",
        "icons": [
            {
                "src": url_for('static', filename='imagen_31-remove_fondo.ico', _external=True),
                "sizes": "48x48",
                "type": "image/x-icon"
            },
            {
                "src": url_for('static', filename='image/imagen_31-remove_fondo.png', _external=True),
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": url_for('static', filename='image/imagen_31-remove_fondo.png', _external=True),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["business", "productivity"],
        "scope": "/",
        "lang": "es"
    }
    return jsonify(manifest_data), 200, {'Content-Type': 'application/manifest+json'}

# Ruta de logout para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('login'))


# --- 3. Función para obtener la configuración de la Base de datos (DB) ---
def get_db_config(db_name):
    """Devuelve el diccionario de configuración para la DB seleccionada."""
    # Asegurarse que los nombres de las bases de datos coincidan con las variables de entorno del .env
    if db_name == 'aitv':
        return {
            'host': os.environ.get('MYSQL_HOST_DB1'),
            'user': os.environ.get('MYSQL_USER_DB1'),
            'password': os.environ.get('MYSQL_PASSWORD_DB1'),
            'db': os.environ.get('MYSQL_DB_DB1'),
        }
    elif db_name == 'ai_eop':
        return {
            'host': os.environ.get('MYSQL_HOST_DB2'),
            'user': os.environ.get('MYSQL_USER_DB2'),
            'password': os.environ.get('MYSQL_PASSWORD_DB2'),
            'db': os.environ.get('MYSQL_DB_DB2'),
        }
    return None

# --- 4. Definicion de las columnas de cada tabla ---
COLUMNAS_aitv = [
    'Centro','Material','Descripcion_material','stock'
]

ALIAS_aitv = {
    'Centro': 'Centro','Material': '# material', 'Descripcion_material': 'Material', 'stock': 'Cantidad (Un)'
}


COLUMNAS_ai_eop = [
    "VBELN", "ERDAT", "POSNR_CT", "POSNR", "AUFNR", "ARKTX", "KUNNR",
    "ESTAT_ORD", "FECHA_DESP", "FECHA_ENTREGA_DESPACHOS", "VDATU1","FH_CR_TRAS", "FH_FIN_TRAS"
]

# Establecimiento de alias para columnas de la tabla ztbsd_seg_ped de la DB ai_eop
ALIAS_ai_eop = {
    "VBELN": "# Pedido", "ERDAT": "Fecha", "POSNR_CT": "Cant.", "POSNR": "Pos.", "AUART": "Clase DOC. ventas",
    "SPSTG": "Estado", "AUFNR": "Orden", "MATNR": "# material", "ARKTX": "Material", "KUNNR": "# Cliente",
    "ESTAT_ORD": "Estatus orden", "FECHA_DESP": "F. plan desp", "FECHA_ENTREGA_DESPACHOS": "F. prod-desp", 
    "VDATU1": "Pref. Entrega inicial","FH_CR_TRAS": "Inicio transp.", "FH_FIN_TRAS": "Fin trasnp."
}
# definición de columnas numéricas y de fecha para cada tabla
numeric_cols_aitv = ['Centro', 'Almacen', 'Material', 'stock', 'VALOR_UNITARIO']
date_cols_aitv = []
# numeric_cols_ai_eop = ['MANDT', 'ID', 'VBELN', 'KUNNR', 'POSNR', 'MATNR', 'WERKS', 'NETWR', 'KZWI1', 'KZWI2', 'BRGEW', 'NETPR', 'WAVWR', 'KZWI3', 'KWMENG', 'NTGEW', 'POSNR_OF', 'PERNR_E', 'PEDIDO', 'KURSK', 'PERNR_E2', 'DIA', 'REN', 'UTILIDAD', 'POSNR_ENT', 'NTGEW_ENT', 'LFIMG_ENT', 'PESO_CONT', 'PESO_NO_CONT', 'CANT_ENT', 'PEND_ENT', 'CANT_FAC', 'PEND_FAC', 'PEND_ENT_FAC', 'DIF_FAC', 'DIF_FAC_CTD', 'DIF_ENT_CTD', 'DIF_ENT', 'DIF_ENT_FAC', 'VL_PEND_FAC', 'VL_PEND_ENT', 'VL_PEN_TOT', 'VL_FACT', 'VALOR_UN_PED', 'RFMNG', 'PESO_FACT', 'RFWRT', 'MJAHR', 'CANT_TRAS', 'PESO_TRAS', 'POSNR_CT', 'ORDENES', 'GJAHR', 'MES', 'CANTIDAD_ENTREGADA', 'DIFERENCIA_ENTREGA']
numeric_cols_ai_eop = [
    "VBELN", "POSNR_CT", "POSNR", "AUART", "SPSTG", "ERDAT", "AUFNR", "MATNR", "ARKTX", "KUNNR",
    "ESTAT_ORD"
]
# date_cols_ai_eop = ['ERDAT', 'ERZET', 'VDATU', 'FH_CR_ENT', 'HR_CR_ENTREGA', 'FH_CR_FACT', 'HR_CR_FACT', 'FECHA_EM_ORD', 'ERZET_EM_ORD', 'FH_CR_TRAS', 'HR_CR_TRAS', 'FH_FIN_TRAS', 'HR_FIN_TRAS', 'FH_CR_OF', 'HR_CR_OF', 'VDATU_OF', 'VDATU_CT', 'FECHA_DESP', 'VDATU1', 'FECHA_ENTREGA_DESPACHOS', 'FECHA_RECEPCION']
date_cols_ai_eop = [
    'ERDAT', "FH_CR_TRAS", "FH_FIN_TRAS", "FECHA_ENTREGA_DESPACHOS"
]


# --- 5. Rutas despues de iniciar sesión ---
# 5.1 Configuración de las rutas para la selección y visualización de tablas de las bases de datos
@app.route('/', methods=['GET', 'POST'])
@login_required
def seleccion_db():
    # Configuración de las bases de datos disponibles y sus 
    config_db = {
        'inventario': 'aitv',
        'ztbsd_seg_ped': 'ai_eop'
    }
    # listas de tablas disponibles y sus alias para mostrar
    tablas_disponibles = [
        {'clave': 'inventario', 'nombre': 'Inventario'},
        {'clave': 'ztbsd_seg_ped', 'nombre': 'Seguimiento de pedidos'}
    ]
    # El valor por defecto de cada vez que se carga la pagina es (-- Seleccione una tabla --)
    tabla_seleccionada = request.args.get('tabla')

    if not tabla_seleccionada:
        # No hay tabla seleccionada, mostrar solo el selector
        return render_template('tabla.html',
                               datos=[],
                               nombres_columnas=[],
                               tabla_actual=None,
                               tablas_disponibles=tablas_disponibles,
                               total_paginas=1)
                               
    
    db_seleccionada = config_db.get(tabla_seleccionada, 'aitv')
    config = get_db_config(db_seleccionada)
    
    if not config:
        return "Error: Base de datos no válida", 400
    
    if tabla_seleccionada == 'inventario':
        sql = f"select {', '.join(COLUMNAS_aitv)} from inventario limit 100"
        nombres_columnas = [ALIAS_aitv.get(col, col) for col in COLUMNAS_aitv]
    elif tabla_seleccionada == 'ztbsd_seg_ped':
        sql = f"select {', '.join(COLUMNAS_ai_eop)} from ztbsd_seg_ped limit 100"
        nombres_columnas = [ALIAS_ai_eop.get(col, col) for col in COLUMNAS_ai_eop]
    
    # Conexion a la base de datos y calculo de total de paginas si superan 100 filas
    datos = []
    total_paginas = 1
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        cursor.execute(sql)
        print(sql)
        datos = cursor.fetchall()
        
        # Calcular total de filas para paginación
        table = "inventario" if tabla_seleccionada == 'inventario' else "ztbsd_seg_ped"
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_filas = cursor.fetchone()[0]
        total_paginas = math.ceil(total_filas / 100)
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return render_template('tabla.html', datos=[], nombres_columnas=[], 
                               tabla_actual=tabla_seleccionada,
                               tablas_disponibles=tablas_disponibles, 
                               error_msg="Error de conexión")

    return render_template('tabla.html',
                           datos=datos,
                           nombres_columnas=nombres_columnas,
                           tabla_actual=tabla_seleccionada,
                           tablas_disponibles=tablas_disponibles,
                           total_paginas=total_paginas)


# 5.2 Ruta para obtener datos de la tabla con paginación y ordenamiento
@app.route('/obtener_tabla/<string:tabla_id>')
def obtener_tabla(tabla_id):
    pagina = int(request.args.get('pagina', 1))
    limit = 100
    offset = (pagina - 1) * limit
    
    mapa_tablas = {'inventario': 'aitv', 'ztbsd_seg_ped': 'ai_eop'}
    db_actual = mapa_tablas.get(tabla_id, 'aitv')
    config = get_db_config(db_actual)
    
    if tabla_id == 'inventario':
        cols = COLUMNAS_aitv
        table = "inventario"
        numeric_cols = numeric_cols_aitv
        date_cols = date_cols_aitv
        nombres_columnas = [ALIAS_aitv.get(col, col) for col in cols]
    elif tabla_id == 'ztbsd_seg_ped':
        cols = COLUMNAS_ai_eop
        table = "ztbsd_seg_ped"
        numeric_cols = numeric_cols_ai_eop
        date_cols = date_cols_ai_eop
        nombres_columnas = [ALIAS_ai_eop.get(col, col) for col in cols]
    else:
        return jsonify({'error': 'Tabla no válida'}), 400
    
    orden_col = request.args.get('orden_col')
    orden_dir = request.args.get('orden_dir')
    
    # Contar total de filas
    count_sql = f"SELECT COUNT(*) FROM {table}"
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        cursor.execute(count_sql)
        total_filas = cursor.fetchone()[0]
        total_paginas = math.ceil(total_filas / limit)
        
        # Obtener datos paginados
        order_clause = ""
        if orden_col and orden_col in cols:
            if orden_col in numeric_cols:
                order_clause = f"ORDER BY CAST({orden_col} AS DECIMAL(20,5)) {orden_dir}"
            elif orden_col in date_cols:
                order_clause = f"ORDER BY {orden_col} {orden_dir}"
            else:
                order_clause = f"ORDER BY {orden_col} {orden_dir}"
        
        results = []
        if True:
            if orden_col:
                # Si hay orden, devolver todos los datos sin paginación
                sql = f"SELECT {', '.join(cols)} FROM {table} {order_clause}"
            else:
                sql = f"SELECT {', '.join(cols)} FROM {table} {order_clause} LIMIT {limit} OFFSET {offset}"
            cursor.execute(sql)
            filas = cursor.fetchall()
            results = []
            for fila in filas:
                obj = {cols[i]: (str(fila[i]) if fila[i] is not None else "") for i in range(len(cols))}
                results.append(obj)
        
        cursor.close()
        conn.close()
        return jsonify({'results': results, 'column_order': cols, 'nombres_columnas': nombres_columnas, 'total_paginas': 1, 'initial': len(results) == 0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 5.3 Ruta para búsqueda avanzada
@app.route('/buscar_avanzado/<string:tabla_nombre>', methods=['POST'])
def buscar_avanzado(tabla_nombre):
    # Realiza busqueda para saber a qué base de datos conectar
    mapa_tablas = {'inventario': 'aitv', 'ztbsd_seg_ped': 'ai_eop'}
    db_actual = mapa_tablas.get(tabla_nombre, 'aitv')
    
    config = get_db_config(db_actual)
    data = request.get_json() or {}
    clauses = []
    params = []

    # Parámetros de paginación
    pagina = int(data.get('pagina', 1))
    limit = 100
    offset = (pagina - 1) * limit

    # Determinamos columnas y tabla real según el ID
    if tabla_nombre == 'inventario':
        cols = COLUMNAS_aitv
        table = "inventario"
        nombres_columnas = [ALIAS_aitv.get(col, col) for col in cols]
        # Filtro por descripción de material (Descripcion_material)
        if data.get('advDesMAterial'):
            clauses.append("UPPER(Descripcion_material) LIKE UPPER(%s)")
            params.append(f"%{data['advDesMAterial'].strip()}%")
        # Filtro por código de material (Material)
        if data.get('material'):
            clauses.append("UPPER(Material) LIKE UPPER(%s)")
            params.append(f"%{data['material'].strip()}%")
    else: 
        # Determinar si se busca por cliente
        busca_por_cliente = bool(data.get('name1'))
        
        # SIEMPRE incluir NAME1 en las columnas para poder obtener el nombre del cliente
        # El frontend lo excluirá de la visualización cuando se busque por cliente
        # Insertar NAME1 justo después de KUNNR (# Cliente)
        cols = COLUMNAS_ai_eop.copy()
        if "KUNNR" in cols:
            kunnr_index = cols.index("KUNNR")
            cols.insert(kunnr_index + 1, "NAME1")
        else:
            cols.append("NAME1")
        
        table = "ztbsd_seg_ped"
        nombres_columnas = [ALIAS_ai_eop.get(col, col) for col in cols]
        # Agregar alias para NAME1
        if "NAME1" in cols:
            nombres_columnas[cols.index("NAME1")] = "Cliente"
        
        # Filtro por cliente (NAME1)
        if data.get('name1'):
            clauses.append("UPPER(NAME1) LIKE UPPER(%s)")
            params.append(f"%{data['name1'].strip()}%")
        # Filtro por rango de fechas (ERDAT)
        if data.get('fecha_inicio'):
            clauses.append("ERDAT >= %s")
            params.append(data['fecha_inicio'].strip())
        if data.get('fecha_fin'):
            clauses.append("ERDAT <= %s")
            params.append(data['fecha_fin'].strip())
        # Filtro por número de pedido (VBELN)
        if data.get('vbeln'):
            clauses.append("VBELN = %s")
            params.append(data['vbeln'].strip())

    if not clauses:
        return jsonify({'results': [], 'column_order': cols, 'nombres_columnas': nombres_columnas, 'total_paginas': 1, 'pagina_actual': pagina})

    # Consulta para contar total de resultados
    count_sql = f"SELECT COUNT(*) FROM {table} WHERE " + " AND ".join(clauses)

    # Consulta para obtener resultados paginados
    sql = f"SELECT {', '.join(cols)} FROM {table} WHERE " + " AND ".join(clauses) + f" LIMIT {limit} OFFSET {offset}"

    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        # Obtener total de resultados
        cursor.execute(count_sql, tuple(params))
        total_filas = cursor.fetchone()[0]
        total_paginas = math.ceil(total_filas / limit)
 
        # Obtener resultados paginados
        cursor.execute(sql, tuple(params))
        filas = cursor.fetchall()
 
        resultados = []
        for fila in filas:
            obj = {cols[i]: (str(fila[i]) if fila[i] is not None else "") for i in range(len(cols))}
            resultados.append(obj)
 
        cursor.close()
        conn.close()
        return jsonify({
            'results': resultados,
            'column_order': cols,
            'nombres_columnas': nombres_columnas,
            'total_paginas': total_paginas,
            'pagina_actual': pagina,
            'initial': False
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # <-- Agregado el 500
 
 
# Conexion establecida entre los nombres de los clientes de ai_eop
@app.route('/obtener_clientes')
@login_required
def obtener_clientes():
    try:
        # Usamos la configuración de la base de datos ai_eop
        config = get_db_config('ai_eop')
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
 
        # Consulta para traer nombres únicos de la columna NAME1
        query = "SELECT DISTINCT NAME1 FROM ztbsd_seg_ped WHERE NAME1 IS NOT NULL AND NAME1 != '' ORDER BY NAME1 ASC"
        cursor.execute(query)
 
        # Extraemos los resultados en una lista simple
        clientes = [fila[0] for fila in cursor.fetchall()]
 
        cursor.close()
        conn.close()
 
        return jsonify(clientes)
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return jsonify([]), 500
 
 
# Conexion establecida para obtener los materiales únicos de aitv
@app.route('/obtener_materiales')
@login_required
def obtener_materiales():
    try:
        # Usamos la configuración de la base de datos aitv
        config = get_db_config('aitv')
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
 
        # Consulta para traer descripciones únicas de la columna Descripcion_material
        query = "SELECT DISTINCT Descripcion_material FROM inventario WHERE Descripcion_material IS NOT NULL AND Descripcion_material != '' ORDER BY Descripcion_material ASC"
        cursor.execute(query)
 
        # Extraemos los resultados en una lista simple
        materiales = [fila[0] for fila in cursor.fetchall()]
 
        cursor.close()
        conn.close()
 
        return jsonify(materiales)
    except Exception as e:
        print(f"Error al obtener materiales: {e}")
        return jsonify([]), 500
 
 

def es_admin_gestion():
    """Verifica si el usuario actual es AdmCGA o tiene permisos de gestión"""
    if not current_user.is_authenticated:
        return False
    
    # AdmCGA tiene todos los permisos
    if current_user.id == 'AdmCGA':
        return True
    
    # Verificar si es administrador con permisos de gestión
    usuario = USUARIOS.get(current_user.id, {})
    return usuario.get('es_admin', False) and usuario.get('puede_gestionar', False)
 
@app.route('/gestion_usuarios')
@login_required
def gestion_usuarios():
    # Solo AdmCGA o admin con permisos de gestión pueden acceder
    if not es_admin_gestion():
        flash('No tienes permisos para acceder a esta página.')
        return redirect(url_for('seleccion_db'))
    
    # Preparar lista de usuarios con información de sesión
    usuarios_lista = []
    for username, datos in USUARIOS.items():
        usuario_info = {
            'username': username,
            'nombre': datos['nombre'],
            'password': datos['password'],
            'es_admin': datos.get('es_admin', False),
            'puede_gestionar': datos.get('puede_gestionar', False),
            'sesion_activa': False
        }
        usuarios_lista.append(usuario_info)
    
    return render_template('gestion_usuarios.html', 
                         usuarios=usuarios_lista,
                         es_admin_principal=es_admin_principal(),
                         es_admin_gestion=es_admin_gestion())

@app.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    """Crear nuevo usuario - AdmCGA o admin con permisos de gestión pueden crear usuarios"""
    if not es_admin_gestion():
        return jsonify({'error': 'No tiene permisos para realizar esta acción'}), 403

    data = request.get_json() or request.form.to_dict()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    nombre = data.get('nombre', '').strip()
    es_admin_nuevo = data.get('es_admin', False)

    # Validaciones
    if not username or not password:
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

    if username in USUARIOS:
        return jsonify({'error': 'El usuario ya existe'}), 400

    if len(password) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400

    # Solo AdmCGA o AdmTI pueden dar permisos de administrador
    if es_admin_nuevo and not (es_admin_principal() or current_user.id == 'AdmTI'):
        return jsonify({'error': 'Solo AdmCGA o AdmTI pueden dar permisos de administrador'}), 403

    # Crear nuevo usuario
    nuevo_usuario = {
        'password': password,
        'nombre': nombre or username,
        'es_admin': es_admin_nuevo
    }
    
    # Si es administrador y es creado por AdmCGA o AdmTI, dar permisos de gestión por defecto
    if es_admin_nuevo and (es_admin_principal() or current_user.id == 'AdmTI'):
        nuevo_usuario['puede_gestionar'] = True
    
    USUARIOS[username] = nuevo_usuario

    # Guardar usuarios en archivo JSON para persistencia
    guardar_usuarios(USUARIOS)

    admin_texto = "administrador" if es_admin_nuevo else "usuario"
    gestion_texto = " con permisos de gestión" if es_admin_nuevo and es_admin_principal() else ""
    return jsonify({'success': True, 'message': f'Usuario {username} ({admin_texto}{gestion_texto}) creado exitosamente'}), 200

@app.route('/eliminar_usuario', methods=['POST'])
@login_required
def eliminar_usuario():
    """Eliminar usuario - AdmCGA o admin con permisos de gestión pueden eliminar usuarios"""
    if not es_admin_gestion():
        return jsonify({'error': 'No tiene permisos para realizar esta acción'}), 403

    data = request.get_json() or request.form.to_dict()
    username = data.get('username', '').strip()

    # Validaciones
    if not username:
        return jsonify({'error': 'Usuario es requerido'}), 400

    if username not in USUARIOS:
        return jsonify({'error': 'El usuario no existe'}), 400

    # No permitir eliminar a AdmCGA o AdmTI (solo ellos mismos pueden eliminarse, pero no lo haremos)
    if username in ['AdmCGA', 'AdmTI']:
        return jsonify({'error': 'No se puede eliminar al usuario administrador principal'}), 400
    
    # Admin con permisos no puede eliminarse a sí mismo
    if username == current_user.id and not es_admin_principal():
        return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
 
 
    # Eliminar usuario
    del USUARIOS[username]
 
    # Guardar usuarios en archivo JSON para persistencia
    guardar_usuarios(USUARIOS)
 
    return jsonify({'success': True, 'message': f'Usuario {username} eliminado exitosamente'}), 200
 
@app.route('/obtener_usuarios')
@login_required
def obtener_usuarios():
    """Obtener lista de usuarios - Solo AdmCGA"""
    if not es_admin():
        return jsonify({'error': 'No tiene permisos'}), 403
 
    usuarios_lista = [
        {
            'username': username,
            'nombre': datos['nombre'],
            'sesion_activa': username in sesiones_activas
        }
        for username, datos in USUARIOS.items()
    ]
 
    return jsonify(usuarios_lista)
 
# 8. Conexion establecida a IP
if __name__ == '__main__':

 
    print("=" * 60)
    print("- Aplicativo accesible en: http://192.168.0.66:5500")
    print("- Para acceder desde celulares: http://IP:5500")
    print("=" * 60)
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
 
    # Iniciar servidor con Waitress para producción
    # Opción A: Para acceso local + VPN (recomendado)
    serve(app, host='0.0.0.0', port=5500, threads=4)
 
    # Opción B: Si necesitas IP pública (requiere configuración de router)
    # serve(app, host='0.0.0.0', port=5500, threads=4)
 
    # --- OPCIONES ALTERNATIVAS (comentadas):
    # --- Para desarrollo con Flask (solo si necesitas debug):
    # app.run(host='0.0.0.0', port=5500, debug=True)
 
    # --- Conexion con IP fija específica (si necesitas):
    # app.run(host='192.168.1.29', port=5500, debug=False)
    # app.run(host='192.168.0.66', port=5500, debug=False)