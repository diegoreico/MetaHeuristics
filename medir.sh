#!/usr/bin/env bash
time=$(time ( ./main.py distancias_sa_100_2016.txt aleatorios_sa_2016_caso1.txt ) 2>&1 1> aqui )
echo $time
