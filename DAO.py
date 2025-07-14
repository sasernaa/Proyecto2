import re
import io
import os
from Cliente import Cliente
from Empleado import Empleado
from Servicio import Servicio
from Reserva import Reserva
from tabulate import tabulate #Instalar tabulate (pip install tabulate)
from datetime import datetime
from datetime import date

class DAO():
    def __init__(self,clientes,servicios,empleados,handleClientes,handleEmpleados,handleServicios,handleReservas,reservas):
        self.clientes = clientes
        self.servicios = servicios
        self.empleados = empleados
        self.handleClientes = handleClientes
        self.handleEmpleados = handleEmpleados
        self.handleServicios = handleServicios
        self.handleReservas = handleReservas
        self.reservas = reservas

    def validar_codigo_servicio(self,codigo):
        validCode = re.match(r'^[0-9]{3}$',codigo)
        return True if validCode else False

    def validar_email(self,email):
        validEmail = re.match(r'^[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-z]{2,}$',email)
        return True if validEmail else False
    
    def validar_nombre(self,nombre):
        validName = re.match(r'^[a-zA-Z]+$',nombre)
        return True if validName else False

    def validar_telefono(self,telefono):
        validTelephone = re.match(r'^[0-9\s]{10}$',telefono)
        return True if validTelephone else False
    
    def validar_cedula(self,cedula):
        validCedula = re.match(r'^[0-9]{7,10}$',cedula)
        return True if validCedula else False

    def validar_fecha(self,fecha):
        formatoFecha = "%d/%m/%Y"
        try:
            tempdate = datetime.strptime(fecha,formatoFecha)
            if(tempdate >= datetime.now()):
                return True
            else:
                raise ValueError()
        except ValueError:
            return False

    def get_codigos(self,lista):
        temp = []
        for i in lista:
            temp.append(i.get_cedula())
        return temp

    def verificar_Empleado_sin_Reservas(self,xcedula):
        test = True
        for r in self.reservas:
            if(r.get_idespecialista() == xcedula):
                test = False
        return test
    
    def crear_Empleado(self):
        print("Bienvenido a la seccion crear empleado, para cancelar la operacion digite: salir()\nPor favor digite:")
        while(True):
            xcedula = input("Cedula: ")
            if(xcedula == "salir()"):
                break
            elif(self.validar_cedula(xcedula)):
                while(True):
                    xnombre = input("Primer nombre: ")
                    if(xnombre == "salir()"):
                        break
                    elif(self.validar_nombre(xnombre)):
                        while(True):
                            xapellido = input("Apellido: ")
                            if(xapellido == "salir()"):
                                break
                            elif(self.validar_nombre(xapellido)):
                                while(True):
                                    xtelefono = "".join(input("Numero telefónico: ").split(" "))
                                    if(xtelefono == "salir()"):
                                        break
                                    elif(self.validar_telefono(xtelefono)):
                                        while(True):
                                            xemail = input("Email: ")
                                            if(xemail == "salir()"):
                                                break
                                            elif(self.validar_email(xemail)):
                                                xservicio = list(input("Servicio: ").split(","))
                                                if(xservicio == ["salir()"]):
                                                    break
                                                else:
                                                    test = True
                                                    idsServicios = []
                                                    for s in self.servicios:
                                                        idsServicios.append(s.get_codigo())
                                                    test2 = True
                                                    for s in xservicio:
                                                        if(s not in idsServicios):
                                                            test2 = False
                                                            break
                                                    for e in self.empleados:
                                                        if(e.get_cedula() == xcedula):
                                                            test = False
                                                    if(test and test2):
                                                        empleado = Empleado(xcedula,xnombre,xapellido,xtelefono,xemail,xservicio)
                                                        self.empleados.append(empleado)
                                                        self.handleEmpleados.seek(0,io.SEEK_END)
                                                        self.handleEmpleados.write(empleado.formato_escrito())
                                                        self.handleEmpleados.flush()
                                                        os.fsync(self.handleEmpleados.fileno())        
                                                        print("Operacion exitosa :)\n")
                                                        break
                                                    else:
                                                        print("Error: Duplicidad en id de empleado/No existe codigo de servicio")
                                                break
                                            else:
                                                print(f"{xemail} no es un email valido :(\nDebe tener formato de email")
                                        break
                                    else:
                                        print(f"{xtelefono} no es un numero telefonico valido :(\nSolo se acepta numeros y espacios con 10 caracteres")
                                break    
                            else:
                                print(f"{xapellido} no es un apellido valido :(\nEl formato solo acepta letras sin espacio")
                        break
                    else:
                        print(f"{xnombre} no es un nombre valido :(\nEl formato solo acepta letras sin espacio")
                break
            else:
                print("Formato de cedula incorrecto :(\nDebe ser numeros entre 7-10 caracteres sin espacio")

    def borrar_Empleado(self):
        print("Bienvenido a la seccion borrar empleado, por favor digite:")
        xcedula = input("Cedula del empleado: ")
        test = False
        for e in self.empleados:
            if(e.get_cedula() == xcedula):
                test = True
                break
        if(test):
            if(self.verificar_Empleado_sin_Reservas(xcedula)):
                self.empleados.remove(e)
                self.handleEmpleados.seek(0)
                self.handleEmpleados.truncate()
                for empleado in self.empleados:
                    self.handleEmpleados.write(empleado.formato_escrito().rstrip("\n"))
                    self.handleEmpleados.write("\n")
                self.handleEmpleados.flush()
                os.fsync(self.handleEmpleados.fileno())
                print("Operacion exitosa :)")
            else:
                print(f"No se puede borrar al empleado de cedula: {xcedula}\nYa tiene una reserva asignada :(")
        else:
            print(f"No existe un empleado con cedula: {xcedula}")
    
    def validar_idReserva(self,idReserva):
        test = True
        listaidReservas = []
        for r in self.reservas:
            listaidReservas.append(r.get_idReserva())
        if(idReserva in listaidReservas):
            test = False
        return test

    def validar_disponibilidad_Reserva(self,idEspecialista,idServicio,fecha,hora):
        test = True
        temp = 0
        for e in self.empleados:
            if(e.get_cedula() == idEspecialista):
                temp = e
        if(idServicio in temp.get_servicio()):
            for r in self.reservas:
                if(r.get_fecha() == fecha and r.get_hora() == hora and r.get_idespecialista() == idEspecialista and r.get_idservicio() == idServicio):
                    test = False
                    print(f"El especialista: {temp.get_nombre()} ya tiene una cita para\nFecha: {fecha} y hora: {hora}")
                    break
        else:
            test = False
            print(f"El especialista: {temp.get_nombre()} no provee el servicio de codigo: {idServicio} :(")
        return test

    def validar_agenda_Cliente(self,idCliente,fecha,hora):
        test = True
        for r in self.reservas:
            if(r.get_idCliente() == idCliente and r.get_fecha() == fecha and r.get_hora() == hora):
                    test = False
        return test

    def validar_agenda_Empleado(self,idEspecialista,fecha,hora):
        test = True
        for r in self.reservas:
            if(r.get_idespecialista() == idEspecialista and r.get_fecha() == fecha and r.get_hora() == hora):
                test = False
        return test
    
    def crear_Reserva(self,xcedula):
        print("Modulo Cliente/Agendar_cita Digite:\nSi desea salir digite: salir()")
        while(True):
            xidReserva = input("Añada un id para la reserva: ")
            if(xidReserva == "salir()"):
                break
            else:
                test = self.validar_idReserva(xidReserva)
                if(not test):
                    print("Este id de la reserva ya existe")
                else:
                    while(True):
                        xidespecialista = input("Cedula del especialista: ")
                        if(xidespecialista == "salir()"):
                            break
                        else:
                            if(xidespecialista in self.get_codigos(self.empleados) and test):
                                while(True):
                                    xidservicio = input("Codigo del servicio: ")
                                    if(xidservicio == "salir()"):
                                        break
                                    else:
                                        while(True):
                                            xfecha = input("Fecha(D/M/YYYY): ")
                                            if(xfecha == "salir()"):
                                                break
                                            elif(self.validar_fecha(xfecha)):
                                                while(True):
                                                    xhora = input("Hora(8-18): ")
                                                    if(xhora == "salir()"):
                                                        break
                                                    elif(xhora in ["8","9","10","11","12","13","14","15","16","17","18"]):
                                                        if(self.validar_agenda_Empleado(xidespecialista,xfecha,xhora)):
                                                            if(self.validar_agenda_Cliente(xcedula,xfecha,xhora)):
                                                                if(self.validar_disponibilidad_Reserva(xidespecialista,xidservicio,xfecha,xhora)):
                                                                    tempserv = 0
                                                                    for s in self.servicios:
                                                                        if(s.get_codigo() == xidservicio):
                                                                            tempserv = s
                                                                            break
                                                                    reserva = Reserva(xidReserva,xcedula,xidespecialista,xidservicio,tempserv.get_costo(),tempserv.get_nombre(),xfecha,xhora)
                                                                    self.reservas.append(reserva)
                                                                    self.handleReservas.seek(0,io.SEEK_END)
                                                                    self.handleReservas.write(reserva.formato_escrito())
                                                                    self.handleReservas.flush()
                                                                    os.fsync(self.handleReservas.fileno())
                                                                    print("Operacion exitosa :)\n",f"Recuerde su cita para: {xfecha} a las {xhora}")
                                                                    break
                                                            else:
                                                                print(f"Ya tienes un cita agendada para la fecha: {xfecha} y la hora: {xhora}")        
                                                        else:
                                                            print(f"El especialista con id: {xidespecialista} ya esta ocupado para\nFecha: {xfecha} y hora: {xhora}")
                                                    else:
                                                        print("La hora debe ser un numero entre 8 y 18")
                                                break
                                            else:
                                                print("Formato invalido para fecha, se espera recibir: D/M/YYYY")
                                        break
                                break
                            else:
                                print(f"No existe un especialista de id: {xidespecialista} :(")
                    break

    def consultar_Reservas(self,xcedula):
        listaReservas = []
        for r in self.reservas:
            if(r.get_idCliente() == xcedula):
                listaReservas.append(r)
        return listaReservas

    def cancelar_Reserva(self,xcedula,xidReserva):
        listaRservas = self.consultar_Reservas(xcedula)
        temp = 0
        for r in listaRservas:
            if(r.get_idReserva() == xidReserva):
                temp = r
                break
        else:
            print(f"No se encontro reserva con codigo {xidReserva} :(")
        if(temp != 0):    
            self.reservas.remove(temp)
            self.handleReservas.seek(0)
            self.handleReservas.truncate()
            for reserva in self.reservas:
                self.handleReservas.write(reserva.formato_escrito().rstrip("\n"))
                self.handleReservas.write("\n")
            self.handleReservas.flush()
            os.fsync(self.handleReservas.fileno())
            print(f"Se ha borrado la reserva con id: {xidReserva}")

    def acceder_cliente(self):
        xcedula = input("Digite su cedula--> ")
        test = True
        temp = 0
        for c in self.clientes:
            if(c.get_cedula() == xcedula):
                temp = c
                break
        else:
            print("No se ha encontrado su cedula en la base de datos :(")
            test = False
        if(test):
            while(True):
                print(f"Hola! {temp.get_nombre()} Presione:\n1: Agendar cita\n2: Cancelar cita\n3: Consultar citas\n4: Salir")
                tramiteCliente = input("--> ")
                if(tramiteCliente == "1"):
                    self.crear_Reserva(temp.get_cedula())
                elif(tramiteCliente == "2"):
                    idReserva = input("Ingrese el id de la reserva--> ")
                    self.cancelar_Reserva(xcedula,idReserva)
                elif(tramiteCliente == "3"):
                    temp1 = []
                    for r in self.consultar_Reservas(xcedula):
                        temp1.append(r.imprimir())
                    print(f"Cliente ID: {xcedula}\n")
                    print(tabulate(temp1,headers=["Id Reserva","Id Especialista","Id Servicio","Fecha","Hora","Costo","Servicio"]))   
                elif(tramiteCliente == "4"):
                    break
                else:
                    print("Opcion incorrecta :(")

    def crear_cliente(self):
        print("Bienvenido a crear una cuenta, si desea salir digite: salir()\nPor favor: ")
        while(True):
            test = True
            xcedula = input("Ingrese su cedula: ")
            if(xcedula == "salir()"):
                break
            elif(self.validar_cedula(xcedula)):
                for c in self.clientes:
                    if(c.get_cedula() == xcedula):
                        test = False
                if(test):
                    while(True):
                        xnombre = input("Ingrese su primer nombre: ")
                        if(xnombre == "salir()"):
                            break
                        elif(self.validar_nombre(xnombre)):
                            while(True):
                                xapellido = input("Ingrese su apellido: ")
                                if(xapellido == "salir()"):
                                    break
                                elif(self.validar_nombre(xapellido)):
                                    while(True):
                                        xtelefono = "".join(input("Ingrese su número telefónico: ").split(" "))
                                        if(xtelefono == "salir()"):
                                            break
                                        elif(self.validar_telefono(xtelefono)):
                                            while(True):
                                                xemail = input("Ingrese su email: ")
                                                if(xemail == "salir()"):
                                                    break
                                                elif(self.validar_email(xemail)):
                                                    cliente = Cliente(cedula=xcedula,nombre=xnombre,apellido=xapellido,telefono=xtelefono,email=xemail)
                                                    self.clientes.append(cliente)
                                                    self.handleClientes.seek(0,io.SEEK_END)
                                                    self.handleClientes.write(cliente.formato_escrito())
                                                    self.handleClientes.flush()
                                                    os.fsync(self.handleClientes.fileno())
                                                    print("Operacion exitosa :)")
                                                    print(cliente)
                                                    break
                                                else:
                                                    print(f"{xemail} no es un email valido :(\nDebe tener formato de email")
                                            break
                                        else:
                                            print(f"{xtelefono} no es un numero telefonico valido :(\nSolo se acepta numeros y espacios con 10 caracteres")
                                    break
                                else:
                                    print(f"{xapellido} no es un apellido valido :(\nEl formato solo acepta letras sin espacio")
                            break
                        else:
                            print(f"{xnombre} no es un nombre valido :(\nEl formato solo acepta letras sin espacio")
                    break
                else:
                    print("Este usuario ya existe :(")
            else:
                print("Formato de cedula incorrecto :(\nDebe ser numeros entre 7-10 caracteres sin espacio")

    def crear_servicio(self):
        print("Modulo crear servicio, si desea salir digite: salir()\nPor favor digite:")
        while(True):
            xcodigo = input("Codigo: ")
            if(xcodigo == "salir()"):
                break
            elif(self.validar_codigo_servicio(xcodigo)):
                test = True
                for s in self.servicios:
                    if(s.get_codigo() == xcodigo):
                        test = False
                if(test):
                    while(True):
                        xnombre = input("Nombre: ")
                        if(xnombre == "salir()"):
                            break
                        elif(self.validar_nombre(xnombre)):
                            xduracion = 60
                            while(True):
                                xcosto = input("Costo: ")
                                if(xcosto == "salir()"):
                                    break
                                else:
                                    try:
                                        xcosto = int(xcosto)
                                        while(True):
                                            xlistaEspecialistas = list(input("Cedulas de especialistas: ").split(","))
                                            if(xlistaEspecialistas == ["salir()"]):
                                                break
                                            else:
                                                test2 = True
                                                for i in xlistaEspecialistas:
                                                    if(i not in self.get_codigos(self.empleados)):
                                                        test2 = False
                                                if(test2):
                                                    servicio = Servicio(xcodigo,xnombre,xduracion,xcosto,xlistaEspecialistas)
                                                    self.servicios.append(servicio)
                                                    self.handleServicios.seek(0,io.SEEK_END)
                                                    self.handleServicios.write(servicio.formato_escrito())      
                                                    self.handleServicios.flush()  
                                                    os.fsync(self.handleServicios.fileno())
                                                    print("Operacion exitosa :)")
                                                    break
                                                else:
                                                    print("Verifique la cedula de los especialistas que ingreso")
                                        break
                                    except ValueError:
                                        print(f"{xcosto} no es un costo valido, debe ser un numero entero positivo")
                                        continue
                            break
                        else:
                            print(f"{xnombre} no es un nombre valido :(\nEl formato solo acepta letras sin espacio")
                    break
                else:
                    print("Este servicio ya existe :(")
            else:
                print(f"{xcodigo} no es un formato de código valido, solo se aceptan 3 numeros")
    
    def verificar_Servicio_sin_Reservas(self,codigo):
        test = True
        for r in self.reservas:
            if(r.get_idservicio() == codigo):
                test = False
        return test

    def borrar_servicio(self,codigo):
        temp = 0
        for s in self.servicios:
            if(codigo == s.get_codigo()):
                temp = s
                break
        if(temp != 0):
            if(self.verificar_Servicio_sin_Reservas(codigo)):
                self.servicios.remove(temp)
                self.handleServicios.seek(0)
                self.handleServicios.truncate()
                for servicio in self.servicios:
                    self.handleServicios.write(servicio.formato_escrito().rstrip("\n"))
                    self.handleServicios.write("\n")
                self.handleServicios.flush()
                os.fsync(self.handleServicios.fileno())
                print(f"Se ha eliminado el servicio de codigo: {codigo} exitosamente :)")
            else:
                print(f"El servicio de codigo: {codigo} tiene una reserva pendiente :(")
        else:
            print(f"No se ha encontrado un servicio con codigo: {codigo} :(")
        

    def run(self):
        salir = True
        while(salir):
            print("Bienvenido al spa \"Dolorcito Quito\"")
            tramite = input("Ingrese:\n1: Ingresar como cliente\n2: Ingresar como admin\n3: Salir\n--> ")
            if(tramite == "1"):
                while(True):
                    print("Modulo Cliente Presione:\n1: Acceder a su cuenta\n2: Crear una cuenta\n3: Salir")
                    tramiteCliente = input("--> ")
                    if(tramiteCliente == "1"):
                        self.acceder_cliente()
                    elif(tramiteCliente == "2"):
                        self.crear_cliente()
                    elif(tramiteCliente == "3"):
                        break
                    else:
                        print("Opcion incorrecta")
            
            elif(tramite == "2"):
                while(True):
                    print("Modulo Administracion\n1: Modulo empleados\n2: Modulo servicios\n3: Salir")
                    tramiteAdmin = input("-->")
                    if(tramiteAdmin == "1"):
                        while(True):
                            print("Modulo Administracion/Empleados\nPresione:\n1: Agregar un nuevo empleado\n2: Eliminar un empleado\n3: Salir")
                            tramiteAdminEmpleado = input("-->")
                            if(tramiteAdminEmpleado == "1"):
                                self.crear_Empleado()
                            elif(tramiteAdminEmpleado == "2"):
                                self.borrar_Empleado()
                            elif(tramiteAdminEmpleado == "3"):
                                break
                            else:
                                print("Opcion incorrecta")
                    elif(tramiteAdmin == "2"):
                        while(True):
                            print("Modulo Administacion/Servicios\nPresione:\n1: Ingresar un servicio\n2: Borrar un servicio\n3: Salir")
                            tramiteAdminServicios = input("--> ")
                            if(tramiteAdminServicios == "1"):
                                self.crear_servicio()
                            elif(tramiteAdminServicios == "2"):
                                codigo = input("Ingrese el codigo del servicio--> ")
                                self.borrar_servicio(codigo)
                            elif(tramiteAdminServicios == "3"):
                                break
                            else:
                                print("Opcion incorrecta")
                    elif(tramiteAdmin == "3"):
                        break
                    else:
                        print("Opcion incorrecta")
                    
            elif(tramite == "3"):
                print("Vuelva pronto! :)")
                break

            else:
                print("Opcion incorrecta :(")