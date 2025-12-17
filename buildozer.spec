[app]

# Título de la aplicación
title = DercoR8

# Nombre del paquete (DEBE SER ÚNICO, cámbialo si es necesario)
package.name = dercor8app

# Dominio (inverso del package.name)
package.domain = com.dercor8

# Directorio fuente
source.dir = .

# Archivos a incluir
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,db

# Versión de la aplicación
version = 1.0.0

# Requerimientos
requirements = python3==3.9.13,kivy==2.2.1,android,plyer

# Versión de Python
python.version = 3.9

# Orientación
orientation = portrait

# Permisos Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK

# API mínimo
android.minapi = 21

# API objetivo
android.api = 31

# NDK
android.ndk = 23b

# SDK
android.sdk = 33

# Píxeles por pulgada
android.minsdk = 21

# Color de pantalla de carga
android.presplash_color = #0a0f14

# Ícono (asegúrate de tener assets/icon.png)
icon.filename = assets/icon.png

# Modo ventana
fullscreen = 0

# Log de depuración
log_level = 2

# Incluir patrones
source.include_patterns = assets/*,data/*

# Excluir archivos grandes
source.exclude_dirs = tests, bin

# Arquitectura
android.arch = armeabi-v7a

# Aceptar licencias
android.accept_sdk_license = True

# Configuración de buildozer
[buildozer]
log_level = 2
warn_on_root = 1