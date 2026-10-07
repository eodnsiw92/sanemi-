[app]

# اسم التطبيق الظاهري على الهاتف
title = Sanemi Downloader

# اسم الحزمة البرمجية
package.name = sanemidownloader

# نطاق الحزمة
package.domain = org.sanemi

# الملفات المدعومة (تأكد من تضمين صيغة الصور المتحركة gif وصورة سانيمي)
source.include_exts = py,png,jpg,kv,atlas,gif

# المتطلبات الأساسية للتشغيل والدمج
requirements = python3,kivy,yt-dlp,openssl,urllib3,certifi,idna,charset-normalizer,requests,ffmpeg

# الصلاحيات المطلوبة للتحزين والإنترنت
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
