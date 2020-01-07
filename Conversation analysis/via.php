<?php

$post = $_POST['text'];
$file = "text.txt";
file_put_contents($file, $post, FILE_APPEND);

//あとでtestに戻す
$command='''フルパスでanalysis.pyを指定する。''';
exec($command,$output, $return_var);

echo json_encode($output, JSON_UNESCAPED_UNICODE);
