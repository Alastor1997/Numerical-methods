<?php
header('Content-Type: text/html; charset=utf-8');
$field = isset($_GET['field'])? $_GET['field'] : '';
$sort = isset($_GET['sort'])? $_GET['sort'] : 'asc';

$link = mysql_connect("localhost", "student","student") or die('Не удалось соединиться: ' . mysql_error());
mysql_select_db("student");
$q = "SELECT TableRus.id, TableRus.datet,TableRus.had, AvtorRus.fio, RubricaRus.NameRubric,TableRus.anons,TableRus.body FROM TableRus INNER JOIN AvtorRus ON(TableRus.avtor = AvtorRus.id) INNER JOIN RubricaRus ON(TableRus.rubric = RubricaRus.id) ";
if (!empty($field)) {
  $q .= " ORDER BY $field $sort";
}
$result = mysql_query($q) or die('Запрос не удался: ' . mysql_error());;
//$rows = 2; // количество строк, tr
//$cols = 7; // количество столбцов, td

echo '<table border="5" width="1900">';

echo '<tr>';
for ($i = 0, $L = mysql_num_fields($result); $i < $L; $i++) {
    $field = mysql_fetch_field($result, $i);
    $sort_rev = $sort=='asc' ? 'desc': 'asc';
    echo "<th><a href='?field={$field->name}&sort=$sort_rev'>", htmlspecialchars($field? $field->name : "[$i]"), '</a></th>';
    
}
echo '</tr>';

while ($line = mysql_fetch_array($result, MYSQL_ASSOC)) {
echo "\t<tr>\n";
foreach ($line as $col_value) {
echo "<td>$col_value</td>\n";
}
echo "</tr>\n";
}
echo "</table>\n";
// Освобождаем память от результата
mysql_free_result($result);
// Закрываем соединение
mysql_close($link);
?> 
