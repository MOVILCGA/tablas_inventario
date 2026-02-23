# 🖥️ Guía para Servidor Dedicado (No computadora personal)

## ✅ SÍ, tu código funciona perfectamente en servidor dedicado

De hecho, es **MEJOR** usar un servidor dedicado porque:
- ✅ Más estable (siempre encendido)
- ✅ Más seguro
- ✅ Mejor rendimiento
- ✅ Acceso controlado

---

## 🔧 Configuración según Tipo de Servidor

### **OPCIÓN 1: Windows Server**

Los pasos son **similares** a una PC, pero con permisos de administrador:

1. **Conectarse al servidor** (RDP - Escritorio Remoto)

2. **Abrir PowerShell como Administrador**

3. **Configurar Firewall:**
   ```powershell
   New-NetFirewallRule -DisplayName "Flask App - Puerto 5500" -Direction Inbound -LocalPort 5500 -Protocol TCP -Action Allow
   ```

4. **Subir código** (por red, USB, o comprimir y subir)

5. **Obtener IP del servidor:**
   ```powershell
   ipconfig
   # Anotar la IP (ejemplo: 192.168.10.50)
   ```

6. **Ejecutar aplicación:**
   ```powershell
   cd "C:\ruta\a\tu\App"
   python App.py
   ```

7. **¡Listo!** Los usuarios acceden con: `http://IP_SERVIDOR:5500`

---

### **OPCIÓN 2: Linux Server (Ubuntu/Debian/CentOS)**

Para servidores Linux necesitas comandos diferentes:

#### **A. Instalar Python y dependencias:**
```bash
# Actualizar sistema
sudo apt update  # Ubuntu/Debian
# O: sudo yum update  # CentOS/RHEL

# Instalar Python 3 y pip
sudo apt install python3 python3-pip  # Ubuntu/Debian
# O: sudo yum install python3 python3-pip  # CentOS/RHEL

# Instalar dependencias de Flask
pip3 install flask flask-login flask-mysqldb python-dotenv
```

#### **B. Configurar Firewall (Linux):**
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 5500/tcp
sudo ufw reload

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=5500/tcp
sudo firewall-cmd --reload
```

#### **C. Subir código al servidor:**
```bash
# Usando SCP desde tu PC:
scp -r App/ usuario@IP_SERVIDOR:/ruta/destino/

# O subir manualmente por SFTP
```

#### **D. Ejecutar aplicación:**
```bash
cd /ruta/a/tu/App
python3 App.py
```

#### **E. Obtener IP del servidor:**
```bash
ip addr show
# O simplemente:
hostname -I
```

---

### **OPCIÓN 3: Servidor Virtual o Cloud**

Si es servidor virtual (VMware, Hyper-V, Azure, AWS):

1. **Conectarse al servidor** (RDP para Windows, SSH para Linux)

2. **Seguir pasos según sistema operativo** (Windows o Linux arriba)

3. **Importante para Cloud:**
   - Configurar **Security Groups** / **Firewall Rules** en la plataforma cloud
   - Permitir puerto 5500 en el panel de control de Azure/AWS
   - Asignar IP estática (Elastic IP en AWS, Static IP en Azure)

---

## 🚀 Hacer que el Servidor Ejecute Automáticamente (Recomendado)

### **Windows Server - Servicio como Servicio:**

#### **Opción A: Usar Task Scheduler (Más fácil)**

1. Abrir **Programador de tareas** (Task Scheduler)
2. Crear tarea básica
3. Configurar:
   - **Nombre:** Flask App CGA
   - **Trigger:** Al iniciar sesión (o al iniciar sistema)
   - **Acción:** Iniciar programa
   - **Programa:** `python`
   - **Argumentos:** `C:\ruta\completa\a\App\App.py`
   - **Iniciar en:** `C:\ruta\completa\a\App`

4. Guardar y probar

#### **Opción B: Usar NSSM (Más profesional)**

1. Descargar NSSM: https://nssm.cc/download
2. Instalar como servicio:
   ```powershell
   nssm install FlaskAppCGA
   # En la ventana que aparece:
   # Path: C:\Python\python.exe  (ruta a tu Python)
   # Startup directory: C:\ruta\a\tu\App
   # Arguments: App.py
   ```
3. Iniciar servicio:
   ```powershell
   nssm start FlaskAppCGA
   ```

### **Linux Server - Usar systemd (Recomendado):**

1. Crear archivo de servicio:
   ```bash
   sudo nano /etc/systemd/system/flaskapp-cga.service
   ```

2. Agregar este contenido:
   ```ini
   [Unit]
   Description=Flask App CGA - Visualización de Tablas
   After=network.target

   [Service]
   Type=simple
   User=tu_usuario
   WorkingDirectory=/ruta/a/tu/App
   ExecStart=/usr/bin/python3 /ruta/a/tu/App/App.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Habilitar y iniciar:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable flaskapp-cga
   sudo systemctl start flaskapp-cga
   ```

4. Verificar estado:
   ```bash
   sudo systemctl status flaskapp-cga
   ```

---

## 🔒 Configuración para Producción en Servidor

### **Usar Waitress (Mejor que Flask por defecto):**

```python
# Al final de App.py, reemplazar:
if __name__ == '__main__':
    from waitress import serve
    print("✅ Servidor Flask iniciado en puerto 5500")
    print("🌐 Accesible en: http://IP_SERVIDOR:5500")
    serve(app, host='0.0.0.0', port=5500, threads=4)
```

Instalar Waitress:
```bash
# Windows:
pip install waitress

# Linux:
pip3 install waitress
```

---

## 📋 Checklist para Servidor Dedicado

- [ ] Identificar sistema operativo del servidor
- [ ] Conectarse al servidor (RDP/SSH)
- [ ] Subir código de la aplicación
- [ ] Instalar Python y dependencias
- [ ] Configurar firewall del servidor
- [ ] Configurar firewall de la plataforma (si es cloud)
- [ ] Obtener IP estática del servidor
- [ ] Ejecutar aplicación (o configurar como servicio)
- [ ] Probar acceso desde otro equipo
- [ ] Configurar para que inicie automáticamente
- [ ] Probar acceso desde celular con VPN

---

## ⚠️ Consideraciones Importantes

### **IP del Servidor:**
- Si es servidor interno: usar IP local (ejemplo: 192.168.10.50)
- Si es servidor cloud: usar IP pública asignada
- Considerar usar dominio interno (ejemplo: `tablas-cga.empresa.local`)

### **Seguridad:**
- ✅ Firewall configurado correctamente
- ✅ Solo acceso desde VPN
- ✅ `debug=False` en producción
- ✅ Usuarios con credenciales seguras

### **Backup:**
- Mantener copia del código en otro lugar
- Configurar respaldos automáticos si es necesario

---

## 🆘 Si Necesitas Ayuda Específica

Dime qué tipo de servidor tienes y te doy pasos exactos:

1. **Windows Server** → Usar PowerShell
2. **Linux Ubuntu/Debian** → Usar terminal Linux
3. **Linux CentOS/RHEL** → Usar terminal Linux  
4. **VMware/Hyper-V** → Conectarse por RDP/SSH primero
5. **Azure/AWS** → Configurar Security Groups + seguir pasos según OS

---

**¡Tu código funciona en CUALQUIER servidor! Solo cambian los comandos según el sistema operativo.** 🚀✅
