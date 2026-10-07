from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import yt_dlp
import threading
import re

class SanemiDownloaderApp(App):
    def build(self):
        self.title = "Sanemi Downloader Pro"
        
        # تصميم الواجهة بتنسيق عمودي ومرتب بطابع حاد
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        # عرض الصورة المتحركة (تأكد من وضع ملف الصورة باسم sanemi.gif أو الاحتفاظ باسمه)
        try:
            self.avatar = Image(
                source='sanemi.gif',
                anim_delay=0.04,
                size_hint_y=None,
                height=160
            )
            layout.add_widget(self.avatar)
        except Exception:
            pass
        
        # العنوان بطابع سانيمي
        layout.add_widget(Label(
            text="SANEMI ULTIMATE DOWNLOADER",
            font_size=16,
            color=(0.9, 0.2, 0.2, 1), # لون أحمر هجومي يناسب سانيمي
            size_hint_y=None,
            height=25,
            bold=True
        ))
        
        # حقل إدخال الرابط
        self.url_input = TextInput(
            hint_text="Paste video link here...",
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=(0.08, 0.08, 0.08, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.9, 0.2, 0.2, 1),
            padding_x=10
        )
        layout.add_widget(self.url_input)
        
        # قائمة اختيار الجودة (Resolution)
        layout.add_widget(Label(
            text="Select Quality:",
            font_size=13,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=20
        ))
        
        self.quality_spinner = Spinner(
            text='Best 4K / HD (Auto)',
            values=('Best 4K / HD (Auto)', '4K (2160p)', '2K (1440p)', '1080p (FHD)', '720p (HD)', 'Audio Only (MP3)'),
            size_hint_y=None,
            height=45,
            background_color=(0.7, 0.1, 0.1, 1)
        )
        layout.add_widget(self.quality_spinner)
        
        # زر التحميل الرئيسي
        self.download_btn = Button(
            text="EXECUTE DOWNLOAD",
            size_hint_y=None,
            height=45,
            background_color=(0.8, 0.15, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.download_btn.bind(on_press=self.verify_and_download)
        layout.add_widget(self.download_btn)
        
        # خانة الحالة
        self.status_label = Label(
            text="Status: Ready.",
            font_size=13,
            color=(0.2, 0.9, 0.4, 1),
            halign='center'
        )
        layout.add_widget(self.status_label)
        
        return layout

    def verify_and_download(self, instance):
        url = self.url_input.text.strip()
        selected_quality = self.quality_spinner.text
        
        url_pattern = re.compile(
            r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|tiktok\.com|instagram\.com|facebook\.com)/.+$'
        )
        
        if not url:
            self.status_label.text = "Error: Link field is empty!"
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
            
        if not url_pattern.match(url):
            self.status_label.text = "Error: Invalid link format!"
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        
        self.download_btn.disabled = True
        self.status_label.text = f"Preparing {selected_quality} download..."
        self.status_label.color = (0.9, 0.6, 0.2, 1)
        
        threading.Thread(target=self.execute_download, args=(url, selected_quality)).daemon = True
        threading.Thread(target=self.execute_download, args=(url, selected_quality)).start()

    def execute_download(self, url, quality):
        ydl_opts = {
            'outtmpl': '%(title)s [%(resolution)s].%(ext)s',
            'noplaylist': True,
        }
        
        if quality == '4K (2160p)':
            ydl_opts['format'] = 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'
        elif quality == '2K (1440p)':
            ydl_opts['format'] = 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'
        elif quality == '1080p (FHD)':
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p (HD)':
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == 'Audio Only (MP3)':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("Download Completed Successfully!", (0.2, 0.9, 0.4, 1))
        except Exception as e:
            self.update_status(f"Error: Make sure FFmpeg is active.", (1, 0.3, 0.3, 1))
        finally:
            self.download_btn.disabled = False

    def update_status(self, message, color):
        self.status_label.text = message
        self.status_label.color = color

if __name__ == '__main__':
    SanemiDownloaderApp().run()
