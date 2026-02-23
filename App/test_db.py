import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

def probar_conexion():
    try:
        print("Intentando conectar a DB2 (Local)...")
        conn = MySQLdb.connect(
            host=os.environ.get('MYSQL_HOST_DB2'),
            user=os.environ.get('MYSQL_USER_DB2'),
            passwd=os.environ.get('MYSQL_PASSWORD_DB2'),
            db=os.environ.get('MYSQL_DB_DB2')
        )
        print("✅ CONEXIÓN EXITOSA a la base de datos 'prueba'")
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'ztbsd_seg_ped'")
        tabla = cursor.fetchone()
        
        if tabla:
            print(f"✅ TABLA ENCONTRADA: {tabla[0]}")
            cursor.execute("SELECT COUNT(*) FROM ztbsd_seg_ped")
            print(f"✅ CANTIDAD DE REGISTROS: {cursor.fetchone()[0]}")
        else:
            print("❌ ERROR: La tabla 'ztbsd_seg_ped' NO EXISTE en la base de datos 'prueba'.")
            
        conn.close()
    except Exception as e:
        print(f"❌ FALLO DE CONEXIÓN: {e}")

if __name__ == "__main__":
    probar_conexion()