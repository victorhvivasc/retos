# -*- coding utf-8 -*-
import kivy
import os
import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.accordion import Accordion , AccordionItem
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
import random
from random import shuffle
from os import scandir
from kivy.uix.image import Image
from kivy.core.window import Window


Config.set("graphics", "width", "340")
Config.set("graphics", "height", "640")

def conectar(path):
    try:
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306")
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE laliga")
        print("base de datos creada")
        #creatablaequipo(cursor)
        print("crear tablas pasado")
        conn.commit()
        conn.close()
        """con = sqlite3.connect(path)
        cursor= con.cursor()
        creatablaequipo(cursor)
        con.commit()
        con.close()"""    
    except Exception as e:
        print(e)

class mensajes(Popup):
    pass

class MainWid(ScreenManager):
    def __init__(self, **kwars):
        super(MainWid, self).__init__()
        #control 
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+"/laliga.db"
        self.Startwid = Startwid(self)
        self.basededatoswid = basededatoswid(self)
        self.insertar = BoxLayout()
        self.actualiza_bd = BoxLayout()
        self.infotorneo = BoxLayout(orientation="vertical")
        self.Popup = mensajes()
        self.detallestorneo = BoxLayout(orientation="vertical")
        self.ventanaextratorneo = BoxLayout(orientation="vertical")
        self.inscribirequipo = BoxLayout(orientation="vertical")
        self.buena_fe = BoxLayout()
        self.inscribirjugadora = BoxLayout(orientation="vertical")


        wid = Screen(name="start")
        wid.add_widget(self.Startwid)
        self.add_widget(wid)
        wid = Screen(name="datos")
        wid.add_widget(self.basededatoswid)
        self.add_widget(wid)
        wid = Screen(name="Insertar")
        wid.add_widget(self.insertar)
        self.add_widget(wid)
        wid = Screen(name="Actualiza_torneo")
        wid.add_widget(self.actualiza_bd)
        self.add_widget(wid)
        wid = Screen(name="info_torneo")
        wid.add_widget(self.infotorneo)
        self.add_widget(wid)
        wid = Screen(name="detalle_torneo")
        wid.add_widget(self.detallestorneo)
        self.add_widget(wid)
        wide = Screen(name="Insertar2")
        wide.add_widget(self.ventanaextratorneo)
        self.add_widget(wide)
        wid = Screen(name="Inscribir_equipo")
        wid.add_widget(self.inscribirequipo)
        self.add_widget(wid)
        wid = Screen(name="buena_fe")
        wid.add_widget(self.buena_fe)
        self.add_widget(wid)
        wid = Screen(name="inscribir_jugadora")
        wid.add_widget(self.inscribirjugadora)
        self.add_widget(wid)


        self.goto_start()


    def goto_start(self):
        self.current = "start"

    def goto_datos(self):
        self.basededatoswid.check()
        self.current = "datos"

    def goto_insertdata(self):
        self.insertar.clear_widgets()
        wid = insertar(self)
        self.insertar.add_widget(wid)
        self.current = "Insertar"

    def goto_idat2(self):
        self.ventanaextratorneo.clear_widgets()
        wid = ventanaextratorneo(self)
        self.ventanaextratorneo.add_widget(wid)
        self.current = "Insertar2"

    def goto_actualiza_data(self, data_id):
        self.actualiza_bd.clear_widgets()
        wid = actualiza_bd(self, data_id)
        self.actualiza_bd.add_widget(wid)
        self.current = "Actualiza_torneo"

    def goto_infotorn(self, data_id, id_equipo):
        self.infotorneo.clear_widgets()
        wid = infotorneo(self, data_id, id_equipo)
        self.infotorneo.add_widget(wid)
        self.current = "info_torneo"

    def goto_detalles(self, data_id):
        self.detallestorneo.clear_widgets()
        wid = detallestorneo(self, data_id)
        self.detallestorneo.add_widget(wid)
        self.current = "detalle_torneo"

    def goto_inscripcion(self, data_id):
        self.inscribirequipo.clear_widgets()
        wid = inscribirequipo(self, data_id)
        self.inscribirequipo.add_widget(wid)
        self.current= "Inscribir_equipo"

    def goto_buenafe(self, data_id, id_equipo):
        self.buena_fe.clear_widgets()
        wid = buena_fe(self, data_id, id_equipo)
        self.buena_fe.add_widget(wid)
        self.current= "buena_fe"

    def goto_insc_jugadora(self, data_id, id_equipo):
        self.inscribirjugadora.clear_widgets()
        wid = inscribirjugadora(self, data_id, id_equipo)
        self.inscribirjugadora.add_widget(wid)
        self.current = "inscribir_jugadora"

