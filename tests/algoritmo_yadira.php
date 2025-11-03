<?php
// Variables normales y primitivas
$bool_true = true;
$bool_false = false;
$var_null = null;
$decimal = 3.42;
$entero = 42;
$string_simple = "Hello, World!";
$string_complejo = 'PHP is fun!';
$string_anidado = "Esto es 'un ejemplo' con comillas";

// Superglobales
$_POST['username'] = "admin";
$_SESSION['id'] = 123;
$_GET['action'] = 'login';
$_COOKIE['session'] = 'abcd';
$_SERVER['REQUEST_METHOD'] = 'POST';
$_FILES['file'] = null;
$_REQUEST['q'] = 'buscar';
$_ENV['PATH'] = '/usr/bin';
$GLOBALS['globalVar'] = 100;

// Operadores lógicos
$logico1 = $_GET && false || !true xor true;
$logico2 = $_POST or $bool_true and !$bool_false;

// Comentarios
/* Comentario multilínea simple
   que debería ser ignorado por el lexer */
/** Comentario multilínea con asteriscos **/
/* Comentario multilínea anidado /* aún ignorado */ 

// Comentarios de línea
// Este es un comentario de línea
# Otro comentario de línea

?>
