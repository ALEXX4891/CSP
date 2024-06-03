<?php 
// sleep(1);
// $x =  "hello world";
// $json = json_encode($x);
// echo $json;
// echo '1';
// // echo $x; / так не сработает


// $cmd = 'python ' . dirname(__FILE__) . '/test2.py';
// print_r($cmd);
// $python =  exec($cmd, $out, $code);

// $output = shell_exec('python C:\OSPanel\domains\test\test_1.py h'); +

// $inputData = '[[1150],[[140,143],[150,143],[160,286],[170,286],[180,286]]]';
$inputData = file_get_contents('php://input');
// echo $inputData;

// $file = 'order.txt';
// // W = $_POST['W'];
// $W = 1150;
// // $data1 = $W;
// $data = [
//   [140, 143],
//   [150, 143],
//   [160, 286],
//   [170, 286],
//   [180, 286],
// ];


if (!$inputData) {
  die('No data');
}

$data = json_decode($inputData, true);
// print_r($data);
$arrKeys = array_keys($data);
// print_r($arrKeys);

$file = 'order.txt';
// W = $_POST['W'];
$W = $data[0][0];
// echo '$W: ';
// print_r($W);
// $data1 = $W;
$dataRes = $data[1];
// $arrDataRes = [];

// Новый человек, которого нужно добавить в файл
// $person = "Джон Смит\n";

// Записываем содержимое в файл
// с флагом FILE_APPEND, чтобы дописать содержимое в конец файла,
// и флагом LOCK_EX, чтобы никто другой не мог записывать данные в файл в то же самое время
// file_put_contents($file, $W, FILE_APPEND | LOCK_EX);
file_put_contents($file, $W . PHP_EOL);
for ($i = 0; $i < count($dataRes); $i++) {
  for ($j = 0; $j < count($dataRes[$i]); $j++) {
    if ($j%2) {
    file_put_contents($file, $dataRes[$i][$j] . PHP_EOL, FILE_APPEND);
    } else {
    file_put_contents($file, $dataRes[$i][$j] . ' ', FILE_APPEND);
    }
  } 

  // file_put_contents($file, $dataRes[$i] . PHP_EOL, FILE_APPEND);
}
// file_put_contents($file, $dataRes . PHP_EOL, FILE_APPEND);

// echo '2';


$output = shell_exec('python test_1.py'); 
// test_1.py
// echo '3';

if (!$output) {
  echo json_encode("No output");
}

echo $output;
// echo '4';

// header('Location: index.php');
