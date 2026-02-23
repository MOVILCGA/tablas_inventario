# 🚀 Guía Paso a Paso: Instalar Servicio con Waitress + NSSM

## ✅ Objetivo

Instalar tu aplicación como servicio de Windows para que:
- ✅ Funcione **sin tener VS Code abierto**
- ✅ Siga funcionando aunque **cierres todas las ventanas**
- ✅ **Inicie automáticamente** al encender el PC
- ✅ Funcione como un **servicio profesional**

---

## 📋 Paso 1: Verificar que Tienes Todo

### **A. Verificar que tienes nssm.exe:**

Ya lo tienes en:
```
C:\Users\atecnologia2\Downloads\nssm-2.24\win64\nssm.exe
```

✅ **Confirmado**

---

### **B. Verificar que Waitress está instalado:**

Abrir PowerShell y ejecutar:
```powershell
pip list | findstr waitress
```

Si no aparece, instalar:
```powershell
pip install waitress
```

O si usas entorno virtual:
```powershell
cd "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
Entorno_V\Scripts\activate
pip install waitress
```

---

### **C. Encontrar la ruta de Python:**

**Opción 1: Si Python está en PATH**
```powershell
where python
```

**Opción 2: Si usas entorno virtual**
La ruta sería:
```
C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\Entorno_V\Scripts\python.exe
```

**Opción 3: Buscar manualmente**
- Buscar "python.exe" en el explorador de archivos
- O revisar: `C:\Users\atecnologia2\AppData\Local\Programs\Python\`

**Anotar esta ruta** - la necesitarás

---

## 📋 Paso 2: Preparar el Script de Instalación

### **A. Abrir el archivo `instalar_servicio.ps1`**

El script ya está configurado con tus rutas, pero verifica:

1. **Ruta a nssm.exe** (línea 19):
   ```powershell
   $nssmPath = "C:\Users\atecnologia2\Downloads\nssm-2.24\win64\nssm.exe"
   ```
   ✅ Ya está correcto

2. **Ruta a App.py** (línea 21):
   ```powershell
   $appDir = "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
   ```
   ✅ Ya está correcto

3. **Python** - El script lo busca automáticamente, pero si no lo encuentra, te pedirá la ruta.

---

## 📋 Paso 3: Ejecutar el Script

### **IMPORTANTE: Ejecutar como Administrador**

1. **Ir a la carpeta App:**
   ```
   C:\Users\atecnologia2\Desktop\Visualización_tablas_\App
   ```

2. **Click derecho en `instalar_servicio.ps1`**

3. **Seleccionar:** "Ejecutar con PowerShell"

4. **Si aparece advertencia de seguridad:**
   - Click en "Más información"
   - Click en "Ejecutar de todas formas"
   - O ejecutar desde PowerShell como Admin (ver abajo)

---

### **Alternativa: Ejecutar desde PowerShell como Administrador**

1. **Abrir PowerShell como Administrador:**
   - Click en Inicio
   - Buscar "PowerShell"
   - Click derecho > "Ejecutar como administrador"

2. **Ir a la carpeta:**
   ```powershell
   cd "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
   ```

3. **Permitir ejecución de scripts (solo primera vez):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

4. **Ejecutar el script:**
   ```powershell
   .\instalar_servicio.ps1
   ```

---

## 📋 Paso 4: Seguir las Instrucciones del Script

El script te guiará paso a paso:

1. ✅ Verificará que eres administrador
2. ✅ Buscará Python automáticamente
3. ✅ Verificará que nssm.exe existe
4. ✅ Verificará que App.py existe
5. ✅ Creará carpeta de logs
6. ✅ Instalará el servicio
7. ✅ Configurará inicio automático
8. ✅ Iniciará el servicio

**Si el script no encuentra Python automáticamente**, te pedirá que ingreses la ruta manualmente.

---

## 📋 Paso 5: Verificar que Funciona

### **A. Verificar estado del servicio:**

Abrir PowerShell como Administrador:
```powershell
Get-Service FlaskAppCGA
```

Deberías ver:
```
Status   Name               DisplayName
------   ----               -----------
Running  FlaskAppCGA        Flask App CGA
```

---

### **B. Probar en navegador:**

Abrir navegador y ir a:
```
http://localhost:5500
```

✅ Debe aparecer la página de login

---

### **C. Ver logs (opcional):**

Los logs están en:
```
C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\output.log
C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\error.log
```

---

## 🛠️ Comandos Útiles

### **Iniciar servicio:**
```powershell
nssm start FlaskAppCGA
```

### **Detener servicio:**
```powershell
nssm stop FlaskAppCGA
```

### **Reiniciar servicio:**
```powershell
nssm restart FlaskAppCGA
```

### **Ver estado:**
```powershell
nssm status FlaskAppCGA
```

### **Ver en Servicios de Windows:**
1. Presionar `Win + R`
2. Escribir: `services.msc`
3. Buscar: "Flask App CGA"

---

## 🐛 Solución de Problemas

### **Error: "Access Denied" o "No se puede ejecutar"**

**Solución:** Ejecutar PowerShell **como Administrador**

---

### **Error: "Python no encontrado"**

**Solución:**
1. Encontrar la ruta de Python (ver Paso 1.C)
2. Cuando el script pregunte, ingresar la ruta completa
3. Ejemplo: `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\Entorno_V\Scripts\python.exe`

---

### **Error: "nssm.exe no encontrado"**

**Solución:**
1. Verificar que nssm.exe esté en: `C:\Users\atecnologia2\Downloads\nssm-2.24\win64\nssm.exe`
2. Si está en otra ubicación, editar línea 19 del script `instalar_servicio.ps1`

---

### **El servicio se instala pero no inicia**

**Solución:**
1. Ver logs de error:
   ```powershell
   Get-Content "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\error.log"
   ```

2. Verificar que App.py funciona manualmente:
   ```powershell
   cd "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"
   python App.py
   ```

3. Si funciona manualmente pero no como servicio, verificar rutas en nssm:
   ```powershell
   nssm status FlaskAppCGA
   ```

---

### **El servicio inicia pero la app no responde**

**Solución:**
1. Verificar que el puerto 5500 no esté bloqueado por firewall
2. Verificar logs:
   ```powershell
   Get-Content "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\output.log" -Tail 50
   ```

---

## ✅ Verificación Final

Después de instalar, prueba esto:

1. ✅ **Cerrar todas las ventanas** (VS Code, PowerShell, etc.)
2. ✅ **Abrir navegador** y ir a `http://localhost:5500`
3. ✅ **Debe funcionar** - la app sigue corriendo como servicio
4. ✅ **Reiniciar PC** - el servicio debe iniciar automáticamente

---

## 📝 Para el Servidor

Una vez que funcione en tu PC, puedes hacer lo mismo en el servidor:

1. ✅ Copiar el script `instalar_servicio.ps1` al servidor
2. ✅ Ajustar las rutas en el script según el servidor
3. ✅ Ejecutar el script como Administrador
4. ✅ Verificar que funciona

---

## 🎉 ¡Listo!

Con esto, tu aplicación funcionará como un servicio profesional de Windows:
- ✅ Sin necesidad de VS Code
- ✅ Inicio automático
- ✅ Funciona siempre

**¿Listo para probarlo?** Ejecuta el script y sigue las instrucciones. Si tienes algún problema, avísame y te ayudo. 🚀
