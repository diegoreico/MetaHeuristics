#!/usr/bin/env bash
time=$(time ( python3 main.py distancias_100_2016.txt aleatorios_ls_2016.txt ) 2>&1 1> aqui )
echo $time