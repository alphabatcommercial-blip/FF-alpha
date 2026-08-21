import json
import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import DictProperty, ListProperty

kivy.require('2.0.0')

# ==========================================
# DATA STORAGE / DATABASE HANDLING
# ==========================================
DATA_FILE = "factory_data.json"

DEFAULT_DATA = {
    "items": ["Sofa", "Bed", "Almirah", "Chair", "Table", "Showcase"],
    "production": [],
    "orders": [],
    "expenses": [],
    "workers": []
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def show_popup(title, text):
    popup = Popup(title=title, content=Label(text=text), size_hint=(0.8, 0.3))
    popup.open()

# ==========================================
# KIVY UI LAYOUT (KV LANGUAGE)
# ==========================================
KV_DESIGN = '''
<MainLayout>:
    orientation: 'horizontal'
    
    # Sidebar Navigation
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.25
        padding: 10
        spacing: 5
        canvas.before:
            Color:
                rgba: 0.17, 0.24, 0.31, 1
            Rectangle:
                pos: self.pos
                size: self.size
                
        Label:
            text: "FS. Manager"
            font_size: '20sp'
            bold: True
            size_hint_y: None
            height: 50
            color: 0.18, 0.8, 0.44, 1

        Button:
            text: "ড্যাশবোর্ড"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('dashboard')
            
        Button:
            text: "প্রোডাকশন"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('production')

        Button:
            text: "অর্ডার/বিলিং"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('orders')

        Button:
            text: "খরচ"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('expenses')

        Button:
            text: "কর্মী ও বেতন"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('workers')

        Button:
            text: "আইটেমস"
            size_hint_y: None
            height: 40
            on_release: app.switch_screen('items')

        Widget: # Spacer

        Button:
            text: "ব্যাকআপ"
            size_hint_y: None
            height: 40
            background_color: 0.15, 0.68, 0.38, 1
            on_release: app.export_data()

    # Main Content Area
    ScreenManager:
        id: screen_manager
        
        Screen:
            name: 'dashboard'
            BoxLayout:
                orientation: 'vertical'
                padding: 15
                spacing: 10
                Label:
                    text: "স্মার্ট ড্যাশবোর্ড"
                    font_size: '22sp'
                    bold: True
                    size_hint_y: None
                    height: 40
                    color: 0.17, 0.24, 0.31, 1

                GridLayout:
                    cols: 2
                    spacing: 10
                    
                    Button:
                        text: "মোট কর্মী: " + str(app.dash_workers)
                        background_color: 0.08, 0.62, 0.52, 1
                    Button:
                        text: "ক্যাশ ইন হ্যান্ড: ৳" + str(app.dash_cash)
                        background_color: 0.15, 0.68, 0.38, 1
                    Button:
                        text: "ব্যাংক ব্যালেন্স: ৳" + str(app.dash_bank)
                        background_color: 0.16, 0.5, 0.72, 1
                    Button:
                        text: "মোট রেভিনিউ: ৳" + str(app.dash_revenue)
                        background_color: 0.55, 0.27, 0.67, 1
                    Button:
                        text: "মোট খরচ: ৳" + str(app.dash_expense)
                        background_color: 0.75, 0.22, 0.17, 1
                    Button:
                        text: "নিট লাভ/ক্ষতি: ৳" + str(app.dash_profit)
                        background_color: 0.82, 0.32, 0, 1

        Screen:
            name: 'items'
            BoxLayout:
                orientation: 'vertical'
                padding: 15
                spacing: 10
                Label:
                    text: "আইটেম সেটিংস"
                    font_size: '20sp'
                    size_hint_y: None
                    height: 40

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    spacing: 10
                    TextInput:
                        id: item_input
                        hint_text: "নতুন আইটেমের নাম"
                        multiline: False
                    Button:
                        text: "যোগ করুন"
                        size_hint_x: 0.3
                        on_release: app.add_item(item_input.text); item_input.text = ""

                ScrollView:
                    BoxLayout:
                        id: items_list
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
'''

# ==========================================
# MAIN KIVY APPLICATION CLASS
# ==========================================
class MainLayout(BoxLayout):
    pass

class FSManagerApp(App):
    db = DictProperty({})
    dash_workers = ListProperty([0])
    dash_cash = ListProperty([0])
    dash_bank = ListProperty([0])
    dash_revenue = ListProperty([0])
    dash_expense = ListProperty([0])
    dash_profit = ListProperty([0])

    def build(self):
        self.db = load_data()
        self.root_widget = Builder.load_string(KV_DESIGN)
        self.update_dashboard()
        self.render_items()
        return self.root_widget

    def switch_screen(self, screen_name):
        self.root_widget.ids.screen_manager.current = screen_name
        if screen_name == 'dashboard':
            self.update_dashboard()

    def update_dashboard(self):
        total_workers = len(self.db.get("workers", []))
        total_revenue = sum(float(o.get("paid", 0)) for o in self.db.get("orders", []))
        total_expenses = sum(float(e.get("amount", 0)) for e in self.db.get("expenses", []))

        cash_in = sum(float(o.get("paid", 0)) for o in self.db.get("orders", []) if o.get("method") == "Cash")
        cash_out = sum(float(e.get("amount", 0)) for e in self.db.get("expenses", []) if e.get("method") == "Cash")
        cash_in_hand = cash_in - cash_out

        bank_in = sum(float(o.get("paid", 0)) for o in self.db.get("orders", []) if o.get("method") == "Bank")
        bank_out = sum(float(e.get("amount", 0)) for e in self.db.get("expenses", []) if e.get("method") == "Bank")
        bank_balance = bank_in - bank_out

        net_profit = total_revenue - total_expenses

        self.dash_workers = total_workers
        self.dash_cash = cash_in_hand
        self.dash_bank = bank_balance
        self.dash_revenue = total_revenue
        self.dash_expense = total_expenses
        self.dash_profit = net_profit

    def render_items(self):
        container = self.root_widget.ids.screen_manager.get_screen('items').ids.items_list
        container.clear_widgets()

        for idx, item in enumerate(self.db.get("items", [])):
            box = BoxLayout(size_hint_y=None, height=40, spacing=10)
            box.add_widget(Label(text=item, color=(0,0,0,1)))
            
            btn_del = Button(text="মুছুন", size_hint_x=0.3, background_color=(0.9, 0.2, 0.2, 1))
            btn_del.bind(on_release=lambda instance, i=idx: self.delete_item(i))
            box.add_widget(btn_del)
            
            container.add_widget(box)

    def add_item(self, val):
        val = val.strip()
        if val and val not in self.db["items"]:
            self.db["items"].append(val)
            save_data(self.db)
            self.render_items()

    def delete_item(self, idx):
        if idx < len(self.db["items"]):
            del self.db["items"][idx]
            save_data(self.db)
            self.render_items()

    def export_data(self):
        save_data(self.db)
        show_popup("সফল", "ডাটা সফলভাবে ব্যাকআপ নেওয়া হয়েছে!")

if __name__ == "__main__":
    FSManagerApp().run()
