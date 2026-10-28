[app]
title = DownVideo
package.name = downvideo
package.domain = org.downvideo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1.0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
orientation = portrait
fullscreen = 0

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b
android.gradle_dependencies = 

# ESTO ES LO IMPORTANTE - NO PUEDE ESTAR VACÍO
requirements = python3,kivy==2.2.1,urllib3

p4a_dir = ~/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a

[buildozer:buildozer]
log_level = 2
