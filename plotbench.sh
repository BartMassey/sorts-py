#!/bin/sh
# Copyright © 2018 Bart Massey
# This work is licensed under the "MIT License". Please see
# the file LICENSE in this distribution for license terms.

# Run Gnuplot to produce plots.

(
    echo set logscale xy 2
    echo set key left
    PLOT=plot
    for p in *.plot
    do
        echo $PLOT "\"${p}\""
        PLOT=replot
    done
    echo set terminal png
    echo set output '"plotbench.png"'
    echo replot
    echo set terminal wxt 0 enhanced
    echo unset output
    echo replot
    echo pause mouse
) | gnuplot
