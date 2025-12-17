from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import os
import sqlite3
from datetime import datetime
import json

# Configuración básica para desarrollo
Window.size = (400, 700)

# Base de datos
class Database:
    def __init__(self):
        self.db_path = self.get_db_path()
        self.init_database()
    
    def get_db_path(self):
        """Obtiene la ruta correcta para la base de datos según la plataforma"""
        from kivy.utils import platform
        
        if platform == 'android':
            from android.storage import app_storage_path
            app_path = app_storage_path()
            if not os.path.exists(app_path):
                os.makedirs(app_path)
            return os.path.join(app_path, 'dercor8.db')
        else:
            # Para escritorio
            if not os.path.exists('data'):
                os.makedirs('data')
            return os.path.join('data', 'dercor8.db')
    
    def init_database(self):
        """Inicializa la base de datos con tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio REAL,
                imagen TEXT,
                descripcion TEXT,
                stock INTEGER DEFAULT 1
            )
        ''')
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                fecha_registro TEXT
            )
        ''')
        
        # Tabla de proyectos guardados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nombre TEXT,
                tipo TEXT,
                datos TEXT,
                fecha TEXT
            )
        ''')
        
        # Insertar datos de ejemplo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            self.insert_sample_data(cursor)
        
        # Insertar usuario por defecto
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO usuarios (username, fecha_registro) VALUES (?, ?)",
                ("Usuario", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        """Inserta datos de ejemplo en la base de datos"""
        productos = [
            ("Sofá Moderno", "Sofá", 4500.00, "assets/sofa.png", 
             "Sofá contemporáneo con diseño ergonómico. Material: Cuero sintético. Dimensiones: 200x90x80cm", 10),
            ("Mesa de Centro", "Mesa", 3200.00, "assets/mesa.png",
             "Mesa de centro con diseño minimalista. Material: Madera de roble. Dimensiones: 120x60x45cm", 8),
            ("Lámpara de Pie", "Lámpara", 1200.00, "assets/lampara.png",
             "Lámpara de pie con estilo moderno. Material: Metal y tela. Altura: 160cm", 15),
            ("Silla de Oficina", "Silla", 2500.00, "assets/silla.png",
             "Silla ergonómica para oficina. Material: Malla transpirable", 12),
            ("Estantería", "Estantería", 4200.00, "assets/estanteria.png",
             "Estantería modular de diseño moderno. Material: MDF y metal", 5),
            ("Cama King Size", "Cama", 6800.00, "assets/cama.png",
             "Cama king size con cabecero tapizado. Material: Madera y tela", 6)
        ]
        
        for producto in productos:
            cursor.execute(
                "INSERT INTO productos (nombre, categoria, precio, imagen, descripcion, stock) VALUES (?, ?, ?, ?, ?, ?)",
                producto
            )
    
    def get_productos(self):
        """Obtiene todos los productos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    def get_usuario(self, username="Usuario"):
        """Obtiene un usuario por nombre"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    def update_usuario(self, old_username, new_username):
        """Actualiza el nombre de usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET username = ? WHERE username = ?", 
                      (new_username, old_username))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def guardar_propuesta(self, user_id, estilo, contenido):
        """Guarda una propuesta de diseño"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO proyectos (user_id, nombre, tipo, datos, fecha) VALUES (?, ?, ?, ?, ?)",
            (user_id, f"Propuesta {estilo}", "propuesta", contenido, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    
    def guardar_proyecto_ar(self, user_id, nombre, datos):
        """Guarda un proyecto AR"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO proyectos (user_id, nombre, tipo, datos, fecha) VALUES (?, ?, ?, ?, ?)",
            (user_id, nombre, "ar", datos, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    
    def get_proyectos_usuario(self, user_id, tipo=None):
        """Obtiene los proyectos de un usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if tipo:
            cursor.execute(
                "SELECT * FROM proyectos WHERE user_id = ? AND tipo = ? ORDER BY fecha DESC",
                (user_id, tipo)
            )
        else:
            cursor.execute(
                "SELECT * FROM proyectos WHERE user_id = ? ORDER BY fecha DESC",
                (user_id,)
            )
        proyectos = cursor.fetchall()
        conn.close()
        return proyectos
    
    def eliminar_proyecto(self, proyecto_id):
        """Elimina un proyecto"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proyectos WHERE id = ?", (proyecto_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

# Definición de las pantallas
KV = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<NavButton@Button>:
    size_hint_y: None
    height: 40
    background_normal: ''
    background_color: 0.2, 0.6, 0.8, 1
    color: 1,1,1,1
    font_size: 16
    border: (0,0,0,0)
    bold: True
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]

<Header@Label>:
    font_size: 30
    bold: True
    size_hint_y: None
    height: 50
    color: 1,1,1,1
    halign: 'center'

<HomeScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.1, 0.15, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Header:
            text: "DercoR8"
        
        Label:
            text: "Diseña tu espacio soñado"
            color: 1,1,1,1
            font_size: 20
            size_hint_y: None
            height: 40
            halign: 'center'
        
        Image:
            source: "assets/logo.png" if os.path.exists("assets/logo.png") else ""
            size_hint_y: 0.4
            allow_stretch: True
            keep_ratio: True
        
        NavButton:
            text: "Catálogo de Muebles"
            on_release:
                app.root.transition = SlideTransition(direction="left")
                app.root.current = "catalog"
        
        NavButton:
            text: "Asistente de Diseño"
            on_release:
                app.root.transition = SlideTransition(direction="left")
                app.root.current = "assistant"
        
        NavButton:
            text: "Realidad Aumentada"
            on_release:
                app.root.transition = FadeTransition()
                app.root.current = "ar_view"
        
        NavButton:
            text: "Mi Perfil"
            background_color: 0.3, 0.7, 0.5, 1
            on_release:
                app.root.transition = FadeTransition()
                app.root.current = "profile"

<CatalogScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        canvas.before:
            Color:
                rgba: 0.1, 0.15, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: 70
            NavButton:
                text: "← Volver"
                width: 100
                size_hint_x: None
                on_release:
                    app.root.transition = SlideTransition(direction="right")
                    app.root.current = "home"
            Header:
                text: "Catálogo"
        
        ScrollView:
            GridLayout:
                id: products_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 15

<AssistantScreen>:
    proposal_text: ""
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 10
        canvas.before:
            Color:
                rgba: 0.1, 0.15, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: 70
            NavButton:
                text: "← Volver"
                width: 100
                size_hint_x: None
                on_release:
                    app.root.transition = SlideTransition(direction="right")
                    app.root.current = "home"
            Header:
                text: "Asistente"
        
        Label:
            text: "Selecciona un estilo de diseño:"
            color: 1,1,1,1
            font_size: 16
            size_hint_y: None
            height: 40
            halign: 'center'
        
        GridLayout:
            cols: 2
            spacing: 10
            size_hint_y: None
            height: 180
            NavButton:
                text: "Moderno"
                on_release: root.generate_proposal("Moderno")
            NavButton:
                text: "Clásico"
                on_release: root.generate_proposal("Clásico")
            NavButton:
                text: "Industrial"
                on_release: root.generate_proposal("Industrial")
            NavButton:
                text: "Minimalista"
                on_release: root.generate_proposal("Minimalista")
        
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            NavButton:
                text: "Guardar Propuesta"
                background_color: 0.3, 0.7, 0.5, 1
                on_release: root.save_proposal()
            NavButton:
                text: "Ver Historial"
                background_color: 0.5, 0.3, 0.7, 1
                on_release: root.view_history()
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                Label:
                    id: proposal_label
                    text: root.proposal_text
                    color: 1,1,1,1
                    font_size: 16
                    text_size: self.width, None
                    halign: "left"
                    valign: "top"
                    size_hint_y: None
                    height: self.texture_size[1] + 20

<ARScreen>:
    current_scene: []
    BoxLayout:
        orientation: "vertical"
        spacing: 10
        padding: 10
        canvas.before:
            Color:
                rgba: 0.08, 0.1, 0.15, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: 70
            NavButton:
                text: "← Volver"
                width: 100
                size_hint_x: None
                on_release:
                    app.root.transition = FadeTransition()
                    app.root.current = "home"
            Header:
                text: "Realidad Aumentada"
        
        FloatLayout:
            id: ar_area
            size_hint_y: 0.7
            canvas.before:
                Color:
                    rgba: 0.15, 0.15, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Label:
                text: "Área de Realidad Aumentada\\nAgrega muebles con los botones"
                color: 0.7,0.7,0.7,1
                font_size: 18
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            NavButton:
                text: "Guardar Escena"
                background_color: 0.3, 0.7, 0.5, 1
                on_release: root.save_scene()
            NavButton:
                text: "Cargar Escena"
                background_color: 0.5, 0.3, 0.7, 1
                on_release: root.load_scenes()
        
        BoxLayout:
            size_hint_y: None
            height: 80
            spacing: 10
            NavButton:
                text: "Sofá"
                on_release: root.add_furniture("sofa")
            NavButton:
                text: "Mesa"
                on_release: root.add_furniture("mesa")
            NavButton:
                text: "Lámpara"
                on_release: root.add_furniture("lampara")
            NavButton:
                text: "Limpiar"
                background_color: 0.8, 0.2, 0.2, 1
                on_release: root.clear_scene()

<ProfileScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.1, 0.15, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: 70
            NavButton:
                text: "← Volver"
                width: 100
                size_hint_x: None
                on_release:
                    app.root.transition = SlideTransition(direction="right")
                    app.root.current = "home"
            Header:
                text: "Mi Perfil"
        
        Label:
            text: "Nombre de Usuario:"
            color: 1,1,1,1
            font_size: 16
            size_hint_y: None
            height: 30
            halign: 'left'
        
        TextInput:
            id: username_input
            text: app.username
            multiline: False
            size_hint_y: None
            height: 50
            background_color: 0.2,0.2,0.2,1
            foreground_color: 1,1,1,1
            padding: [10, 10]
        
        Label:
            text: "Mis Proyectos:"
            color: 1,1,1,1
            font_size: 16
            size_hint_y: None
            height: 40
            halign: 'left'
            bold: True
        
        ScrollView:
            GridLayout:
                id: projects_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
        
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            NavButton:
                text: "Guardar Cambios"
                background_color: 0.3, 0.7, 0.5, 1
                on_release: root.save_profile()
            NavButton:
                text: "Eliminar Proyectos"
                background_color: 0.8, 0.3, 0.3, 1
                on_release: root.delete_projects()

ScreenManager:
    id: screen_manager
    HomeScreen:
        name: "home"
    CatalogScreen:
        name: "catalog"
    AssistantScreen:
        name: "assistant"
    ARScreen:
        name: "ar_view"
    ProfileScreen:
        name: "profile"
'''

# Clases de pantallas
class HomeScreen(Screen):
    pass

class CatalogScreen(Screen):
    def on_enter(self):
        self.load_products()
    
    def load_products(self):
        app = App.get_running_app()
        productos = app.db.get_productos()
        
        grid = self.ids.products_grid
        grid.clear_widgets()
        
        for producto in productos:
            prod_id, nombre, categoria, precio, imagen, descripcion, stock = producto
            
            # Crear un card para cada producto
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=200,
                spacing=5,
                padding=10
            )
            
            # Fondo del card
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(0.2, 0.25, 0.3, 1)
                RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            
            # Información del producto
            card.add_widget(Label(
                text=nombre,
                color=(1,1,1,1),
                font_size=18,
                bold=True,
                size_hint_y=None,
                height=30
            ))
            
            card.add_widget(Label(
                text=f"Precio: ${precio:,.2f}",
                color=(0.9,0.9,0.2,1),
                font_size=16,
                size_hint_y=None,
                height=25
            ))
            
            card.add_widget(Label(
                text=f"Stock: {stock} unidades",
                color=(0.7,0.7,0.7,1) if stock > 0 else (1,0.3,0.3,1),
                font_size=14,
                size_hint_y=None,
                height=20
            ))
            
            card.add_widget(Label(
                text=descripcion[:50] + "..." if len(descripcion) > 50 else descripcion,
                color=(0.8,0.8,0.8,1),
                font_size=12,
                size_hint_y=None,
                height=40
            ))
            
            grid.add_widget(card)

class AssistantScreen(Screen):
    proposal_text = StringProperty("")
    current_style = ""
    
    def generate_proposal(self, style):
        self.current_style = style
        
        proposals = {
            "Moderno": """• Colores: Blanco, gris, negro
• Materiales: Vidrio, acero, cuero
• Iluminación: LED, focos direccionales
• Muebles: Líneas limpias, minimalistas
• Recomendación: Sofá modular, mesa de vidrio""",
            
            "Clásico": """• Colores: Beige, marrón, dorado
• Materiales: Madera tallada, terciopelo
• Iluminación: Lámparas de araña, candelabros
• Muebles: Con detalles ornamentales
• Recomendación: Sofá Chester, mesas con patas torneadas""",
            
            "Industrial": """• Colores: Gris, negro, marrón
• Materiales: Metal, ladrillo, cemento
• Iluminación: Focos colgantes, luces de tubería
• Muebles: Rústicos, con estructura visible
• Recomendación: Mesa de centro de metal, estanterías de tubos""",
            
            "Minimalista": """• Colores: Blanco, beige, gris claro
• Materiales: Madera clara, vidrio, acero
• Iluminación: Empotrada, luz natural
• Muebles: Funcionales, sin adornos
• Recomendación: Muebles modulares, almacenamiento oculto"""
        }
        
        self.proposal_text = f"Propuesta para estilo {style}:\n\n{proposals.get(style, 'Estilo no disponible')}"
    
    def save_proposal(self):
        if not self.current_style:
            return
        
        app = App.get_running_app()
        usuario = app.db.get_usuario(app.username)
        
        if usuario:
            user_id = usuario[0]
            app.db.guardar_propuesta(user_id, self.current_style, self.proposal_text)
            
            popup = Popup(
                title="Propuesta Guardada",
                content=Label(text="La propuesta se ha guardado en tus proyectos"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
    
    def view_history(self):
        app = App.get_running_app()
        usuario = app.db.get_usuario(app.username)
        
        if usuario:
            user_id = usuario[0]
            proyectos = app.db.get_proyectos_usuario(user_id, "propuesta")
            
            if proyectos:
                content = BoxLayout(orientation='vertical', spacing=10, padding=10)
                scroll = ScrollView(size_hint=(1, 0.9))
                grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
                grid.bind(minimum_height=grid.setter('height'))
                
                for proyecto in proyectos[:5]:  # Últimas 5 propuestas
                    proj_id, user_id, nombre, tipo, datos, fecha = proyecto
                    
                    prop_box = BoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        height=100,
                        spacing=5
                    )
                    
                    prop_box.add_widget(Label(
                        text=f"{nombre} - {fecha[:10]}",
                        color=(1,1,1,1),
                        font_size=16,
                        bold=True,
                        size_hint_y=None,
                        height=30
                    ))
                    
                    prop_box.add_widget(Label(
                        text=datos[:80] + "..." if len(datos) > 80 else datos,
                        color=(0.8,0.8,0.8,1),
                        font_size=12,
                        size_hint_y=None,
                        height=60
                    ))
                    
                    grid.add_widget(prop_box)
                
                scroll.add_widget(grid)
                content.add_widget(scroll)
                
                popup = Popup(
                    title="Historial de Propuestas",
                    content=content,
                    size_hint=(0.9, 0.8)
                )
                popup.open()
            else:
                popup = Popup(
                    title="Sin Historial",
                    content=Label(text="No hay propuestas guardadas"),
                    size_hint=(0.6, 0.4)
                )
                popup.open()

class ARScreen(Screen):
    current_scene = []
    
    def add_furniture(self, furniture_type):
        mapping = {
            "sofa": ("assets/sofa.png", (200, 150)),
            "mesa": ("assets/mesa.png", (150, 150)),
            "lampara": ("assets/lampara.png", (100, 150))
        }
        
        if furniture_type not in mapping:
            return
        
        path, size = mapping[furniture_type]
        
        if not os.path.exists(path):
            path = "assets/default.png"
            if not os.path.exists(path):
                return
        
        area = self.ids.ar_area
        
        scatter = Scatter(
            size_hint=(None, None), 
            size=size,
            do_rotation=True,
            do_scale=True,
            do_translation=True,
            auto_bring_to_front=True
        )
        
        img = Image(
            source=path,
            size=scatter.size,
            allow_stretch=True,
            keep_ratio=True
        )
        
        scatter.add_widget(img)
        scatter.center = area.center
        area.add_widget(scatter)
        
        # Guardar en la escena actual
        self.current_scene.append({
            "type": furniture_type,
            "position": (scatter.center_x, scatter.center_y),
            "rotation": scatter.rotation,
            "scale": scatter.scale
        })
    
    def clear_scene(self):
        area = self.ids.ar_area
        for child in area.children[:]:
            if isinstance(child, Scatter):
                area.remove_widget(child)
        self.current_scene = []
    
    def save_scene(self):
        if not self.current_scene:
            return
        
        app = App.get_running_app()
        usuario = app.db.get_usuario(app.username)
        
        if usuario:
            user_id = usuario[0]
            
            scene_data = json.dumps(self.current_scene)
            nombre = f"Escena AR {datetime.now().strftime('%d/%m %H:%M')}"
            
            app.db.guardar_proyecto_ar(user_id, nombre, scene_data)
            
            popup = Popup(
                title="Escena Guardada",
                content=Label(text="La escena se ha guardado en tus proyectos"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
    
    def load_scenes(self):
        app = App.get_running_app()
        usuario = app.db.get_usuario(app.username)
        
        if usuario:
            user_id = usuario[0]
            proyectos = app.db.get_proyectos_usuario(user_id, "ar")
            
            if proyectos:
                content = BoxLayout(orientation='vertical', spacing=10, padding=10)
                scroll = ScrollView(size_hint=(1, 0.9))
                grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
                grid.bind(minimum_height=grid.setter('height'))
                
                for proyecto in proyectos[:5]:  # Últimas 5 escenas
                    proj_id, user_id, nombre, tipo, datos, fecha = proyecto
                    
                    btn = Button(
                        text=f"{nombre} - {fecha[:10]}",
                        size_hint_y=None,
                        height=50,
                        background_color=(0.2, 0.5, 0.7, 1)
                    )
                    btn.bind(on_release=lambda instance, d=datos: self.load_scene_data(d))
                    grid.add_widget(btn)
                
                scroll.add_widget(grid)
                content.add_widget(scroll)
                
                popup = Popup(
                    title="Seleccionar Escena",
                    content=content,
                    size_hint=(0.9, 0.8)
                )
                popup.open()
            else:
                popup = Popup(
                    title="Sin Escenas",
                    content=Label(text="No hay escenas AR guardadas"),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
    
    def load_scene_data(self, scene_data):
        try:
            data = json.loads(scene_data)
            self.clear_scene()
            
            for item in data:
                self.add_furniture(item["type"])
            
            popup = Popup(
                title="Escena Cargada",
                content=Label(text="Escena cargada correctamente"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
        except:
            popup = Popup(
                title="Error",
                content=Label(text="Error al cargar la escena"),
                size_hint=(0.6, 0.4)
            )
            popup.open()

class ProfileScreen(Screen):
    def on_enter(self):
        self.load_profile()
    
    def load_profile(self):
        app = App.get_running_app()
        self.ids.username_input.text = app.username
        self.load_projects()
    
    def load_projects(self):
        app = App.get_running_app()
        grid = self.ids.projects_grid
        grid.clear_widgets()
        
        usuario = app.db.get_usuario(app.username)
        if usuario:
            user_id = usuario[0]
            proyectos = app.db.get_proyectos_usuario(user_id)
            
            if proyectos:
                for proyecto in proyectos[:10]:  # Últimos 10 proyectos
                    proj_id, user_id, nombre, tipo, datos, fecha = proyecto
                    
                    project_box = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=60,
                        spacing=5
                    )
                    
                    project_box.add_widget(Label(
                        text=f"{nombre} ({tipo})",
                        color=(1,1,1,1),
                        font_size=14,
                        size_hint_x=0.7,
                        halign='left'
                    ))
                    
                    project_box.add_widget(Label(
                        text=fecha[:10],
                        color=(0.7,0.7,0.7,1),
                        font_size=12,
                        size_hint_x=0.3,
                        halign='right'
                    ))
                    
                    grid.add_widget(project_box)
            else:
                grid.add_widget(Label(
                    text="No hay proyectos guardados",
                    color=(0.7,0.7,0.7,1),
                    font_size=14,
                    size_hint_y=None,
                    height=40
                ))
    
    def save_profile(self):
        app = App.get_running_app()
        new_username = self.ids.username_input.text.strip()
        
        if new_username and new_username != app.username:
            if app.db.update_usuario(app.username, new_username):
                app.username = new_username
                popup = Popup(
                    title="Perfil Actualizado",
                    content=Label(text="Nombre de usuario actualizado"),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
    
    def delete_projects(self):
        app = App.get_running_app()
        usuario = app.db.get_usuario(app.username)
        
        if usuario:
            user_id = usuario[0]
            proyectos = app.db.get_proyectos_usuario(user_id)
            
            if proyectos:
                # Eliminar todos los proyectos
                for proyecto in proyectos:
                    app.db.eliminar_proyecto(proyecto[0])
                
                popup = Popup(
                    title="Proyectos Eliminados",
                    content=Label(text="Todos los proyectos han sido eliminados"),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
                self.load_projects()
            else:
                popup = Popup(
                    title="Sin Proyectos",
                    content=Label(text="No hay proyectos para eliminar"),
                    size_hint=(0.6, 0.4)
                )
                popup.open()

# Aplicación principal
class DercoR8App(App):
    username = StringProperty("Usuario")
    
    def build(self):
        self.title = "DercoR8 - Diseño de Interiores"
        
        # Inicializar base de datos
        self.db = Database()
        
        # Obtener usuario actual
        usuario = self.db.get_usuario()
        if usuario:
            self.username = usuario[1]
        
        return Builder.load_string(KV)
    
    def on_start(self):
        # Crear carpetas necesarias
        if not os.path.exists("assets"):
            os.makedirs("assets")
        if not os.path.exists("data"):
            os.makedirs("data")
        
        print("Aplicación DercoR8 iniciada")

if __name__ == "__main__":
    DercoR8App().run()