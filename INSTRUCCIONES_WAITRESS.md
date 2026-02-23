# 🚀 Instrucciones para Usar Waitress

## ✅ ¿Qué es Waitress y por qué usarlo?

**Waitress** es un servidor WSGI profesional que:
- ✅ Permite ejecutar la aplicación **sin necesidad de VS Code abierto**
- ✅ Mejor rendimiento que el servidor de desarrollo de Flask
- ✅ Más estable para producción
- ✅ Puede ejecutarse como servicio de Windows

---

## 📋 Pasos para Configurar

### **1. Instalar Waitress (si no está instalado):**

Abrir PowerShell o CMD y ejecutar:

```powershell
pip install waitress
```

O si usas entorno virtual:

```powershell
# Activar entorno virtual primero
Entorno_V\Scripts\activate

# Luego instalar
pip install waitress
```

---

### **2. Verificar que App.py esté configurado:**

El archivo `App.py` ya está configurado para usar Waitress. La última sección debe verse así:

```python
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5500, threads=4)
```

✅ **Ya está configurado correctamente**

---

## 🎯 Formas de Ejecutar la Aplicación

### **OPCIÓN 1: Usar el archivo .bat (Más fácil)**

1. **Doble click en:** `run_app.bat`
2. Se abrirá una ventana de CMD
3. Verás mensajes de inicio
4. La aplicación estará corriendo
5. **Puedes cerrar VS Code** - la app seguirá funcionando

**Para detener:** Cerrar la ventana de CMD o presionar `Ctrl+C`

---

### **OPCIÓN 2: Desde PowerShell/CMD manualmente**

1. Abrir PowerShell o CMD
2. Ir a la carpeta App:
   ```powershell
   cd "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
   ```
3. Activar entorno virtual (si lo usas):
   ```powershell
   Entorno_V\Scripts\activate
   ```
4. Ejecutar:
   ```powershell
   python App.py
   ```

---

### **OPCIÓN 3: Desde Visual Studio Code**

1. Abrir VS Code en la carpeta App
2. Abrir terminal (Ctrl + `)
3. Ejecutar:
   ```powershell
   python App.py
   ```

---

## ✅ Verificar que Funciona

### **1. Ver mensajes en la consola:**

Deberías ver algo como:
```
============================================================
🚀 Servidor Flask iniciado con Waitress
============================================================
✅ Aplicativo accesible en: http://0.0.0.0:5500
📱 Para acceder desde celulares: http://TU_IP:5500
============================================================
```

### **2. Probar en navegador:**

Abrir navegador y ir a:
```
http://localhost:5500
```

✅ Debe aparecer la página de login

---

## 🔄 Diferencias: Flask vs Waitress

| Característica | Flask (app.run) | Waitress |
|---------------|-----------------|----------|
| **VS Code necesario** | ❌ Sí (normalmente) | ✅ No |
| **Rendimiento** | Básico | ✅ Mejor |
| **Producción** | ❌ No recomendado | ✅ Recomendado |
| **Múltiples usuarios** | Limitado | ✅ Mejor |
| **Estabilidad** | Básica | ✅ Mayor |

---

## 🛠️ Solución de Problemas

### **Error: "No module named 'waitress'"**

**Solución:**
```powershell
pip install waitress
```

O si usas entorno virtual:
```powershell
Entorno_V\Scripts\activate
pip install waitress
```

---

### **Error: "Puerto 5500 ya en uso"**

**Solución:**
1. Cerrar otras instancias de la aplicación
2. O cambiar el puerto en App.py:
   ```python
   serve(app, host='0.0.0.0', port=5501, threads=4)  # Cambiar a 5501
   ```

---

### **La aplicación se cierra al cerrar la ventana**

**Esto es normal** - para que siga corriendo después de cerrar:
- Usar Task Scheduler (ver guía de servidor dedicado)
- O usar NSSM para crear servicio de Windows

---

## 📝 Notas Importantes

1. ✅ **Waitress ya está configurado** en App.py
2. ✅ **Puedes ejecutar sin VS Code** usando `run_app.bat`
3. ✅ **Mejor rendimiento** que Flask por defecto
4. ✅ **Listo para producción**

---

## 🎉 ¡Listo!

Ahora puedes:
- ✅ Ejecutar la app con `run_app.bat`
- ✅ Cerrar VS Code - la app seguirá funcionando
- ✅ Acceder desde celulares corporativos
- ✅ Usar en producción

**¡Tu aplicación está lista para funcionar sin VS Code!** 🚀
