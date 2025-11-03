<?php

$numero1 = 85;
$numero2 = 90;
$numero3 = 78;
$total = 0;
$promedio = 0.0;
$contador = 3;

$suma = $numero1 + $numero2;
$resta = $numero1 - $numero3;
$multiplicacion = $numero2 * 2;
$division = $suma / $contador;
$modulo = $numero1 % 10;
$potencia = 2 ** 3;

$total = $numero1 + $numero2 + $numero3;
$promedio = $total / $contador;

echo "Calculadora de Promedios\n";
echo "========================\n\n";

if ($promedio >= 90) {
    echo "Excelente rendimiento!\n";
    $calificacion = "A";
} elseif ($promedio >= 80) {
    echo "Buen rendimiento\n";
    $calificacion = "B";
} elseif ($promedio >= 70) {
    echo "Rendimiento aceptable\n";
    $calificacion = "C";
} else {
    echo "Necesita mejorar\n";
    $calificacion = "F";
}

$es_mayor = $numero1 > $numero2;
$es_menor = $numero1 < $numero3;
$es_igual = $numero1 == 85;
$es_identico = $numero1 === 85;
$es_diferente = $numero1 != $numero2;
$mayor_o_igual = $promedio >= 80;
$menor_o_igual = $promedio <= 100;

echo "\nEstadísticas:\n";
echo "Total: " . $total . "\n";
echo "Promedio: " . $promedio . "\n";
echo "Calificación: " . $calificacion . "\n";

echo "\nDesglose de notas:\n";
for ($i = 1; $i <= $contador; $i++) {
    echo "Nota " . $i . ": ";
    
    switch ($i) {
        case 1:
            echo $numero1 . "\n";
            break;
        case 2:
            echo $numero2 . "\n";
            break;
        case 3:
            echo $numero3 . "\n";
            break;
        default:
            echo "N/A\n";
    }
}

$intentos = 0;
while ($intentos < 3) {
    $intentos = $intentos + 1;
    echo "Intento " . $intentos . "\n";
    
    if ($intentos == 2) {
        continue;
    }
}

$notas = array($numero1, $numero2, $numero3);
$estudiante = array("nombre" => "Juan", "edad" => 20);

define("NOTA_MINIMA", 60);
define("NOTA_MAXIMA", 100);

if ($promedio > NOTA_MINIMA && $promedio <= NOTA_MAXIMA) {
    echo "\nEl promedio está en el rango válido\n";
}

$resultado1 = (10 + 5) * 2;
$resultado2 = 10 + (5 * 2);
$resultado3 = ((15 - 5) / 2) + 3;

$aprobado = true;
$reprobado = false;
$sin_calificar = null;

function calcular_promedio($n1, $n2, $n3) {
    $suma_total = $n1 + $n2 + $n3;
    return $suma_total / 3;
}

class Estudiante {
    public $nombre;
    public $edad;
    private $promedio;
    
    function __construct($n, $e) {
        $this->nombre = $n;
        $this->edad = $e;
    }
}

$est1 = new Estudiante("María", 21);

echo "\n¡Análisis completado!\n";

?>