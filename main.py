import json
import os
import shutil
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp


APP_NAME = "FS Manager"
DATA_FILE = "factory_data.json"

DEFAULT_DATA = {
    "items": [
        "Sofa",
        "Bed",
        "Almirah",
        "Chair",
        "Table",
        "Showcase"
    ],
    "production": [],
    "orders": [],
    "expenses": [],
    "workers": []
}


# =========================================================
# DATABASE
# =========================================================

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Save error:", e)


def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "items": DEFAULT_DATA["items"].copy(),
            "production": [],
            "orders": [],
            "expenses": [],
            "workers": []
        }
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key in DEFAULT_DATA:
            if key not in data:
                data[key] = []

        return data

    except Exception:
        data = {
            "items": DEFAULT_DATA["items"].copy(),
            "production": [],
            "orders": [],
            "expenses": [],
            "workers": []
        }
        save_data(data)
        return data


def money(value):
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return "0.00"


def show_popup(title, message):
    popup = Popup(
        title=title,
        content=Label(
            text=str(message),
            halign="center",
            valign="middle"
        ),
        size_hint=(0.85, 0.35)
    )
    popup.open()


# =========================================================
# KV UI
# =========================================================

KV = r'''
#:import dp kivy.metrics.dp

<MainLayout>:
    orientation: "horizontal"

    # ================= SIDEBAR =================

    BoxLayout:
        orientation: "vertical"
        size_hint_x: 0.25
        padding: dp(8)
        spacing: dp(5)

        canvas.before:
            Color:
                rgba: 0.10, 0.14, 0.18, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "FS Manager"
            font_size: "20sp"
            bold: True
            size_hint_y: None
            height: dp(55)
            color: 0.18, 0.80, 0.44, 1

        Button:
            text: "ড্যাশবোর্ড"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("dashboard")

        Button:
            text: "প্রোডাকশন"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("production")

        Button:
            text: "অর্ডার / বিলিং"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("orders")

        Button:
            text: "খরচ"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("expenses")

        Button:
            text: "কর্মী ও বেতন"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("workers")

        Button:
            text: "আইটেমস"
            size_hint_y: None
            height: dp(42)
            on_release: app.switch_screen("items")

        Widget:

        Button:
            text: "ব্যাকআপ"
            size_hint_y: None
            height: dp(45)
            background_color: 0.15, 0.68, 0.38, 1
            on_release: app.export_data()


    # ================= MAIN AREA =================

    ScreenManager:
        id: screen_manager

        # ================= DASHBOARD =================

        Screen:
            name: "dashboard"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(10)

                Label:
                    text: "স্মার্ট ড্যাশবোর্ড"
                    font_size: "23sp"
                    bold: True
                    size_hint_y: None
                    height: dp(45)
                    color: 0.10, 0.14, 0.18, 1

                GridLayout:
                    cols: 2
                    spacing: dp(10)

                    Button:
                        text: "মোট কর্মী\\n" + str(app.dash_workers)
                        background_color: 0.08, 0.62, 0.52, 1

                    Button:
                        text: "ক্যাশ\\n৳ " + app.dash_cash
                        background_color: 0.15, 0.68, 0.38, 1

                    Button:
                        text: "ব্যাংক\\n৳ " + app.dash_bank
                        background_color: 0.16, 0.50, 0.72, 1

                    Button:
                        text: "রেভিনিউ\\n৳ " + app.dash_revenue
                        background_color: 0.55, 0.27, 0.67, 1

                    Button:
                        text: "মোট খরচ\\n৳ " + app.dash_expense
                        background_color: 0.75, 0.22, 0.17, 1

                    Button:
                        text: "নিট লাভ/ক্ষতি\\n৳ " + app.dash_profit
                        background_color: 0.82, 0.32, 0.00, 1


        # ================= PRODUCTION =================

        Screen:
            name: "production"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "প্রোডাকশন"
                    font_size: "21sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(5)

                    Spinner:
                        id: production_item
                        text: "আইটেম নির্বাচন"
                        values: app.item_values

                    TextInput:
                        id: production_qty
                        hint_text: "পরিমাণ"
                        input_filter: "int"
                        multiline: False

                    TextInput:
                        id: production_cost
                        hint_text: "খরচ"
                        input_filter: "float"
                        multiline: False

                    Button:
                        text: "যোগ"
                        size_hint_x: 0.25
                        on_release: app.add_production(
                            production_item.text,
                            production_qty.text,
                            production_cost.text
                        )

                ScrollView:
                    BoxLayout:
                        id: production_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(5)


        # ================= ORDERS =================

        Screen:
            name: "orders"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "অর্ডার / বিলিং"
                    font_size: "21sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: customer_name
                    hint_text: "কাস্টমারের নাম"
                    multiline: False
                    size_hint_y: None
                    height: dp(42)

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(5)

                    Spinner:
                        id: order_item
                        text: "আইটেম"
                        values: app.item_values

                    TextInput:
                        id: order_qty
                        hint_text: "পরিমাণ"
                        input_filter: "int"
                        multiline: False

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(5)

                    TextInput:
                        id: order_total
                        hint_text: "মোট মূল্য"
                        input_filter: "float"
                        multiline: False

                    TextInput:
                        id: order_paid
                        hint_text: "জমা"
                        input_filter: "float"
                        multiline: False

                    Spinner:
                        id: order_method
                        text: "Cash"
                        values: ["Cash", "Bank"]

                    Button:
                        text: "অর্ডার যোগ"
                        size_hint_x: 0.30
                        on_release: app.add_order(
                            customer_name.text,
                            order_item.text,
                            order_qty.text,
                            order_total.text,
                            order_paid.text,
                            order_method.text
                        )

                ScrollView:
                    BoxLayout:
                        id: orders_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(5)


        # ================= EXPENSES =================

        Screen:
            name: "expenses"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "খরচ"
                    font_size: "21sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(5)

                    TextInput:
                        id: expense_title
                        hint_text: "খরচের নাম"
                        multiline: False

                    TextInput:
                        id: expense_amount
                        hint_text: "টাকার পরিমাণ"
                        input_filter: "float"
                        multiline: False

                    Spinner:
                        id: expense_method
                        text: "Cash"
                        values: ["Cash", "Bank"]

                    Button:
                        text: "যোগ"
                        size_hint_x: 0.25
                        on_release: app.add_expense(
                            expense_title.text,
                            expense_amount.text,
                            expense_method.text
                        )

                ScrollView:
                    BoxLayout:
                        id: expenses_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(5)


        # ================= WORKERS =================

        Screen:
            name: "workers"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "কর্মী ও বেতন"
                    font_size: "21sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(5)

                    TextInput:
                        id: worker_name
                        hint_text: "কর্মীর নাম"
                        multiline: False

                    TextInput:
                        id: worker_salary
                        hint_text: "বেতন"
                        input_filter: "float"
                        multiline: False

                    TextInput:
                        id: worker_paid
                        hint_text: "পরিশোধ"
                        input_filter: "float"
                        multiline: False

                    Button:
                        text: "যোগ"
                        size_hint_x: 0.25
                        on_release: app.add_worker(
                            worker_name.text,
                            worker_salary.text,
                            worker_paid.text
                        )

                ScrollView:
                    BoxLayout:
                        id: workers_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(5)


        # ================= ITEMS =================

        Screen:
            name: "items"

            BoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "আইটেম সেটিংস"
                    font_size: "21sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(8)

                    TextInput:
                        id: item_input
                        hint_text: "নতুন আইটেমের নাম"
                        multiline: False

                    Button:
                        text: "যোগ করুন"
                        size_hint_x: 0.30
                        on_release: app.add_item(item_input.text)

                ScrollView:
                    BoxLayout:
                        id: items_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(5)
'''


