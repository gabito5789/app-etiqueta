[app]

# (str) Title of your application
title = Etiquetador

# (str) Package name
package.name = etiquetador

# (str) Package domain (needed for android packaging)
package.domain = org.etiquetador

# (list) Source files to include (let it blank to include all files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) Application requirements
# ¡Ojo aquí! Usamos fpdf y quitamos openpyxl para evitar errores en Android
requirements = python3, kivy, fpdf

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (str) Android arch to build for
android.archs = arm64-v8a, armeabi-v7a