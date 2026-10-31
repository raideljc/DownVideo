[app]
title = DownTube
package.name = downtube
package.domain = org.raideljc
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf, txt
version = 0.10.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,yt-dlp,cryptography,requests,urllib3,charset-normalizer,idna,certifi,ffpyplayer
###source.exclude_dirs = bin, .buildozer, __pycache__, .git, ffmpg
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE
p4a.branch = develop
#requirements = python3,kivy,pyjnius
orientation = portrait
android.api = 33
android.minapi = 21
#android.ndk = 23e 
#android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
#android.permissions = INTERNET
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
