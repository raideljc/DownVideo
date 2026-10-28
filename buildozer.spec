[app]
title = Mi App
package.name = miapp
package.domain = org.miapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1.0

[buildozer]
log_level = 2
warn_on_root = 1
android_api = 33
android_minapi = 21
android_ndk = 25b

[app:android]
permissions = INTERNET
orientation = portrait
fullscreen = 0

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

requirements = python3,kivy==2.2.1

[buildozer:buildozer]
log_level = 2
