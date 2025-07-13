# Proyecto de curso – Tercera Entrega – 10%
## Fundamentos de Programación
## Título: Aplicación de Administración de servicios
## FECHA ENTREGA: 16 JULIO
## FECHA DE SUSTENTACION: 18 JULIO
El objetivo de este proyecto es desarrollar un sistema utilizando el lenguaje de programación Python. Este sistema debe permitir realizar reservas de servicios prestados, permitiendo seleccionar el servicio deseado, el especialista/trabajador disponible, la agenda disponible del especialista seleccionado y el costo del servicio.

Especialista / Trabajador: Debe tener la información de cedula, nombre, apellido, teléfono y email.
Servicio: Debe tener el nombre del servicio, duración del servicio, el costo y la lista de los especialistas que lo ofrecen.
Reserva: Debe tener el nombre del cliente, el especialista asignado, y la fecha y hora de la reserva. No se puede reservar el mismo servicio con el mismo especialista en la misma fecha y hora.

## Funcionalidades del Sistema:
1. Ingresar/Editar/Cancelar reserva de servicio.
2. Consultar reservas.
3. Ingresar/Editar/Borrar especialista/ trabajador (no se puede borrar un trabajador si tiene reservas asociadas)
4. Ingresar/Editar/Borrar Servicios (no se puede borrar servicios si tienen reservas asociadas o especialistas asociados)
5. Guardar archivo estructurado (JSON, CSV, XLS, XML, etc) con la información de: reservas, servicios, especialistas, clientes.
6. Cargar información desde el archivo guardado.
7. Para todas las funciones debe ser posible cancelar la operación.
8. Adicionar todas las condiciones de formatos de datos:

1. Se debe verificar el ingreso de fechas correctas y en caso de ingresar una fecha incorrecta, el programa debe de reintentar el ingreso de la fecha.
2. Se debe verificar el ingreso de correos electrónicos correctos (xxx@yyy.com).
3. Se debe verificar el ingreso de teléfonos correctos. No debe permitir ingreso de letras ni caracteres especiales. Puede permitir espacios.
4. Se debe verificar el ingreso de cedulas correctas. No debe permitir ingreso de letras ni caracteres especiales. No debe permitir espacios
5. Se debe verificar el ingreso correcto de nombres y apellidos (no debe permitir números ni caracteres extraños)
## Ejemplo:
Se implementará el sistema de servicios a un taller de mecánica de motos.
Se ofrecen los servicios de: 
1. Mantenimiento de frenos. Los realiza Juan y Francisco vale 80.000 pesos. Dura 1h
2. Revisión de emisiones. Lo realiza Juliana vale 100.000 pesos. Dura 30min
3. Cambio de aceite. Lo realiza Rigo y vale 120.000 pesos. Dura 30min
Para este caso, se asumen los precios fijos sin importar el tamaño de la moto.
El sistema requiere persistencia de datos, es decir, requiere que la información sea guardada en archivos de forma permanente.
Entrega:
La entrega se realiza mediante un único archivo comprimido ZIP nombrado como “Integrante1_Integrante2_Integrante3.zip”. donde quedarán los archivos .py utilizados por su programa.
De ser necesario el uso de librerías externas, debe incluir el archivo requirements.txt
El archivo se envía al correo electrónico del profesor: 
## LAAGUILAL@UNAL.EDU.CO 