class MainLayout(BoxLayout):
    pass


class FSManagerApp(App):

    dash_workers = NumericProperty(0)

    dash_cash = StringProperty("0.00")
    dash_bank = StringProperty("0.00")
    dash_revenue = StringProperty("0.00")
    dash_expense = StringProperty("0.00")
    dash_profit = StringProperty("0.00")

    item_values = ListProperty([])

    def build(self):
        self.title = APP_NAME

        self.db = load_data()

        self.root_widget = Builder.load_string(KV)

        self.update_item_values()
        self.update_dashboard()
        self.render_all()

        return self.root_widget

    # =====================================================
    # SCREEN
    # =====================================================

    def switch_screen(self, screen_name):
        self.root_widget.ids.screen_manager.current = screen_name
        self.update_dashboard()
        self.render_all()

    # =====================================================
    # DASHBOARD
    # =====================================================

    def update_dashboard(self):

        workers = self.db.get("workers", [])
        orders = self.db.get("orders", [])
        expenses = self.db.get("expenses", [])

        self.dash_workers = len(workers)

        revenue = sum(
            float(o.get("paid", 0))
            for o in orders
        )

        expense = sum(
            float(e.get("amount", 0))
            for e in expenses
        )

        cash_in = sum(
            float(o.get("paid", 0))
            for o in orders
            if o.get("method") == "Cash"
        )

        cash_out = sum(
            float(e.get("amount", 0))
            for e in expenses
            if e.get("method") == "Cash"
        )

        bank_in = sum(
            float(o.get("paid", 0))
            for o in orders
            if o.get("method") == "Bank"
        )

        bank_out = sum(
            float(e.get("amount", 0))
            for e in expenses
            if e.get("method") == "Bank"
        )

        self.dash_cash = money(cash_in - cash_out)
        self.dash_bank = money(bank_in - bank_out)
        self.dash_revenue = money(revenue)
        self.dash_expense = money(expense)
        self.dash_profit = money(revenue - expense)

    # =====================================================
    # ITEMS
    # =====================================================

    def update_item_values(self):
        self.item_values = self.db.get("items", []).copy()

    def add_item(self, value):

        value = value.strip()

        if not value:
            show_popup("সতর্কতা", "আইটেমের নাম লিখুন।")
            return

        if value in self.db["items"]:
            show_popup("সতর্কতা", "এই আইটেম আগে থেকেই আছে।")
            return

        self.db["items"].append(value)

        save_data(self.db)

        self.update_item_values()
        self.render_items()

        self.root_widget.ids.item_input.text = ""

    def delete_item(self, index):

        items = self.db.get("items", [])

        if 0 <= index < len(items):

            name = items[index]

            del items[index]

            save_data(self.db)

            self.update_item_values()
            self.render_items()

            show_popup(
                "সফল",
                f"{name} মুছে ফেলা হয়েছে।"
            )

    def render_items(self):

        container = (
            self.root_widget
            .ids.screen_manager
            .get_screen("items")
            .ids.items_list
        )

        container.clear_widgets()

        for index, item in enumerate(
            self.db.get("items", [])
        ):

            row = BoxLayout(
                size_hint_y=None,
                height=dp(40),
                spacing=dp(5)
            )

            row.add_widget(
                Label(
                    text=item,
                    color=(0, 0, 0, 1)
                )
            )

            button = Button(
                text="মুছুন",
                size_hint_x=0.25,
                background_color=(0.9, 0.2, 0.2, 1)
            )

            button.bind(
                on_release=lambda instance,
                i=index: self.delete_item(i)
            )

            row.add_widget(button)

            container.add_widget(row)

    # =====================================================
    # PRODUCTION
    # =====================================================

    def add_production(self, item, quantity, cost):

        if item == "আইটেম নির্বাচন":
            show_popup("সতর্কতা", "আইটেম নির্বাচন করুন।")
            return

        if not quantity or not cost:
            show_popup("সতর্কতা", "পরিমাণ ও খরচ দিন।")
            return

        try:
            quantity_value = int(quantity)
            cost_value = float(cost)
        except ValueError:
            show_popup("সতর্কতা", "সঠিক সংখ্যা দিন।")
            return

        if quantity_value <= 0 or cost_value < 0:
            show_popup("সতর্কতা", "সঠিক পরিমাণ দিন।")
            return

        record = {
            "item": item,
            "quantity": quantity_value,
            "cost": cost_value,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.db["production"].append(record)

        save_data(self.db)
        self.render_production()

        self.root_widget.ids.production_qty.text = ""
        self.root_widget.ids.production_cost.text = ""

        show_popup("সফল", "প্রোডাকশন যোগ হয়েছে।")

    def render_production(self):

        container = (
            self.root_widget
            .ids.screen_manager
            .get_screen("production")
            .ids.production_list
        )

        container.clear_widgets()

        for index, record in enumerate(
            self.db.get("production", [])
        ):

            text = (
                f"{record.get('item', '')} | "
                f"Qty: {record.get('quantity', 0)} | "
                f"Cost: ৳{money(record.get('cost', 0))}\n"
                f"{record.get('date', '')}"
            )

            row = BoxLayout(
                size_hint_y=None,
                height=dp(55),
                spacing=dp(5)
            )

            row.add_widget(
                Label(
                    text=text,
                    color=(0, 0, 0, 1)
                )
            )

            button = Button(
                text="মুছুন",
                size_hint_x=0.22,
                background_color=(0.9, 0.2, 0.2, 1)
            )

            button.bind(
                on_release=lambda instance,
                i=index: self.delete_production(i)
            )

            row.add_widget(button)
            container.add_widget(row)

    def delete_production(self, index):

        if 0 <= index < len(self.db.get("production", [])):

            del self.db["production"][index]

            save_data(self.db)
            self.render_production()

    # =====================================================
    # ORDERS
    # =====================================================

    def add_order(
        self,
        customer,
        item,
        quantity,
        total,
        paid,
        method
    ):

        customer = customer.strip()

        if not customer:
            show_popup("সতর্কতা", "কাস্টমারের নাম দিন।")
            return

        if item == "আইটেম":
            show_popup("সতর্কতা", "আইটেম নির্বাচন করুন।")
            return

        if not quantity or not total or not paid:
            show_popup("সতর্কতা", "সব তথ্য পূরণ করুন।")
            return

        try:
            quantity_value = int(quantity)
            total_value = float(total)
            paid_value = float(paid)
        except ValueError:
            show_popup("সতর্কতা", "সঠিক সংখ্যা দিন।")
            return

        if quantity_value <= 0:
            show_popup("সতর্কতা", "পরিমাণ 0 হতে পারবে না।")
            return

        if total_value < 0 or paid_value < 0:
            show_popup("সতর্কতা", "টাকার পরিমাণ সঠিক দিন।")
            return

        if paid_value > total_value:
            show_popup(
                "সতর্কতা",
                "জমার টাকা মোট মূল্যের চেয়ে বেশি হতে পারবে না।"
            )
            return

        record = {
            "customer": customer,
            "item": item,
            "quantity": quantity_value,
            "total": total_value,
            "paid": paid_value,
            "due": total_value - paid_value,
            "method": method,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.db["orders"].append(record)

        save_data(self.db)

        self.render_orders()
        self.clear_order_inputs()
        self.update_dashboard()

        show_popup("সফল", "অর্ডার যোগ হয়েছে।")

    def clear_order_inputs(self):

        ids = self.root_widget.ids

        ids.customer_name.text = ""
        ids.order_qty.text = ""
        ids.order_total.text = ""
        ids.order_paid.text = ""

    def render_orders(self):

        container = (
            self.root_widget
            .ids.screen_manager
            .get_screen("orders")
            .ids.orders_list
        )

        container.clear_widgets()

        for index, order in enumerate(
            self.db.get("orders", [])
        ):

            text = (
                f"Customer: {order.get('customer', '')}\n"
                f"{order.get('item', '')} x "
                f"{order.get('quantity', 0)} | "
                f"Total: ৳{money(order.get('total', 0))} | "
                f"Paid: ৳{money(order.get('paid', 0))} | "
                f"Due: ৳{money(order.get('due', 0))}\n"
                f"{order.get('method', '')} | "
                f"{order.get('date', '')}"
            )

            row = BoxLayout(
                size_hint_y=None,
                height=dp(75),
                spacing=dp(5)
            )

            row.add_widget(
                Label(
                    text=text,
                    color=(0, 0, 0, 1)
                )
            )

            button = Button(
                text="মুছুন",
                size_hint_x=0.20,
                background_color=(0.9, 0.2, 0.2, 1)
            )

            button.bind(
                on_release=lambda instance,
                i=index: self.delete_order(i)
            )

            row.add_widget(button)
            container.add_widget(row)

    def delete_order(self, index):

        if 0 <= index < len(self.db.get("orders", [])):

            del self.db["orders"][index]

            save_data(self.db)
            self.render_orders()
            self.update_dashboard()

    # =====================================================
    # EXPENSES
    # =====================================================

    def add_expense(self, title, amount, method):

        title = title.strip()

        if not title or not amount:
            show_popup(
                "সতর্কতা",
                "খরচের নাম ও টাকা দিন।"
            )
            return

        try:
            amount_value = float(amount)
        except ValueError:
            show_popup("সতর্কতা", "সঠিক টাকা দিন।")
            return

        if amount_value < 0:
            show_popup("সতর্কতা", "টাকা সঠিক দিন।")
            return

        record = {
            "title": title,
            "amount": amount_value,
            "method": method,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.db["expenses"].append(record)

        save_data(self.db)

        self.render_expenses()

        self.root_widget.ids.expense_title.text = ""
        self.root_widget.ids.expense_amount.text = ""

        self.update_dashboard()

        show_popup("সফল", "খরচ যোগ হয়েছে।")

    def render_expenses(self):

        container = (
            self.root_widget
            .ids.screen_manager
            .get_screen("expenses")
            .ids.expenses_list
        )

        container.clear_widgets()

        for index, expense in enumerate(
            self.db.get("expenses", [])
        ):

            text = (
                f"{expense.get('title', '')} | "
                f"৳{money(expense.get('amount', 0))}\n"
                f"{expense.get('method', '')} | "
                f"{expense.get('date', '')}"
            )

            row = BoxLayout(
                size_hint_y=None,
                height=dp(55),
                spacing=dp(5)
            )

            row.add_widget(
                Label(
                    text=text,
                    color=(0, 0, 0, 1)
                )
            )

            button = Button(
                text="মুছুন",
                size_hint_x=0.22,
                background_color=(0.9, 0.2, 0.2, 1)
            )

            button.bind(
                on_release=lambda instance,
                i=index: self.delete_expense(i)
            )

            row.add_widget(button)
            container.add_widget(row)

    def delete_expense(self, index):

        if 0 <= index < len(self.db.get("expenses", [])):

            del self.db["expenses"][index]

            save_data(self.db)
            self.render_expenses()
            self.update_dashboard()

    # =====================================================
    # WORKERS
    # =====================================================

    def add_worker(self, name, salary, paid):

        name = name.strip()

        if not name or not salary or not paid:
            show_popup(
                "সতর্কতা",
                "কর্মীর নাম, বেতন ও পরিশোধের টাকা দিন।"
            )
            return

        try:
            salary_value = float(salary)
            paid_value = float(paid)
        except ValueError:
            show_popup("সতর্কতা", "সঠিক টাকা দিন।")
            return

        if salary_value < 0 or paid_value < 0:
            show_popup("সতর্কতা", "টাকা সঠিক দিন।")
            return

        if paid_value > salary_value:
            show_popup(
                "সতর্কতা",
                "পরিশোধ বেতনের চেয়ে বেশি হতে পারবে না।"
            )
            return

        record = {
            "name": name,
            "salary": salary_value,
            "paid": paid_value,
            "due": salary_value - paid_value,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.db["workers"].append(record)

        save_data(self.db)

        self.render_workers()

        self.root_widget.ids.worker_name.text = ""
        self.root_widget.ids.worker_salary.text = ""
        self.root_widget.ids.worker_paid.text = ""

        self.update_dashboard()

        show_popup("সফল", "কর্মী যোগ হয়েছে।")

    def render_workers(self):

        container = (
            self.root_widget
            .ids.screen_manager
            .get_screen("workers")
            .ids.workers_list
        )

        container.clear_widgets()

        for index, worker in enumerate(
            self.db.get("workers", [])
        ):

            text = (
                f"{worker.get('name', '')}\n"
                f"Salary: ৳{money(worker.get('salary', 0))} | "
                f"Paid: ৳{money(worker.get('paid', 0))} | "
                f"Due: ৳{money(worker.get('due', 0))}"
            )

            row = BoxLayout(
                size_hint_y=None,
                height=dp(60),
                spacing=dp(5)
            )

            row.add_widget(
                Label(
                    text=text,
                    color=(0, 0, 0, 1)
                )
            )

            button = Button(
                text="মুছুন",
                size_hint_x=0.22,
                background_color=(0.9, 0.2, 0.2, 1)
            )

            button.bind(
                on_release=lambda instance,
                i=index: self.delete_worker(i)
            )

            row.add_widget(button)
            container.add_widget(row)

    def delete_worker(self, index):

        if 0 <= index < len(self.db.get("workers", [])):

            del self.db["workers"][index]

            save_data(self.db)
            self.render_workers()
            self.update_dashboard()

    # =====================================================
    # RENDER ALL
    # =====================================================

    def render_all(self):

        self.render_items()
        self.render_production()
        self.render_orders()
        self.render_expenses()
        self.render_workers()

    # =====================================================
    # BACKUP
    # =====================================================

    def export_data(self):

        try:

            save_data(self.db)

            backup_name = (
                "factory_backup_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".json"
            )

            shutil.copyfile(
                DATA_FILE,
                backup_name
            )

            show_popup(
                "সফল",
                "Backup তৈরি হয়েছে:\n" + backup_name
            )

        except Exception as e:

            show_popup(
                "Backup Error",
                str(e)
            )


if __name__ == "__main__":
    FSManagerApp().run()
