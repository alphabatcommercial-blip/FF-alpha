[app]

# App Title and Package
title = My Kivy App
package.name = mykivyapp
package.domain = org.example

# Source directory and extensions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Application Version
version = 0.1

# Application requirements (add other modules if your app uses them)
requirements = python3,kivy

# Screen Orientation
orientation = portrait

# Fullscreen setting
fullscreen = 0

# Permissions
android.permissions = INTERNET

# Android API settings
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
