from kivymd.uix.textfield import MDTextField
import datetime
import win10toast
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivymd.app import MDApp
from kivymd.uix.button import *
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from s_helper import screen_helper
from kivymd.uix.picker import MDTimePicker

Window.size=(300,500)

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Content(BoxLayout):
    pass

class ReminderApp(MDApp):

    dialog = None

    def build(self):
        self.theme_cls.primary_palette="Amber"
        self.theme_cls.primary_hue ="400"
        screen=Builder.load_string(screen_helper)
        return screen

    def navigation_info(self):
        canbtn=MDFlatButton(text="Cancel",on_release=self.can_rem)
        self.dialog1=MDDialog(title='info',text='Part 1 of the whole REMNET project',size_hint=(0.7,1), buttons=[canbtn])
        self.dialog1.open()

    def can_rem(self,obj):
        self.dialog1.dismiss()

    def add_task(self):
        if not self.dialog:
            self.dialog = MDDialog(title="Add reminder", size_hint=(0.7,1),type="custom",content_cls=Content(),buttons=[MDFlatButton(text="Cancel", on_release= self.close_dialog),MDRaisedButton(text="Add", on_release=self.time_picker),],)
        self.dialog.set_normal_height()
        self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def time_picker(self,obj):
        from datetime import datetime
        previous_time = datetime.strptime("16:20:00", '%H:%M:%S').time()
        picker=MDTimePicker()
        picker.set_time(previous_time)
        picker.bind(time=self.got_time)
        picker.open()

    def got_time(self,picker_widget,the_time):
        self.dialog.dismiss()
        alarmhour=the_time.hour
        alarmmin=the_time.minute
        while True:
            if(alarmhour==datetime.datetime.now().hour and alarmmin==datetime.datetime.now().minute):
                for obj in self.dialog.content_cls.children:
                    if isinstance(obj, MDTextField):
                        toaster=win10toast.ToastNotifier()
                        toaster.show_toast(obj.text, duration=10)
                break

ReminderApp().run()
