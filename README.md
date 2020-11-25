# MeMyself
MeMyself es un lenguaje de programacion orientado a jóvenes que buscan aprender los fundamentos de la programación gráfica. Este lenguaje es capaz de manejar Estatutos, Expresiones aritmeticas, Modulos, Arreglos, Variables y Output Grafico.

# Antes de empezar
Para poder correr el lenguaje es necesario contar con lo siguiente

* Python con las librerias ply y tkinter (tkinter ya viene instalado con las versiones mas recientes de python)
* Todos los archivos en este repo <br/>
Si se tiene dudas con la ejecucion se puede ver el siguiente video<br/>
https://drive.google.com/file/d/1wVqPWSu562UCBdzNhLaRbMVBsFPWWD_-/view?usp=sharing

# General 
La estructura que sigue MeMyself es la siguiente:
```
Program Nombre_prog;
var tipo :lista_ids;
    <tipo :lista_ids;> ....

module <tipo>  <id> ( <tipo> <id>, .... );
var tipo :lista_ids;
    <tipo :lista_ids;> ....
{
    <Estatutos>
}
module...

main(){
    <Estatutos>
}
```

## Ejemplo de ejecución
Crea un archivo de txt y teclea algo parecido 
```
Program UC1;

main(){
    write("Hello world");
}
```
Para correr el archivo corre el siguiente comando en la terminal
```
py MeMyself.py <Nombre o dirección de tu archivo>
```

## Declaración de variables

Una variable puede ser del tipo int, float o char. Las variables pueden ser globales, si fueron declaradas al principio del programa, o locales son declaradas adentro de un modulo.
Ej.
```
Program TC4;
var int: num , i; \\Variables globales

module int fact (int j);
var int : x; \\Variables locales
```

## Arreglos
Al momento de declarar funciones se pueden declarar arreglos de 1 o 2 dimensiones, la manera de declararlos es la siguiente:
```
var int: Arreglo[20];
```
Los indices del arreglo empiezan del 0 al tamaño declarado menos 1 (19)

## Declaración de módulos (Funciones)

Se pueden declarar modulos de tipo int, float, char o void. Si el tipo del modulo es int, float o void es obligatorio tener un return al final del modulo. Si es void no se ocupa.
```
module int ejemplo(int x);
var int : i;
{
    return(5);
}
```

## Main
Todo programa debe tener un main(),es lo que el programa corre primero y es donde sucede la ejecucion principal. Cualquier operacion o funcion que se quiera correr debe de ser invocado en el main.
Ej:
```
main(){
    write("Hello world");
}
```

## Asignaciones
A todas las variables se les puede asignar un valor que coincida con el tipo con el que fueron declarados. Si la variable es un arreglo se ocupa especificar el indice, el cual debe estar entre las dimensiones establecidas cuando se declaro.
```
Program TC1;
var int : num, Arreglo[20];

main(){
    num = 0;
    Arreglo[0] = 1;
}
```
## Llamadas
Cualquier modulo que ha sido declarada previamente se puede llamar. Si el modulo tiene un return se puede asignar un modulo a una variable. Al momento de llamar al modulo es necesario que contenga el mismo numero de parametros y el mismo tipo del parametro.

```
Program Llamadas;
var int : resultado;

module void ejemplo(){
    write("Hola");
}

module int suma(int x, int y){
    return(x+y);
}
main(){
    ejemplo();
    resultado = suma(1+2);
}
```

## Write
Write te permite imprimir cualquier string o variable en la terminal. Si es un string es necesario que este entre "". Se puede tener uno o mas parametros al momento de llamar a write.
```
write("Hola ", x, " ", suma(1+2));
```

## Read
Read permite al usuario ingresar por medio de la terminal un valor para una variable.       El valor ocupa ser el mismo que el de la variable.
Read no funciona para arreglos. Se ocupar iniciar una variable leerla y luego asignarla.
```
read(x);
```
## Condicionales
If y else son los condicionales permitidos por el lenguaje. La expresion ocupa ser bool.
 ```
if(j == 1) then 
{   
    return (j);
}
else
{
    return (j * fact(j-1));
}
```

## Ciclos
### While
Al igual que con el if, la expresión del while ocupa ser bool.
```
num = 0;
while(num < 1) do{
    write("Introduce un número mayor a 0");
    read(num);
}
```
### From-to
El from to es de la siguiente forma:
```
from i=0 to num do{
        write(fib(i));
}
```
* La variable i ocupa haber sido declarada antes y ser int, num ocupa ser un numero mayor a i y de tipo int.
* La variable i se va a incrementar 1 cada vuelta del from hasta que sea igual que num.

# Funciones especiales
MeMyself es capaz de tener un output grafico gracias a las funciones
* Line, Point, Circle, Arc, Penup, Pendown, Color, Size y Clear.

## Size
Antes de poder utilizar las otras funciones es necesario usar esta.<br/> 
Size especifica el tamaño del canvas en pixeles (ancho, altura).
```
Size(720,480);
```
## Color
Esta funcion especifica el color de relleno del canvas, estos colores pueden ser.
* "white", "black", "red", "green", "blue", "cyan", "yellow", o "magenta".
```
Color("red");
```
## Clear
Clear limpia todos los dibujos del canvas.
```
Clear();
```

## Pendown
Pendown especifica en que coordenadas del canvas se va a dibujar (x,y). <br/> 
Si esta funcion no se llama las coordenadas default seran 0,0. <br/>
Cada vez que se quiera cambiar las coordenadas se ocupa llamar esta funcion.
```
Pendown(300,200);
```
## Penup
Penup se llama cuando se quiere desplegar la ventana del canvas. <br/>
```
Penup();
```
## Line
Line dibuja una línea en el canvas. <br/> 
La linea se va a dibujar desde las coordenadas establecidas por **Pendown** hasta las coordenadas pasadas en los parametros. <br/>
Los parámetros son Line(x,y).
```
Line(500, 200);
```
## Point
Point dibuja un punto en el canvas. <br/> 
El punto se va a dibujar en las coordenadas establecidas por **Pendown**. <br/>
Se ocupa especificar el tamaño del punto este puede ser entre 0 y 10. <br/>
Se le puede especificar el color de relleno a Point de manera opcional.
```
Point(5,"red"); // "red" es opcional
```

## Circle
Circle dibuja un circulo en el canvas. <br/> 
El circulo se va a dibujar en las coordenadas establecidas por **Pendown**. <br/>
Se ocupa especificar el tamaño del circulo este puede ser entre 0 y 10. <br/>
Se le puede especificar el color de relleno a Circle de manera opcional.
```
Circle(4,"blue"); // "blue" es opcional
```

## Arc
Arc dibuja un arco en el canvas. <br/> 
El circulo se va a dibujar en las coordenadas establecidas por **Pendown**. <br/>
Arc toma 2 parámetros y un color opcional </br>
El primer parametro es el tamaño del arco este puede ser entre 0 y 10.<br/>
El segundo parametro es el angulo del arco este puede estar entre 0 y 360<br/>
Se le puede especificar el color de relleno a Circle de manera opcional.
```
Arc(6,90"yellow"); // "yellow" es opcional
```
