#!/usr/bin/awk -f

/^ATOM/ { 
    aname=$3
    gsub("[0-9]", "", aname)
    elem=sprintf("%2s", aname)
    $0=substr($0,1,76)elem
} 

{ print }
