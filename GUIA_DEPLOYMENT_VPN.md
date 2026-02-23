# Guía de Deployment para Acceso Móvil Corporativo vía VPN

## 📱 Configuración del Aplicativo como PWA para Móviles Corporativos

Esta guía explica cómo configurar el aplicativo "Visualización de Tablas CGA" para que sea accesible desde dispositivos móviles corporativos conectados a través de VPN.

---

## 🎯 Requisitos Previos

1. **Servidor con acceso a la VPN corporativa**
2. **IP estática o dominio interno** accesible desde la VPN
3. **Puerto disponible** (recomendado: 5500 o 80/443)
4. **Certificado SSL** (recomendado para producción, especialmente para PWA)

---

## 📋 Paso 1: Configuración del Servidor

### Opción A: Servidor Local con IP Estática

1. **Obtener IP estática del servidor:**
   ```bash
   # En Windows (PowerShell como administrador)
   ipconfig
   # Nota la dirección IPv4 (ejemplo: 192.168.1.100)
   ```

2. **Configurar firewall:**
   - Permitir el puerto 5500 (o el que uses) en el firewall de Windows
   - Ir a: Panel de Control > Firewall de Windows > Configuración avanzada
   - Crear regla de entrada para el puerto TCP 5500

3. **Modificar App.py:**
   ```python
   # En la última línea de App.py, cambiar:
   app.run(host='0.0.0.0', port=5500, debug=False)  # debug=False en producción
   ```

### Opción B: Servidor en la Nube/Intranet

1. **Configurar dominio interno** (ejemplo: `tablas-cga.empresa.local`)
2. **Asignar DNS interno** que apunte al servidor
3. **Configurar proxy reverso** (opcional, con Nginx o IIS)

---

## 📋 Paso 2: Configuración para Producción

### Actualizar App.py para Producción:

```python
if __name__ == '__main__':
    # Para producción con VPN
    app.run(host='0.0.0.0', port=5500, debug=False, threaded=True)
    
    # O usar un servidor WSGI como Waitress o Gunicorn:
    # from waitress import serve
    # serve(app, host='0.0.0.0', port=5500)
```

### Instalar servidor WSGI (Recomendado):

```bash
pip install waitress
```

Luego en App.py:
```python
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5500, threads=4)
```

---

## 📋 Paso 3: Configurar HTTPS (Muy Recomendado para PWA)

Las PWA requieren HTTPS para funcionar completamente (excepto en localhost).

### Opción A: Certificado SSL Interno (Self-Signed)

1. **Generar certificado** (OpenSSL):
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
   ```

2. **Modificar App.py:**
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5500, debug=False, 
               ssl_context=('cert.pem', 'key.pem'))
   ```

### Opción B: Usar Nginx como Proxy Reverso

Configurar Nginx para HTTPS y proxy a Flask:

```nginx
server {
    listen 443 ssl;
    server_name tablas-cga.empresa.local;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5500;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📋 Paso 4: Acceso desde Móviles Corporativos

### Para iOS (iPhone/iPad):

1. **Conectar el dispositivo a la VPN corporativa**
2. **Abrir Safari** (no otros navegadores para PWA)
3. **Navegar a:** `https://IP_DEL_SERVIDOR:5500` o `https://tablas-cga.empresa.local`
4. **Instalar la PWA:**
   - Tocar el botón "Compartir" en Safari
   - Seleccionar "Agregar a pantalla de inicio"
   - La app aparecerá como una app nativa

### Para Android:

1. **Conectar el dispositivo a la VPN corporativa**
2. **Abrir Chrome** (o navegador basado en Chromium)
3. **Navegar a:** `https://IP_DEL_SERVIDOR:5500` o `https://tablas-cga.empresa.local`
4. **Instalar la PWA:**
   - Aparecerá una notificación "Agregar a pantalla de inicio"
   - O ir a menú > "Agregar a pantalla de inicio"
   - La app aparecerá como una app nativa

---

## 📋 Paso 5: Configuración de VPN para Usuarios

### Instrucciones para los usuarios:

1. **Conectarse a la VPN corporativa** antes de abrir la app
2. **Abrir la app instalada** en su dispositivo móvil
3. **Ingresar credenciales** (si es necesario)
4. **La app funcionará** como una aplicación nativa

### Nota importante:
- La app **solo funcionará cuando el dispositivo esté conectado a la VPN**
- Si se desconecta la VPN, la app no podrá acceder al servidor
- Los usuarios pueden mantener la app instalada, pero necesitan VPN para usarla

---

## 📋 Paso 6: Actualizar URLs en Service Worker (si cambia el servidor)

Si cambias la IP o dominio del servidor, actualiza el archivo `sw.js`:

```javascript
// Actualizar las URLs en urlsToCache si es necesario
const urlsToCache = [
  '/',
  '/static/CSS/Estilos.css',
  // ... etc
];
```

---

## 🔒 Consideraciones de Seguridad

1. **Autenticación:** La app ya tiene sistema de login incorporado
2. **VPN:** El acceso está protegido por la VPN corporativa
3. **HTTPS:** Recomendado especialmente para producción
4. **Firewall:** Solo permitir acceso desde la red VPN

---

## 🐛 Solución de Problemas

### La app no se instala:

- **iOS:** Asegúrate de usar Safari, no Chrome
- **Android:** Usa Chrome o navegador basado en Chromium
- **Verificar HTTPS:** Las PWA requieren HTTPS (excepto localhost)
- **Verificar manifest:** Abrir `https://tu-servidor:5500/manifest.json` en el navegador

### La app no se conecta:

- **Verificar VPN:** El dispositivo debe estar conectado a la VPN
- **Verificar IP:** Confirmar que la IP del servidor es correcta
- **Verificar firewall:** El puerto debe estar abierto
- **Verificar servidor:** El servidor Flask debe estar corriendo

### La app no carga recursos:

- **Verificar Service Worker:** Revisar consola del navegador (F12)
- **Limpiar caché:** Configuración del navegador > Limpiar datos
- **Verificar rutas:** Las rutas de archivos estáticos deben ser correctas

---

## 📝 Configuración Ejemplo para App.py Final

```python
if __name__ == '__main__':
    # OPCIÓN 1: Desarrollo simple
    # app.run(host='0.0.0.0', port=5500, debug=True)
    
    # OPCIÓN 2: Producción con Waitress
    from waitress import serve
    print("Servidor iniciado en http://0.0.0.0:5500")
    print("Accesible desde VPN en: https://TU_IP:5500")
    serve(app, host='0.0.0.0', port=5500, threads=4)
    
    # OPCIÓN 3: Producción con HTTPS
    # app.run(host='0.0.0.0', port=5500, debug=False,
    #         ssl_context=('cert.pem', 'key.pem'))
```

---

## ✅ Checklist de Deployment

- [ ] Servidor configurado con IP estática o dominio
- [ ] Puerto del firewall abierto
- [ ] App.py configurado para producción (debug=False)
- [ ] HTTPS configurado (recomendado)
- [ ] Service Worker funcionando
- [ ] Manifest.json accesible
- [ ] Probado desde dispositivo móvil conectado a VPN
- [ ] Instalación PWA exitosa en dispositivos de prueba
- [ ] Documentación para usuarios creada

---

## 📞 Soporte

Para problemas adicionales, contactar al equipo de TI de la empresa.

---

**Última actualización:** Enero 2025
