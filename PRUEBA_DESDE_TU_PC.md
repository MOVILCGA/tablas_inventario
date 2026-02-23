# 📱 Probar desde tu PC - Acceso desde Celulares Corporativos

## ✅ SÍ, puedes probar desde tu PC antes de subir al servidor

**PERO** necesitas cumplir estos requisitos:

---

## 🔍 Requisitos para que Funcione desde tu PC:

### **1. Tu PC debe estar en la red VPN corporativa**
- Tu PC debe estar conectada a la misma VPN que los celulares
- O estar en la misma red local de la empresa

### **2. Obtener la IP de tu PC en la VPN:**

#### **En Windows (PowerShell o CMD):**
```powershell
ipconfig
```

**Buscar:**
- Si estás en VPN: Buscar la IP que empieza con la red VPN (ejemplo: 10.x.x.x o 192.168.x.x)
- Si estás en red local: Buscar "Adaptador de Ethernet" o "Wi-Fi" → "Dirección IPv4"

**Ejemplo de salida:**
```
Adaptador de LAN inalámbrica Wi-Fi:
   Dirección IPv4. . . . . . . . . . . . . . : 192.168.1.50
```

**Anotar esta IP** (ejemplo: `192.168.1.50`)

---

### **3. Configurar Firewall de tu PC:**

#### **Opción A: PowerShell como Administrador**
```powershell
New-NetFirewallRule -DisplayName "Flask App - Puerto 5500" -Direction Inbound -LocalPort 5500 -Protocol TCP -Action Allow
```

#### **Opción B: Panel de Control (Más fácil)**
1. Ir a: **Panel de Control** > **Firewall de Windows** > **Configuración avanzada**
2. Click en **Reglas de entrada** (Inbound Rules)
3. Click en **Nueva regla...**
4. Seleccionar **Puerto** → Siguiente
5. Seleccionar **TCP** y escribir puerto **5500** → Siguiente
6. Seleccionar **Permitir la conexión** → Siguiente
7. Marcar todas las casillas (Dominio, Privada, Pública) → Siguiente
8. Nombre: "Flask App CGA" → Finalizar

---

### **4. Verificar que App.py esté configurado correctamente:**

Abrir `App.py` y verificar que la última línea sea:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)  # ✅ Correcto
```

**IMPORTANTE:** 
- ✅ `host='0.0.0.0'` → Permite conexiones desde otras máquinas
- ❌ `host='127.0.0.1'` o `host='localhost'` → SOLO funciona en tu PC

---

### **5. Ejecutar la aplicación:**

#### **Desde Visual Studio Code:**
1. Abrir terminal en VS Code (Ctrl + `)
2. Ir a la carpeta App:
   ```powershell
   cd App
   ```
3. Ejecutar:
   ```powershell
   python App.py
   ```

#### **O desde PowerShell/CMD:**
```powershell
cd "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
python App.py
```

**Deberías ver algo como:**
```
 * Running on http://0.0.0.0:5500
```

---

### **6. Probar desde tu PC primero:**

Abrir navegador en tu misma PC y probar:
```
http://localhost:5500
```

**O usar la IP de tu PC:**
```
http://192.168.1.50:5500  (reemplazar con tu IP)
```

Si funciona, ¡está listo para probar desde celulares!

---

## 📱 Probar desde Celular Corporativo:

### **Pasos para cada usuario:**

1. **Conectar celular a VPN corporativa** ✅

2. **Abrir navegador** (Chrome en Android, Safari en iPhone)

3. **Escribir en la barra de direcciones:**
   ```
   http://IP_DE_TU_PC:5500
   ```
   
   **Ejemplo:**
   ```
   http://192.168.1.50:5500
   ```
   
   *(Reemplazar `IP_DE_TU_PC` con la IP que anotaste en el paso 2)*

4. **Debería aparecer la página de login** ✅

5. **Iniciar sesión** con credenciales

6. **¡Funciona!** 🎉

---

## ⚠️ IMPORTANTE - Limitaciones de Probar desde tu PC:

### **❌ Problemas si tu PC se apaga:**
- Los usuarios no podrán acceder
- La aplicación se detiene si cierras Visual Studio
- Si tu PC se reinicia, debes volver a ejecutar `python App.py`

### **✅ Soluciones:**
- **Para pruebas:** Está bien usar tu PC
- **Para producción:** Usar servidor dedicado (siempre encendido)

---

## 🔍 Verificar que Funciona:

### **Desde tu PC (misma máquina):**
```
http://localhost:5500
```
✅ Debe funcionar siempre

### **Desde otra PC en la misma red:**
```
http://IP_DE_TU_PC:5500
```
✅ Debe funcionar si están en la misma red

### **Desde celular con VPN:**
```
http://IP_DE_TU_PC:5500
```
✅ Debe funcionar si:
- Tu PC está en la VPN
- El celular está en la VPN
- El firewall permite el puerto 5500

---

## 🐛 Si NO Funciona desde Celular:

### **Problema 1: "No se puede conectar" o "Tiempo de espera agotado"**

**Soluciones:**
1. ✅ Verificar que tu PC esté en la VPN
2. ✅ Verificar que el celular esté en la VPN
3. ✅ Verificar que el firewall permita el puerto 5500
4. ✅ Verificar que `App.py` esté ejecutándose
5. ✅ Verificar que uses la IP correcta (no localhost)

### **Problema 2: "Conexión rechazada"**

**Soluciones:**
1. ✅ Verificar que `host='0.0.0.0'` en App.py (no '127.0.0.1')
2. ✅ Verificar que el puerto 5500 esté abierto en firewall
3. ✅ Verificar que no haya otro programa usando el puerto 5500

### **Problema 3: "Página no encontrada"**

**Soluciones:**
1. ✅ Verificar que la URL sea correcta: `http://IP:5500` (no https)
2. ✅ Verificar que App.py esté corriendo
3. ✅ Probar primero desde tu PC con `http://localhost:5500`

---

## 📋 Checklist Rápido:

- [ ] PC conectada a VPN corporativa
- [ ] IP de tu PC anotada
- [ ] Firewall configurado (puerto 5500 abierto)
- [ ] App.py con `host='0.0.0.0'`
- [ ] App.py ejecutándose (`python App.py`)
- [ ] Probado desde tu PC: `http://localhost:5500` ✅
- [ ] Celular conectado a VPN
- [ ] Probado desde celular: `http://IP_DE_TU_PC:5500` ✅

---

## ✅ Resumen:

**SÍ, puedes probar desde tu PC**, pero:

1. ✅ Tu PC debe estar en la VPN
2. ✅ Abrir puerto 5500 en firewall
3. ✅ Usar `host='0.0.0.0'` en App.py
4. ✅ Ejecutar `python App.py`
5. ✅ Compartir IP de tu PC a los usuarios
6. ✅ Usuarios acceden con: `http://TU_IP:5500`

**Para producción final, mejor usar servidor dedicado** (siempre encendido, más estable).

---

**¡Prueba primero desde tu PC y luego sube al servidor cuando todo funcione!** 🚀