class Startwid(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(Startwid, self).__init__()
        self.mainwi = mainwi
    
    def createdb(self):
        print("creando")
        conectar(self.mainwi.DB_PATH)
        print("creado")
        self.mainwi.goto_datos()
    
    def fin(self):
        MainApp().stop()

class infotorneo(BoxLayout):
    def __init__(self, mainwi, data_id, data2, **kwars):
        super(infotorneo, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        self.data2 = data2
        self.check2()
        

    def check2(self):
        self.ids.container1.clear_widgets()
        con = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = con.cursor()
        q = "SELECT ID, Nombre FROM equipos WHERE Torneo= Torneo= {} OR torneo2 ={} OR torneo3 ={} OR torneo4 = {} OR torneo5 ={}".format(self.data_id, self.data_id, self.data_id, self.data_id, self.data_id)
        cursor.execute(q)
        for equipo in cursor: 
            print(equipo)
            wid = equipos(self.mainwi)
            wid.data_id = self.data_id
            wid.id_equipo =str(equipo[0])
            wid.nombre_equipo = str(equipo[1])  
            self.ids.container1.add_widget(wid)  
        con.close()
        volver= Button(text="Volver", size_hint_y=0.2)
        self.ids.container1.add_widget(volver)
        volver.bind(on_press=lambda x: (self.goto_dbw()))

        #self.ver_tirno()

    def actualizar(self):
        self.mainwi.goto_infotorneo()

    def ver_tirno(self):
        self.mainwi.goto_datos()

    def goto_dbw(self):
        self.mainwi.goto_datos()

    def ir_buenafe(self, data_id, data2): 
        self.mainwi.goto_buenafe(data_id, data2)

#class pruebaloca(Button):
#    def __init__(self, mainwi, data_id, data2, **kwars):
#        super(infotorneo, self).__init__()
#        self.mainwi = mainwi
#        self.data_id = data_id
#        self.data2 = data2

class basededatoswid(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(basededatoswid, self).__init__()
        self.mainwi = mainwi
        
    
    def check(self):
        self.ids.container.clear_widgets()
        wid = torneo(self.mainwi)
        self.ids.container.add_widget(wid)
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nombre, Organizador, Contacto, Zona FROM torneos")
        for equipo in cursor:
            wid = informacion(self.mainwi)
            e1 = "Torneo: "+str(equipo[1])+"\n"
            e2 = "Cancha: "+ str(equipo[4])+"\n"
            e3 = "Organiza: "+str(equipo[2])+"\n"
            e4 = "Contacto: "+ str(equipo[3])
            wid.data_id = str(equipo[0])
            wid.data = e1+e2+e3+e4
            
            self.ids.container.add_widget(wid)
        conn.close()

class insertar(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(insertar, self).__init__()
        self.mainwi = mainwi

    def inserta_dato(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        #d1 = self.ids.ti_id.text
        d2 = self.ids.ti_nde.text.upper()
        d3 = self.ids.ti_capi.text
        d4 = self.ids.ti_conta.text
        d5 = self.ids.ti_hora.text
        #d15 = (d2, d3, d4, d5)
        s1 = "INSERT INTO torneos(ID, Nombre, Organizador, Contacto, Zona)"
        s2 = 'VALUES(NULL, "%s", "%s", "%s", "%s")'% (d2, d3, d4, d5)
        try:
            if len(str(d2)) !=0 and len(str(d3)) !=0 and len(str(d4)) !=0 and len(str(d5)) !=0:                    
                cursor.execute("SELECT Nombre FROM torneos")
                equire= []
                for i in cursor:
                    equire.append(i[0])
                if not str(d2) in equire:
                    if d4.isdigit() and len(d4) == 10:    
                        cursor.execute(s1+' '+s2)
                        #cursor.execute(query)
                        conn.commit()
                        conn.close()
                        self.mainwi.goto_datos()
                    else:
                        message = self.mainwi.Popup.ids.message
                        self.mainwi.Popup.open()
                        self.mainwi.Popup.title = "Error de novato"
                        message.text = "El contacto debe ser un numero de 10 digitos"                
                else:
                    message = self.mainwi.Popup.ids.message
                    self.mainwi.Popup.open()
                    self.mainwi.Popup.title = "Error de novato"
                    message.text = "Ya existe un Torneo con ese nombre"
    
            else:
                message = self.mainwi.Popup.ids.message
                self.mainwi.Popup.open()
                self.mainwi.Popup.title = "Error de novato"
                message.text = "Complete todos los datos por favor"
        except Exception as e:
            message = self.mainwi.Popup.ids.message
            self.mainwi.Popup.open()
            self.mainwi.Popup.title = "Error de novato"
            message.text = str(e)
        conn.close()

    def inserta_dato2(self):
        global d15
        d15 =[]
        d15.append(self.ids.ti_nde.text.upper())
        d15.append(self.ids.ti_capi.text)
        d15.append(self.ids.ti_conta.text)
        d15.append(self.ids.ti_hora.text)
        d15.append(self.ids.ti_reglas.text)
        if self.ids.tb_relampago.state is "down":
            d15.append("Relampago")
        elif self.ids.tb_elidire.state is "down":
            d15.append("Eliminación Directa")
        elif self.ids.tb_elidob.state is "down":
            d15.append("Eliminación Doble")
        elif self.ids.tb_piram.state is "down":
            d15.append("Piramide")
        else:
            d15.append("No indicado")
            message = self.mainwi.Popup.ids.message
            self.mainwi.Popup.open()
            self.mainwi.Popup.title = "Error de novato"
            message.text = "Seleccione una modalidad de torneo por favor"

        print(d15)
        self.mainwi.goto_idat2()

    def back_to_torneo(self):
        self.mainwi.goto_datos()

class ventanaextratorneo(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(ventanaextratorneo, self).__init__()
        self.mainwi = mainwi
        premio = Label(text="Premios")
        self.texinput = TextInput(hint_text="Descripción de los premios")
        self.ids.container3.add_widget(premio)
        self.ids.container3.add_widget(self.texinput)

    def inserta_dato4(self):
        print(d15)
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        s1 = "INSERT INTO torneos(ID, Nombre, Organizador, Contacto, Zona, Reglas, Tipo_torneo, Premio)"
        s2 = 'VALUES(NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(d15[0], d15[1], d15[2], d15[3], d15[4], d15[5], self.texinput.text)
        try:
            if len(str(d15[0])) !=0 and len(str(d15[1])) !=0 and len(str(d15[2])) !=0 and len(str(d15[3])) !=0:                    
                cursor.execute("SELECT Nombre FROM torneos")
                equire= []
                for i in cursor:
                    equire.append(i[0])
                if not str(d15[0]) in equire:
                    if d15[2].isdigit() and len(d15[2]) == 10:    
                        cursor.execute(s1+' '+s2)
                        #cursor.execute(query)
                        conn.commit()
                        conn.close()
                        self.mainwi.goto_datos()
                    else:
                        message = self.mainwi.Popup.ids.message
                        self.mainwi.Popup.open()
                        self.mainwi.Popup.title = "Error de novato"
                        message.text = "El contacto debe ser un numero de 10 digitos"                
                else:
                    message = self.mainwi.Popup.ids.message
                    self.mainwi.Popup.open()
                    self.mainwi.Popup.title = "Error de novato"
                    message.text = "Ya existe un Torneo con ese nombre"
    
            else:
                message = self.mainwi.Popup.ids.message
                self.mainwi.Popup.open()
                self.mainwi.Popup.title = "Error de novato"
                message.text = "Complete todos los datos por favor"
        except Exception as e:
            message = self.mainwi.Popup.ids.message
            self.mainwi.Popup.open()
            self.mainwi.Popup.title = "Error de novato"
            message.text = str(e)
        conn.close()
        d15.clear()

    def continuar(self):
        self.mainwi.goto_datos()
    
    def volver(self):
        self.mainwi.goto_insertdata()

class actualiza_bd(BoxLayout):
    def __init__(self, mainwi, data_id, **kwars):
        super(actualiza_bd, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        self.ver_datos()
    
    def ver_datos(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        z = "SELECT Nombre, Organizador, Contacto, Zona FROM torneos WHERE ID ="
        cursor.execute(z+self.data_id)
        for i in cursor:
            self.ids.ti_nde.text = i[0]
            self.ids.ti_capi.text = i[1]
            self.ids.ti_conta.text = i[2]
            self.ids.ti_hora.text = i[3]     
        conn.close()       
        print("verdatos")

    def confirmaact(self):
        box = BoxLayout(orientation="vertical")
        botones = BoxLayout(orientation="vertical")
        self.si = Button(text="si", size_hint_y=0.2, background_normal='', background_color=(1,0,0,1))
        self.no = Button(text="no", size_hint_y=0.2, background_normal='', background_color=(0,0,1,1))
        etiqueta = Label(text="¿Seguro que desea editar?\n Esta acción es irreversible")
        
        botones.add_widget(etiqueta)
        botones.add_widget(self.si)
        botones.add_widget(self.no)
        box.add_widget(botones)

        pop = Popup(title="Mejor tarde que nunca", content=box)        
        pop.open()
        self.si.bind(on_press=lambda x: (self.act_data(), pop.dismiss()))
        self.no.bind(on_press=lambda y: (pop.dismiss()))

    def act_data(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        #d1 = self.ids.ti_id.text
        d2 = self.ids.ti_nde.text.upper()
        d3 = self.ids.ti_capi.text
        d4 = self.ids.ti_conta.text
        d5 = self.ids.ti_hora.text
        d15 = (d2, d3, d4, d5)
        s1 = "UPDATE torneos SET"
        s2 = 'Nombre = "%s", Organizador= "%s", Contacto= "%s", Zona= "%s"'% d15
        s3 = 'WHERE ID= %s'% self.data_id
        try:
            if len(str(d2)) !=0 and len(str(d3)) !=0 and len(str(d4)) !=0 and len(str(d5)) !=0:                    
                if d4.isdigit() and len(d4) == 10:    
                    cursor.execute(s1+' '+s2+' '+s3)
                    #cursor.execute(query)
                    conn.commit()
                    conn.close()
                    self.mainwi.goto_datos()
                else:
                    message = self.mainwi.Popup.ids.message
                    self.mainwi.Popup.open()
                    self.mainwi.Popup.title = "Error de novato"
                    message.text = "El contacto debe ser un numero de 10 digitos"
            else:
                message = self.mainwi.Popup.ids.message
                self.mainwi.Popup.open()
                self.mainwi.Popup.title = "Error de novato"
                message.text = "Complete todos los datos por favor"
        except Exception as e:
            message = self.mainwi.Popup.ids.message
            self.mainwi.Popup.open()
            self.mainwi.Popup.title = "Error de novato"
            message.text = str(e)
        conn.close()

    def confirmadelete(self):
        box = BoxLayout(orientation="vertical")
        botones = BoxLayout(orientation="vertical")
        self.si = Button(text="si", size_hint_y=0.2, background_normal='', background_color=(1,0,0,1))
        self.no = Button(text="no", size_hint_y=0.2, background_normal='', background_color=(0,0,1,1))
        etiqueta = Label(text="¿Seguro que desea eliminar?\n Esta acción es irreversible")
        
        botones.add_widget(etiqueta)
        botones.add_widget(self.si)
        botones.add_widget(self.no)
        box.add_widget(botones)

        pop = Popup(title="Dificil decision", content=box)        
        pop.open()
        self.si.bind(on_press=lambda x: (self.delete(), pop.dismiss()))
        self.no.bind(on_press=lambda y: (pop.dismiss()))

    def delete(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        s = "DELETE FROM torneos WHERE ID="+self.data_id
        cursor.execute(s)
        conn.commit()
        conn.close()
        self.mainwi.goto_datos()

    def back_to_dbw(self):
        self.mainwi.goto_datos()

class informacion(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(informacion, self).__init__()
        self.mainwi = mainwi
        ruta = "imagenes/torneos/"
        lstFiles = []
        lstDir = os.walk(ruta)
        for root, dirs, files in lstDir:
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                if(extension == ".png"):
                    lstFiles.append(nombreFichero+extension) 
        #lista = ["imagenes/cintillo.png", "imagenes/balon.png", "imagenes/finta.png"]
        shuffle(lstFiles)
        self.imagenes = lstFiles[1]


    def inform(self, data_id, data2):
        self.mainwi.goto_infotorn(data_id, data2)
        #print("data1 inform= "+str(self.data1))
        #print("dataid= "+str(self.data_id))
        
    def actualizar(self, data_id):
        self.mainwi.goto_actualiza_data(data_id)

    def verdetalles(self, data_id):
        self.mainwi.goto_detalles(data_id)

class torneo(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(torneo, self).__init__()
        self.mainwi = mainwi

    def crear_torneo(self):
        print("torneo nuevo")
        self.mainwi.goto_insertdata()

    def goto_atras(self):
        self.mainwi.goto_start()

class equipos(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(equipos, self).__init__()
        self.mainwi = mainwi

    def goto_jugadora(self, data_id, id_equipo):
        self.mainwi.goto_buenafe(data_id, id_equipo)

    #def goto_atrase(self):
    #    self.mainwi.goto_start()

class jugadora(BoxLayout):
    def __init__(self, mainwi, **kwars):
        super(jugadora, self).__init__()
        self.mainwi = mainwi

    def goto_jugadora(self, data_id, id_equipo):
        self.mainwi.goto_buenafe(data_id, id_equipo)

class detallestorneo(BoxLayout):
    def __init__(self, mainwi, data_id, **kwars):
        super(detallestorneo, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        self.ids.container2.clear_widgets()
        #eti= Label(text="Navega por el contenido")
        #self.ids.container2.add_widget(eti)
        
        root = Accordion (orientation="vertical", anim_duration=2.5)
        item1 = AccordionItem(title="Reglas")
        item2 = AccordionItem(title="Fixture")
        item3 = AccordionItem(title="Premios")
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        q = "SELECT Reglas, Premio FROM torneos WHERE ID="
        cursor.execute(q+self.data_id)
        for x in cursor:
            print(x)
            item1.add_widget(Label(text=x[0], text_size=(300, None), valign="top"))
            item2.add_widget(Label(text='%s'%x[0], text_size=(300, None)))
            item3.add_widget(Label(text=x[1], text_size=(300, None), halign="center", valign="top"))
            root.add_widget(item1)
            root.add_widget(item2)
            root.add_widget(item3)
        self.ids.container2.add_widget(root)

        conn.close()

    def goto_atras(self):
        self.mainwi.goto_datos()

    def goto_innsc(self, data_id):
        self.mainwi.goto_inscripcion(data_id)

class inscribirequipo(BoxLayout):
    def __init__(self, mainwi, data_id, **kwars):
        super(inscribirequipo, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        q = "SELECT Nombre FROM torneos WHERE ID="
        cursor.execute(q+self.data_id)
        for x in cursor:
            titulo= Label(text="Torneo: [b][color=000000]%s"%x[0], markup=True)
            self.ids.container4.add_widget(titulo)
        conn.close()
        caja = BoxLayout(orientation= "horizontal")
        regis = Label(text="[color=000000][b]EQUIPOS REGISTRADOS", markup=True)
        self.ids.container4.add_widget(regis)
        equipol = Label(text="Nombre del equipo")
        self.equipoti = TextInput(hint_text="Indique el nombre del equipo a inscribir")
        caja.add_widget(equipol)
        caja.add_widget(self.equipoti)
        self.ids.container4.add_widget(caja)
        #self.ids.container4.add_widget(equipol)
        #self.ids.container4.add_widget(equipoti)
        caja1 = BoxLayout(orientation= "horizontal")
        equipo1l = Label(text="Preferencia Horaria")
        equipo1ti = TextInput(hint_text="¿En qué horario prefieren jugar?")
        self.breg = Button(text="Inscribirse")
        #self.ids.container4.add_widget(equipo1l)
        #self.ids.container4.add_widget(equipo1ti)
        caja1.add_widget(equipo1l)
        caja1.add_widget(equipo1ti)
        self.ids.container4.add_widget(caja1)
        self.ids.container4.add_widget(self.breg)
        self.breg.bind(on_press= lambda x: self.inscripcion_torneo())
        sepa = Label(text="")
        self.ids.container4.add_widget(sepa)
                
        equipon = Label(text="[color=000000][b]EQUIPOS NO REGISTRADOS", markup= True)

        caja2= BoxLayout(orientation="horizontal")
        self.ids.container4.add_widget(equipon)
        equipon1 = Label(text="Nombre del equipo")
        self.equipon1ti = TextInput(hint_text="Indique el nombre del equipo a registrar")
        caja2.add_widget(equipon1)
        caja2.add_widget(self.equipon1ti)
        self.ids.container4.add_widget(caja2)
        #self.ids.container4.add_widget(equipon1)
        #self.ids.container4.add_widget(self.equipon1ti)
        caja3 = BoxLayout(orientation="horizontal")
        equipon2 = Label(text="Nombre de DT\n   Capitana")
        self.equipon2ti = TextInput(hint_text="Indique director tecnico ó capitana")
        caja3.add_widget(equipon2)
        caja3.add_widget(self.equipon2ti)
        self.ids.container4.add_widget(caja3)
        #self.ids.container4.add_widget(equipon2)
        #self.ids.container4.add_widget(self.equipon2ti)
        caja4 = BoxLayout(orientation="horizontal")
        equipon3 = Label(text="Teléfono de contacto")
        self.equipon3ti = TextInput(hint_text="Indique incluyendo el código de area ejemplo: 1512345678")
        caja4.add_widget(equipon3)
        caja4.add_widget(self.equipon3ti)
        self.ids.container4.add_widget(caja4)
        #self.ids.container4.add_widget(equipon3)
        #self.ids.container4.add_widget(self.equipon3ti)
        caja5 = BoxLayout(orientation="horizontal")
        equipon4 = Label(text="Zona de juego")
        self.equipon4ti = TextInput(hint_text="En que lugar practican (No obligatorio)")
        caja5.add_widget(equipon4)
        caja5.add_widget(self.equipon4ti)
        self.ids.container4.add_widget(caja5)
        #self.ids.container4.add_widget(equipon4)
        #self.ids.container4.add_widget(equipon4ti)
        equipon5 = Label(text="Preferencia Horaria")
        self.ids.container4.add_widget(equipon5)
        botonera = BoxLayout(orientation="horizontal")
        b1= ToggleButton(text="9:00\n a \n12:00")
        botonera.add_widget(b1)
        b2= ToggleButton(text="13:00\n a \n16:00")
        botonera.add_widget(b2)
        b3= ToggleButton(text="16:00\n a \n17:00")
        botonera.add_widget(b3)
        b4= ToggleButton(text="18:00\n a \n21:00")
        botonera.add_widget(b4)
        b5= ToggleButton(text="22:00\n a \n00:00")
        botonera.add_widget(b5)
        self.b6= Button(text="Registrar e inscribir")
        self.ids.container4.add_widget(botonera)
        self.ids.container4.add_widget(self.b6)
        self.b6.bind(on_release= lambda x: self.confirma_equipo_nuevo())

    def inscripcion_torneo(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM equipos")
        equire1= []
        for i in cursor:
            equire1.append(i[0])
        if str(self.equipoti.text).upper() in equire1:
            sql= "SELECT ID, Torneo, torneo2, torneo3, torneo4, torneo5 FROM equipos"
            sql2= "WHERE Nombre='{}'".format(self.equipoti.text)
            cursor.execute(sql+' '+sql2)
            for e in cursor:

                if int(e[1]) == 0:
                    s1 = "UPDATE equipos SET"
                    s2 = 'Torneo= "%s"'% self.data_id
                    s3 = 'WHERE ID= %s'% e[0]
                    cursor.execute(s1+' '+s2+' '+s3)
                    conn.commit()    
                    self.retornar()
                elif int(e[2]) == 0:
                    s1 = "UPDATE equipos SET"
                    s2 = 'torneo2= "%s"'% self.data_id
                    s3 = 'WHERE ID= %s'% e[0]
                    cursor.execute(s1+' '+s2+' '+s3)
                    conn.commit()    
                    self.retornar()
                elif int(e[3]) == 0:
                    s1 = "UPDATE equipos SET"
                    s2 = 'torneo3= "%s"'% self.data_id
                    s3 = 'WHERE ID= %s'% e[0]
                    cursor.execute(s1+' '+s2+' '+s3)
                    conn.commit()    
                    self.retornar()
                elif int(e[4]) == 0:
                    s1 = "UPDATE equipos SET"
                    s2 = 'torneo4= "%s"'% self.data_id
                    s3 = 'WHERE ID= %s'% e[0]
                    cursor.execute(s1+' '+s2+' '+s3)
                    conn.commit()    
                    self.retornar()
                elif int(e[5]) == 0:
                    s1 = "UPDATE equipos SET"
                    s2 = 'torneo5= "%s"'% self.data_id
                    s3 = 'WHERE ID= %s'% e[0]
                    cursor.execute(s1+' '+s2+' '+s3)
                    conn.commit()    
                    self.retornar()
                else:
                    message = self.mainwi.Popup.ids.message
                    self.mainwi.Popup.open()
                    self.mainwi.Popup.title = "Error de novato"
                    message.text = "El equipo esta registrado en 5 \n torneos, por favor de la baja \n en alguno para poder registrarse"
        else:
                message = self.mainwi.Popup.ids.message
                self.mainwi.Popup.open()
                self.mainwi.Popup.title = "Error de novato"
                message.text = "El equipo no esta registrado aún\n Por favor registrelo a continuación"
        conn.close()
                  
    def confirma_equipo_nuevo(self):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        nombrem = str(self.equipon1ti.text).upper()
        s1 = "INSERT INTO equipos(ID, Nombre, Capitan, Contacto)"
        s2 = 'VALUES(NULL, "%s", "%s", "%s")'%(nombrem, self.equipon2ti.text, self.equipon3ti.text) 
        try:
            if len(nombrem) !=0 and len(str(self.equipon2ti.text)) !=0 and len(str(self.equipon3ti.text)) !=0:                    
                cursor.execute("SELECT Nombre FROM equipos")
                equire= []
                for i in cursor:
                    equire.append(i[0])
                if not nombrem in equire:
                    if self.equipon3ti.text.isdigit() and len(self.equipon3ti.text) == 10:    
                        cursor.execute(s1+' '+s2)
                        conn.commit()
                        conn.close()
                        self.mainwi.goto_datos()
                    else:
                        message = self.mainwi.Popup.ids.message
                        self.mainwi.Popup.open()
                        self.mainwi.Popup.title = "Error de novato"
                        message.text = "El contacto debe ser un numero de 10 digitos"                
                else:
                    message = self.mainwi.Popup.ids.message
                    self.mainwi.Popup.open()
                    self.mainwi.Popup.title = "Error de novato"
                    message.text = "Ya existe un Equipo con ese nombre"
            else:
                message = self.mainwi.Popup.ids.message
                self.mainwi.Popup.open()
                self.mainwi.Popup.title = "Error de novato"
                message.text = "Complete todos los datos por favor"
        except Exception as e:
            message = self.mainwi.Popup.ids.message
            self.mainwi.Popup.open()
            self.mainwi.Popup.title = "Error de novato"
            message.text = str(e)
        conn.close()

    def retornar(self):
        self.mainwi.goto_datos()

class buena_fe(BoxLayout):
    def __init__(self, mainwi, data_id, id_equipo, **kwars):
        super(buena_fe, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        self.id_equipo = id_equipo
        self.ver_lista(data_id, id_equipo)
        
    def ver_lista(self, data_id, id_equipo):
        conn = mysql.connector.connect(host="167.250.49.138", user="root", passwd="civ6525639", port="3306", database="laliga")
        cursor = conn.cursor()
        q = "SELECT dni1, dni2, dni3, dni4, dni5, dni6, dni7, dni8, dni9, dni10, dni11, dni12 FROM lista_buena_fe WHERE id_torneo={} AND id_equipo={}".format(str(self.data_id), str(self.id_equipo))
        #eq= (str(self.data_id), str(self.id_equipo))
        cursor.execute(q)
        for x in cursor:
            for y in x:
                try:
                    q1 = "SELECT Nombres, Apellidos FROM jugadora WHERE DNI = {}".format(str(y))     
                    cursor.execute(q1)
                    for z in cursor:
                        j = Button(text="Jugadora: {} {}".format(z[0], z[1]))                
                        self.ids.container5.add_widget(j)        
                except Exception as e:
                    pass
                
    def goto_principio(self, data_id, id_equipo):
        self.mainwi.goto_infotorn(data_id, id_equipo)

    def goto_insj(self, data_id, id_equipo):
        self.mainwi.goto_insc_jugadora(data_id, id_equipo)

class inscribirjugadora(BoxLayout):
    def __init__(self, mainwi, data_id, id_equipo,  **kwars):
        super(inscribirjugadora, self).__init__()
        self.mainwi = mainwi
        self.data_id = data_id
        self.id_equipo = id_equipo
        wid = jugadora(self.mainwi)
        self.ids.container6.add_widget(wid)



    def volver(self, data_id, id_equipo):
        self.mainwi.goto_buenafe(data_id, id_equipo)

class MainApp(App):
    title = "La Liga de Futbol"
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return MainWid()
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:
            return False

if __name__ == "__main__":
    MainApp().run()
