#!/bin/bash
xgettext -o pardus-power-manager.pot --from-code="utf-8" src/data/MainWindow.ui `find src -type f -iname "*.py"`
for file in `ls po/*.po`; do
    msgmerge $file pardus-power-manager.pot -o $file.new
    echo POT: $file
    rm -f $file
    mv $file.new $file
done
