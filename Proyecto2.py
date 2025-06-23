from Empleado import Empleado
from Servicio import Servicio
from DAO import DAO

#Empleados:

persona1 = Empleado("111","Elva","Giro","3141516000","ElvaGiro@gmail.com",["001","004"])
persona2 = Empleado("222","Elba","Jito","3139483000","ElbaJito@gmail.com",["002","003"])
persona3 = Empleado("333","Alma","Marcela","3138423940","AlmaMarcela@gmail.com",["001","002"])
persona4 = Empleado("444","Elpa","Laso","3134516000","ElpaLaso@gmail.com",["004","003"])

listaEmpleados = [persona1,persona2,persona3,persona4]

#Servicios:

servicio1 = Servicio("001","Masaje",20,65000,[persona1,persona3])
servicio2 = Servicio("002","Masaje con final feliz",60,500000,[persona2,persona3])
servicio3 = Servicio("003","Terapia",30,95000,[persona2,persona4])
servicio4 = Servicio("004","Hidroterapia",45,145000,[persona1,persona4])

listaServicios = [servicio1,servicio2,servicio3,servicio4]

#Clientes:

listaClientes = []

daoIns = DAO(listaClientes,listaServicios,listaEmpleados)

daoIns.run()