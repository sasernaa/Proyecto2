from Empleado import Empleado
from Servicio import Servicio
from Cliente import Cliente
from Reserva import Reserva
from DAO import DAO

#Empleados:

listaEmpleados = []
handleEmpleado = open("Empleados.txt","a+")
handleEmpleado.seek(0)
for linea in handleEmpleado:
    constructor = list(linea.split(";"))
    listaEmpleados.append(Empleado(constructor[0],constructor[1],constructor[2],constructor[3],constructor[4],constructor[5]))

#Servicios:

listaServicios = []
handleServicio = open("Servicios.txt","a+")
handleServicio.seek(0)
for linea in handleServicio:
    constructor = list(linea.split(";"))
    listaServicios.append(Servicio(constructor[0],constructor[1],constructor[2],constructor[3],constructor[4]))

#Clientes:

listaClientes = []
handleCliente = open("Clientes.txt","a+")
handleCliente.seek(0)
for linea in handleCliente:
    constructor = list(linea.split(";"))
    listaClientes.append(Cliente(constructor[0],constructor[1],constructor[2],constructor[3],constructor[4]))

#Reservas:

listaReservas = []
handleReserva = open("Reservas.txt","a+")
handleReserva.seek(0)
for linea in handleReserva:
    constructor = list(linea.split(";"))
    listaReservas.append(Reserva(constructor[0],constructor[1],constructor[2],constructor[3],constructor[4],constructor[5],constructor[6],constructor[7].rstrip("\n")))

daoIns = DAO(listaClientes,listaServicios,listaEmpleados,handleCliente,handleEmpleado,handleServicio,handleReserva,listaReservas)

daoIns.run()