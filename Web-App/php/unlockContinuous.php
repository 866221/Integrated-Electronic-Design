<!--Server-side system request to use Wiring Pi command to unlock the door continuously-->

<?php
system ( "gpio mode 0 out" );
system ( "gpio write 0 0" );