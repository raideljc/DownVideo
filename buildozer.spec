[app]
title = MiAppBasica
package.name = miappbasica
package.domain = org.ejemplo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# Dependencias necesarias para una app Kivy estándar
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Permisos (opcional, para una app básica suele estar vacío o solo INTERNET)
android.permissions = INTERNET

# Configuración de Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
