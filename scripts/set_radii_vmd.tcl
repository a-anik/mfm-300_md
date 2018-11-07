set sel [atomselect 0 all]
set infile [open "../top/a.rad"  r]
set data_lines [read -nonewline $infile]
set rlist0 [lreplace [split $data_lines \n] 0 1]
set rlist {}
foreach x $rlist0 { lappend rlist [expr $x*10+0.0] }
$sel set radius $rlist
