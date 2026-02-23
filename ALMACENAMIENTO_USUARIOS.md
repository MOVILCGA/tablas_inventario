# 💾 Almacenamiento de Usuarios

## ✅ ¿Dónde se Guardan los Usuarios?

Los usuarios que creas desde la interfaz de "Gestión de Usuarios" se guardan en:

```
C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\usuarios.json
```

---

## 📁 Archivo: `usuarios.json`

Este archivo contiene todos los usuarios del sistema en formato JSON.

### **Estructura del archivo:**

```json
{
    "AdmCGA": {
        "password": "Aceros2025*",
        "nombre": "Admin_APP_CGA"
    },
    "IvanPatinioP": {
        "password": "Aceros123*",
        "nombre": "Usuario 1"
    },
    "UsuarioNuevo": {
        "password": "Password123*",
        "nombre": "Nombre Completo"
    }
}
```

---

## 🔄 ¿Cómo Funciona?

### **Al iniciar la aplicación:**

1. ✅ La aplicación busca el archivo `usuarios.json`
2. ✅ Si existe, carga los usuarios desde ahí
3. ✅ Si no existe, crea el archivo con los usuarios iniciales
4. ✅ Los usuarios iniciales siempre se mantienen (AdmCGA, etc.)

### **Al crear un usuario:**

1. ✅ Se agrega al diccionario en memoria
2. ✅ **Se guarda automáticamente en `usuarios.json`**
3. ✅ El usuario queda persistido permanentemente

### **Al eliminar un usuario:**

1. ✅ Se elimina del diccionario en memoria
2. ✅ **Se guarda automáticamente en `usuarios.json`**
3. ✅ El cambio queda persistido permanentemente

---

## ✅ Ventajas de Este Sistema

| Característica | Antes (Solo memoria) | Ahora (Archivo JSON) |
|----------------|---------------------|---------------------|
| **Persistencia** | ❌ Se perdían al reiniciar | ✅ Se mantienen siempre |
| **Backup** | ❌ No se podía hacer | ✅ Puedes copiar el archivo |
| **Portabilidad** | ❌ No se podía mover | ✅ Puedes mover el archivo |
| **Edición manual** | ❌ No se podía | ✅ Puedes editar el JSON |

---

## 📝 Notas Importantes

### **1. Usuarios Iniciales:**

Los siguientes usuarios **siempre estarán presentes** (no se pueden eliminar desde la interfaz):
- `AdmCGA` - Administrador principal

Si eliminas alguno de los usuarios iniciales del archivo JSON manualmente, se restaurarán automáticamente al iniciar la aplicación.

---

### **2. Seguridad:**

⚠️ **IMPORTANTE:** El archivo `usuarios.json` contiene contraseñas en texto plano.

**Recomendaciones:**
- ✅ Mantener el archivo en una ubicación segura
- ✅ No compartir el archivo con usuarios no autorizados
- ✅ Hacer backups regulares
- ✅ Considerar usar hash de contraseñas en el futuro

---

### **3. Backup:**

Para hacer backup de los usuarios:

1. **Copiar el archivo:**
   ```
   usuarios.json → usuarios_backup.json
   ```

2. **O copiar toda la carpeta App** (incluye usuarios.json)

---

### **4. Restaurar Usuarios:**

Si necesitas restaurar usuarios desde un backup:

1. Detener la aplicación
2. Reemplazar `usuarios.json` con el archivo de backup
3. Reiniciar la aplicación

---

## 🔍 Ubicación del Archivo

**Ruta completa:**
```
C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\usuarios.json
```

**Ruta relativa (desde App.py):**
```
./usuarios.json
```

---

## 🛠️ Edición Manual (Opcional)

Puedes editar el archivo `usuarios.json` manualmente si necesitas:

1. **Agregar usuarios rápidamente**
2. **Cambiar contraseñas**
3. **Modificar nombres**

**Ejemplo de agregar usuario manualmente:**

```json
{
    "AdmCGA": {
        "password": "Aceros2025*",
        "nombre": "Admin_APP_CGA"
    },
    "NuevoUsuario": {
        "password": "MiPassword123*",
        "nombre": "Nombre Completo del Usuario"
    }
}
```

**Después de editar:**
- Reiniciar la aplicación para que cargue los cambios

---

## ✅ Resumen

- ✅ **Ubicación:** `App/usuarios.json`
- ✅ **Formato:** JSON
- ✅ **Persistencia:** Automática al crear/eliminar usuarios
- ✅ **Backup:** Copiar el archivo `usuarios.json`
- ✅ **Restauración:** Reemplazar el archivo y reiniciar

---

**¡Los usuarios ahora se guardan permanentemente!** 🎉
