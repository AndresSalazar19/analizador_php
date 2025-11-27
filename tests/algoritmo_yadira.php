<?php
// Variables normales y primitivas
$bool_true = true;
$bool_false = false;
$var_null = null;
$decimal = 3.42;
$entero = 42;
$negativo = -12;
$grande = 99999;
$cadena_doble = "Hola, PHP!";
$cadena_simple = 'Esto es una cadena simple';
$cadena_mixta = "Texto con 'comillas simples' dentro";
$cadena_escapada = "Salto de línea\n y tabulación\t";
$cadena_vacia = "";
$texto1 = "Texto con variables: $entero, $decimal, $bool_true";
$texto2 = 'Texto estático sin variables: $entero y $decimal';
$texto3 = "Líneas múltiples
pueden ser concatenadas
sin problema";

echo $texto3;

echo $cadena_doble;
echo "Valor entero: $entero\n";
echo 'Valor decimal: ' . $decimal . "\n";
define("PI", 3.14);

function ejemploLocal() {
    $local = 5; // x no existe
}

function hola($nombre) {
    return "Hola " . $nombre;
}

echo hola("Yadira");
echo (4+5);
// Superglobales
$_POST['username'] = "admin";
$_POST['clave'] = "1234";
$_SESSION['id'] = 123;
$_GET['action'] = 'login';
$_COOKIE['session'] = 'abcd';
$_SERVER['REQUEST_METHOD'] = 'POST';
$_FILES['file'] = null;
$_REQUEST['q'] = 'buscar';
$_ENV['PATH'] = '/usr/bin';
$GLOBALS['globalVar'] = 100;

echo $_POST['usuario'];
echo $_GET['accion'];


// Operadores lógicos
$logico1 = $_GET && false || !true xor true;
$logico2 = $_POST or $bool_true and !$bool_false;
$logico3 = true && false;
$logico4 = $bool_true and !$bool_false;
$logico5 = $bool_false or $bool_true;
$logico6 = $bool_true xor $bool_false;
$logico7 =  !($logico1 || $logico2) && $logico3;

// Comentarios
/* Comentario multilínea simple
   que debería ser ignorado por el lexer */
/** Comentario multilínea con asteriscos **/
/* Comentario multilínea anidado /* aún ignorado */ 

// Comentarios de línea
// Este es un comentario de línea
# Otro comentario de línea

if ($logico5) {
    echo "Expresión lógica verdadera\n";
} else {
    echo "Expresión lógica falsa\n";
}

if ($_GET && $_POST && $_SESSION) {
    echo "Se detectaron varias superglobales\n";
}

if ($_FILES || $_REQUEST) {
    echo "Archivos o peticiones detectadas\n";
}

if (!$_ENV) {
    echo "Variable de entorno vacía o no definida\n";
}

if ($logico7) {
    echo "La condición final se cumple\n";
} else {
    echo "Condición no cumplida\n";
}

// Array Asociativos
$estudiante = [
    "nombre" => "Yadira",
    "edad" => 21,
    "carrera" => "Computación",
    "notas" => [10, 9.5, 8.7]
];

$materias = [
    "programacion" => "Aprobada",
    "matematicas" => "Aprobada",
    "ingles" => "En curso"
];

echo "Nombre: " . $estudiante["nombre"] . "\n";

// Bucle While
$contador = 0;
while ($contador < 3) {
    echo "Iteración WHILE número: $contador\n";
    $contador++;
}

// Bucle Foreach
foreach ($materias as $materia => $estado) {
    echo "Materia: $materia - Estado: $estado\n";
}

// Funcion sin retorno
function mostrarSaludo($nombre) {
    echo "Hola, $nombre!\n";
}

mostrarSaludo("Yadira");
mostrarSaludo("Mundo");


// Asignacion por referencia
$a = 10;
$b =& $a;     // b hace referencia a a
$b = 25;

echo "Valor de a después de referencia: $a\n"; // imprime 25

// Mezclando operadores lógicos con superglobales
$verificar = isset($_POST['usuario']) && $_SERVER['REQUEST_METHOD'] == "POST" || !$bool_false;
$comparar = $_COOKIE['tema'] == "oscuro" xor $_GET['accion'] == "iniciar";

// Combinación de tipos y operadores lógicos
$ejemplo1 = $_POST && $_SESSION || $_GET;
$ejemplo2 = $bool_true && ($_POST['usuario'] or $_POST['clave']);
$ejemplo3 = !$bool_false && ($_ENV['PATH'] != null);
$ejemplo4 = $_COOKIE && $_FILES && $bool_true;
$ejemplo5 = ($_REQUEST or $_SERVER) and !$bool_false;

echo "Fin de análisis del algoritmo de Yadira";


// Ingreso por teclado CLI
$nombre_usuario = "";
$nombre_usuario = readline("Ingrese su nombre: ");

if ($nombre_usuario != "") {
    echo "Bienvenido, $nombre_usuario!\n";
} else {
    echo "No se ingresó ningún nombre.\n";
}

echo "Fin de análisis del algoritmo de Yadira\n";
?>
