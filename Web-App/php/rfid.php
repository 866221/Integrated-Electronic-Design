<?php
$output;
//system ( "sudo -u root python3 /home/pi/Desktop/Integrated-Electronic-Design/MFRC522-python/Read.py" );
//$output = system("sudo -u root python /home/pi/test.py");

$lastline = exec("sudo -u root python3 /home/pi/Desktop/Integrated-Electronic-Design/MFRC522-python/Read.py", $output);

echo($output);


