from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from fpdf import FPDF
import os

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class EtiquetadorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.archivo_db = ""
        self.codigos = []

        lbl_instruccion1 = Label(text="1. Selecciona tu Base de Datos (.txt):", size_hint_y=None, height=40, color=(0,0,0,1))
        self.add_widget(lbl_instruccion1)
        
        self.filechooser = FileChooserListView(filters=['*.txt'], path='/storage/emulated/0/')
        self.add_widget(self.filechooser)

        self.btn_cargar = Button(text="Cargar Base de Datos", size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1))
        self.btn_cargar.bind(on_release=self.seleccionar_archivo)
        self.add_widget(self.btn_cargar)

        self.lbl_archivo = Label(text="Ningún archivo seleccionado", size_hint_y=None, height=30, color=(0.4, 0.4, 0.4, 1))
        self.add_widget(self.lbl_archivo)

        lbl_instruccion2 = Label(text="2. Escanea el código:", size_hint_y=None, height=40, color=(0,0,0,1))
        self.add_widget(lbl_instruccion2)
        
        self.entrada_codigo = TextInput(font_size=35, multiline=False, size_hint_y=None, height=70, halign='center')
        self.entrada_codigo.bind(on_text_validate=self.agregar_codigo)
        self.add_widget(self.entrada_codigo)

        self.lbl_lista = Label(text="Códigos a imprimir:\n", size_hint_y=None, height=120, color=(0,0,0,1))
        self.add_widget(self.lbl_lista)

        self.btn_generar = Button(text="GENERAR PDF", size_hint_y=None, height=70, background_color=(0.8, 0.2, 0.2, 1), font_size=20, bold=True)
        self.btn_generar.bind(on_release=self.generar_pdf)
        self.add_widget(self.btn_generar)

    def seleccionar_archivo(self, instance):
        if self.filechooser.selection:
            self.archivo_db = self.filechooser.selection[0]
            nombre = os.path.basename(self.archivo_db)
            self.lbl_archivo.text = f"Base cargada: {nombre}"
        else:
            self.mostrar_mensaje("Error", "Selecciona un archivo .txt de la lista.")

    def agregar_codigo(self, instance):
        codigo_completo = self.entrada_codigo.text.strip()
        if codigo_completo:
            if codigo_completo.endswith(".0"):
                codigo_completo = codigo_completo[:-2]
            
            codigo_7 = codigo_completo[-7:] 
            self.codigos.append(codigo_7)
            
            mostrar = self.codigos[-5:]
            self.lbl_lista.text = "Códigos a imprimir:\n" + ", ".join(mostrar) + ("..." if len(self.codigos)>5 else "")
            
            self.entrada_codigo.text = ""
            Clock.schedule_once(lambda dt: setattr(self.entrada_codigo, 'focus', True), 0.1)

    def generar_pdf(self, instance):
        if not self.archivo_db:
            self.mostrar_mensaje("Error", "Primero selecciona tu base de datos.")
            return
        if not self.codigos:
            self.mostrar_mensaje("Error", "No hay códigos escaneados.")
            return
        
        try:
            diccionario_productos = {}
            with open(self.archivo_db, 'r', encoding='utf-8') as f:
                for linea in f:
                    partes = linea.strip().split(',')
                    if len(partes) >= 4:
                        cod = partes[0].strip()[-7:]
                        diccionario_productos[cod] = {
                            "mayoreo": partes[1].strip(),
                            "caja": partes[2].strip(),
                            "pzs": partes[3].strip()
                        }
            
            carpeta = os.path.dirname(self.archivo_db)
            ruta_pdf = os.path.join(carpeta, "ETIQUETAS_IMPRIMIR.pdf")
            
            pdf = FPDF(unit='cm', format=(6, 4))
            
            for cod in self.codigos:
                pdf.add_page()
                
                if cod in diccionario_productos:
                    datos = diccionario_productos[cod]
                    try:
                        m_val = float(datos['mayoreo'])
                        c_val = float(datos['caja'])
                        p_val = int(float(datos['pzs']))
                        
                        txt_mayoreo = f"MAYOREO: ${m_val:.2f}"
                        txt_caja = f"CAJA: ${c_val:.2f} ({p_val} pzs)"
                    except ValueError:
                        txt_mayoreo = f"MAYOREO: {datos['mayoreo']}"
                        txt_caja = f"CAJA: {datos['caja']} ({datos['pzs']} pzs)"
                    
                    pdf.set_font("Arial", 'B', 24)
                    pdf.set_xy(0, 0.5)
                    pdf.cell(w=6, h=1, txt=str(cod), align='C')
                    
                    pdf.set_font("Arial", 'B', 12)
                    pdf.set_xy(0, 1.8)
                    pdf.cell(w=6, h=1, txt=txt_mayoreo, align='C')
                    
                    pdf.set_font("Arial", 'B', 11)
                    pdf.set_xy(0, 2.7)
                    pdf.cell(w=6, h=1, txt=txt_caja, align='C')
                    
                    pdf.rect(x=0.1, y=0.1, w=5.8, h=3.8)
                else:
                    pdf.set_font("Arial", 'B', 16)
                    pdf.set_xy(0, 1.0)
                    pdf.cell(w=6, h=1, txt=str(cod), align='C')
                    pdf.set_font("Arial", '', 10)
                    pdf.set_xy(0, 2.0)
                    pdf.cell(w=6, h=1, txt="No encontrado", align='C')
                
            pdf.output(ruta_pdf)
            
            self.codigos = []
            self.lbl_lista.text = "Códigos a imprimir:\n"
            self.mostrar_mensaje("¡PDF Creado!", f"Tu PDF se guardó en:\n{ruta_pdf}")
            
        except Exception as e:
            self.mostrar_mensaje("Error", f"Ocurrió un problema:\n{str(e)}")

    def mostrar_mensaje(self, titulo, mensaje):
        popup = Popup(title=titulo, content=Label(text=mensaje, text_size=(Window.width*0.7, None), halign='center'), 
                      size_hint=(0.8, 0.4))
        popup.open()

class AppEtiquetas(App):
    def build(self):
        return EtiquetadorLayout()

if __name__ == '__main__':
    AppEtiquetas().run()