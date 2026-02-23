# 🔧 Configurar como Servicio de Windows con NSSM

## ✅ ¿Por qué usar NSSM?

Con **nssm.exe** puedes:
- ✅ Ejecutar la app **sin tener ninguna ventana abierta**
- ✅ La app **sigue funcionando** aunque cierres VS Code
- ✅ La app **inicia automáticamente** al encender el servidor
- ✅ La app **sigue corriendo** aunque cierres sesión
- ✅ **Mejor para producción** - funciona como servicio real

---

## 📋 Paso 1: Tener nssm.exe

Veo que ya tienes `nssm.exe` en:
```
Descargas > nssm-2.24 > win64 > nssm.exe
```

**Copiar nssm.exe a una ubicación permanente:**

1. Crear carpeta: `C:\Tools\nssm\`
2. Copiar `nssm.exe` ahí
3. O dejarlo donde está y usar la ruta completa

---

## 📋 Paso 2: Obtener Rutas Necesarias

Necesitas estas rutas:

### **A. Ruta a Python:**
```powershell
where python
```
**Ejemplo:** `C:\Users\atecnologia2\AppData\Local\Programs\Python\Python313\python.exe`

### **B. Ruta a App.py:**
**Ejemplo:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\App.py`

### **C. Ruta de trabajo (carpeta App):**
**Ejemplo:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App`

---

## 📋 Paso 3: Instalar como Servicio

### **Método A: Usando PowerShell (Recomendado)**

Abrir **PowerShell como Administrador** y ejecutar:

```powershell
# Cambiar estas rutas según tu configuración:
$nssm = "C:\Tools\nssm\nssm.exe"  # O la ruta donde está nssm.exe
$python = "C:\Users\atecnologia2\AppData\Local\Programs\Python\Python313\python.exe"
$appPath = "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\App.py"
$workingDir = "C:\Users\atecnologia2\Desktop\Visualización_tablas_\App"

# Instalar servicio
& $nssm install FlaskAppCGA $python "$appPath"

# Configurar directorio de trabajo
& $nssm set FlaskAppCGA AppDirectory "$workingDir"

# Configurar para que se inicie automáticamente
& $nssm set FlaskAppCGA Start SERVICE_AUTO_START

# Configurar descripción
& $nssm set FlaskAppCGA Description "Aplicativo Visualización de Tablas CGA"

# Configurar para que se reinicie si falla
& $nssm set FlaskAppCGA AppRestartDelay 10000

# Iniciar servicio
& $nssm start FlaskAppCGA
```

---

### **Método B: Usando Interfaz Gráfica (Más fácil)**

1. **Abrir CMD como Administrador**

2. **Ir a la carpeta de nssm:**
   ```cmd
   cd "C:\Users\atecnologia2\Downloads\nssm-2.24\win64"
   ```

3. **Ejecutar nssm con interfaz:**
   ```cmd
   nssm install FlaskAppCGA
   ```

4. **En la ventana que aparece, llenar:**

   **Tab "Application":**
   - **Path:** `C:\Users\atecnologia2\AppData\Local\Programs\Python\Python313\python.exe`
     *(O la ruta donde está tu Python - usar `where python` para encontrarla)*
   
   - **Startup directory:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App`
   
   - **Arguments:** `App.py`

   **Tab "Details":**
   - **Display name:** `Flask App CGA`
   - **Description:** `Aplicativo Visualización de Tablas CGA`

   **Tab "I/O":**
   - **Output:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\output.log`
   - **Error:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\error.log`
   
   *(Crear carpeta `logs` primero si no existe)*

   **Tab "Exit Actions":**
   - Marcar: **Restart application**
   - **Delay:** `10000` (10 segundos)

5. **Click en "Install service"**

6. **Iniciar servicio:**
   ```cmd
   nssm start FlaskAppCGA
   ```

---

## 📋 Paso 4: Verificar que Funciona

### **Verificar estado del servicio:**

```powershell
# Ver estado
nssm status FlaskAppCGA

# O desde PowerShell:
Get-Service FlaskAppCGA
```

### **Probar en navegador:**

Abrir navegador y ir a:
```
http://localhost:5500
```

✅ Debe aparecer la página de login

---

## 🛠️ Comandos Útiles de NSSM

### **Iniciar servicio:**
```cmd
nssm start FlaskAppCGA
```

### **Detener servicio:**
```cmd
nssm stop FlaskAppCGA
```

### **Reiniciar servicio:**
```cmd
nssm restart FlaskAppCGA
```

### **Ver logs en tiempo real:**
```cmd
nssm status FlaskAppCGA
```

### **Eliminar servicio (si necesitas):**
```cmd
nssm remove FlaskAppCGA confirm
```

---

## 📋 Paso 5: Configurar para Inicio Automático

El servicio ya debería iniciarse automáticamente, pero puedes verificar:

1. Abrir **Services** (servicios.msc)
2. Buscar **"Flask App CGA"**
3. Click derecho > **Properties**
4. En **Startup type:** Seleccionar **Automatic**
5. Click **OK**

---

## ✅ Ventajas de Usar NSSM

| Característica | Sin NSSM | Con NSSM |
|----------------|----------|----------|
| **Cerrar VS Code** | ❌ Se detiene | ✅ Sigue funcionando |
| **Cerrar sesión** | ❌ Se detiene | ✅ Sigue funcionando |
| **Reiniciar servidor** | ❌ Hay que iniciar manual | ✅ Inicia automático |
| **Ventana abierta** | ❌ Necesaria | ✅ No necesaria |
| **Producción** | ❌ No recomendado | ✅ Recomendado |

---

## 🐛 Solución de Problemas

### **Error: "Access Denied"**

**Solución:** Ejecutar PowerShell/CMD **como Administrador**

---

### **Error: "Service not found"**

**Solución:** Verificar que el servicio esté instalado:
```cmd
nssm status FlaskAppCGA
```

Si no existe, instalarlo de nuevo.

---

### **El servicio no inicia**

**Solución:**
1. Verificar logs de error:
   ```cmd
   nssm status FlaskAppCGA
   ```
2. Verificar que las rutas sean correctas
3. Probar ejecutar manualmente:
   ```cmd
   python App.py
   ```
   Si funciona manualmente, el problema es la configuración de nssm

---

### **Ver logs del servicio:**

Si configuraste archivos de log:
- **Output:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\output.log`
- **Error:** `C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\logs\error.log`

---

## 📝 Resumen

### **Con Waitress SOLO:**
- ✅ Mejor rendimiento
- ✅ Funciona sin VS Code (si no cierras la terminal)
- ❌ Se detiene si cierras la ventana
- ❌ No inicia automático

### **Con Waitress + NSSM:**
- ✅ Mejor rendimiento (Waitress)
- ✅ Funciona sin VS Code
- ✅ Sigue funcionando aunque cierres todo
- ✅ Inicia automático
- ✅ **Ideal para producción**

---

## 🎯 Recomendación

**Para producción en servidor:**
1. ✅ Usar **Waitress** (ya configurado)
2. ✅ Instalar con **NSSM** como servicio
3. ✅ Configurar inicio automático

**Para pruebas en tu PC:**
- Puedes usar solo `run_app.bat` (más simple)
- O instalar con NSSM si quieres que funcione siempre

---

**¡Con NSSM tu aplicación funcionará como un servicio profesional de Windows!** 🚀✅
