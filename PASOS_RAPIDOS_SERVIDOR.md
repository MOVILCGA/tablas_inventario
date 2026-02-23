# 🚀 Pasos Rápidos para Activar el Aplicativo en el Servidor

## ✅ Pasos para que funcione desde celulares corporativos:

### **1. Subir código al servidor**
- Copiar toda la carpeta `App` al servidor (el que tenga acceso VPN)

### **2. En el servidor, abrir PowerShell o CMD como Administrador**

### **3. Configurar Firewall (SOLO UNA VEZ)**
```powershell
# Permitir puerto 5500 en el firewall
New-NetFirewallRule -DisplayName "Flask App - Puerto 5500" -Direction Inbound -LocalPort 5500 -Protocol TCP -Action Allow
```

### **4. Obtener la IP del servidor**
```powershell
ipconfig
# Buscar "Dirección IPv4" (ejemplo: 192.168.1.100)
# ANOTAR ESTA IP - Es la que usarán los usuarios
```

### **5. Ir a la carpeta App y ejecutar:**
```powershell
cd "C:\ruta\a\tu\App"
python App.py
```

### **6. Verificar que funciona:**
- Abrir navegador en el mismo servidor
- Ir a: `http://localhost:5500`
- Debe aparecer la página de login

---

## 📱 Para los usuarios (Desde sus celulares corporativos):

### **Pasos para cada usuario:**

1. **Conectar el celular a la VPN corporativa** ✅

2. **Abrir el navegador** (Chrome en Android, Safari en iPhone)

3. **Escribir en la barra de direcciones:**
   ```
   http://IP_DEL_SERVIDOR:5500
   ```
   *(Reemplazar IP_DEL_SERVIDOR con la IP que anotaste en el paso 4)*

4. **Iniciar sesión** con sus credenciales

5. **Instalar como app (OPCIONAL pero recomendado):**
   - **Android (Chrome):** Aparecerá una notificación "Agregar a pantalla de inicio" → Tocar
   - **iPhone (Safari):** Botón Compartir (cuadrado con flecha) → "Agregar a pantalla de inicio"

6. **¡Listo!** La app quedará instalada y funcionará cuando tengan VPN activa

---

## ⚠️ IMPORTANTE - Antes de que los usuarios accedan:

### **Cambiar App.py para producción:**

Abrir `App.py` y cambiar la última línea:

```python
# ANTES (desarrollo):
app.run(host='0.0.0.0', port=5500, debug=True)

# DESPUÉS (producción):
app.run(host='0.0.0.0', port=5500, debug=False)
```

**¿Por qué?** `debug=True` muestra información sensible si hay errores (no seguro en producción).

---

## 🔒 Para mayor seguridad (Recomendado):

### **Usar HTTPS en lugar de HTTP:**

1. **Instalar Waitress (mejor servidor):**
   ```powershell
   pip install waitress
   ```

2. **Modificar última línea de App.py:**
   ```python
   from waitress import serve
   print("✅ Servidor iniciado - Accesible en: http://IP_DEL_SERVIDOR:5500")
   serve(app, host='0.0.0.0', port=5500, threads=4)
   ```

---

## ✅ Resumen rápido:

1. ✅ Subir código al servidor
2. ✅ Abrir puerto 5500 en firewall  
3. ✅ Anotar IP del servidor
4. ✅ Ejecutar `python App.py`
5. ✅ Cambiar `debug=True` a `debug=False`
6. ✅ Compartir URL: `http://IP:5500` a los usuarios
7. ✅ Usuarios conectan VPN y abren la URL
8. ✅ ¡Funciona! 🎉

---

## ❓ Si algo no funciona:

### **El servidor no arranca:**
- Verificar que Python esté instalado: `python --version`
- Verificar que Flask esté instalado: `pip install flask flask-login flask-mysqldb python-dotenv`

### **Los celulares no pueden acceder:**
- Verificar que el firewall permita el puerto 5500
- Verificar que la IP del servidor sea correcta
- Verificar que los usuarios estén conectados a la VPN
- Verificar que el servidor esté ejecutando: `python App.py`

### **La app no se instala en el celular:**
- **Android:** Debe usar Chrome
- **iPhone:** Debe usar Safari
- La app solo se instala si acceden por HTTPS (o localhost)

---

**¡Eso es todo!** Con estos pasos, tus compañeros podrán acceder desde sus celulares corporativos. 📱✅
