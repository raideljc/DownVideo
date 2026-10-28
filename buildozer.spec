[app]
title = DownVideo
package.name = downvideo
package.domain = org.downvideo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1.0

# ========== BUILDOZER ==========
[buildozer]
log_level = 2
warn_on_root = 1

# ========== ANDROID ==========
[app:android]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
orientation = portrait
fullscreen = 0

# API Levels
android.minapi = 21
android.targetapi = 33
android.ndk_api = 24

# Architectures
android.archs = arm64-v8a,armeabi-v7a

# Aceptar licencias
android.accept_sdk_license = True

# NDK version
android.ndk = 25b

# IMPORTANTE: Requirements no puede estar vacío
requirements = python3,kivy==2.2.1,urllib3

# Build tools version
android.gradle_dependencies = 

# Toolchain version
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

[buildozer:buildozer]
log_level = 2
