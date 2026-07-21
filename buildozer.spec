[app]

# (str) Title of your application
title = Etiquetador

# (str) Package name
package.name = etiquetador

# (str) Package domain (needed for android packaging)
package.domain = org.etiquetador

# (str) Version of your application
version = 0.1

# (str) Source code where the application resides
source.dir = .

# (list) Source files to include (let it blank to include all files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) Application requirements
requirements = python310,kivy,fpdf

# (str) Custom source for python-for-android
p4a.branch = master

# (str) Supported python version
osx.python_version = 3
android.python_api = 31

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android sdk update accept (true/false)
android.accept_sdk_license = True
