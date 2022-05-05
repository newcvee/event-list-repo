## Pantalla de añadir evento 200.PRE-01

ruta de pantalla : /events/add
src/pages/events/event-add/EventAddPage.vue

POST/api/events

BODY {
"id": ,
"name": ,
"description": ,
"date": ,
"time": ,
"completed":
}

response 200 OK

## Pantalla de mostrar detalles de evento 300.PRE-01

ruta de pantalla :events/:idDelEvento
src/pages/event-details/EventDetailPage.vue

GET/api/events/:id_del_evento

BODY {
"id": ,
"name": ,
"description": ,
"date": ,
"time": ,
"completed":
}

response 200 OK

## Tabla BD users

{
"id": ,
"user_name":
},

## ID'S ALEATORIAS

Para crear ids aleatorias utilizamos la librería UUID V4 en Vue.
Se utiliza con la función uuidv4()

## FECHAS

Para utilizar las fechas utilizamos la librería datetime.
from datetime import \*
Para detectar el dia actual usamos datetime.today()
