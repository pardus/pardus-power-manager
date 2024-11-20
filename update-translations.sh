#!/bin/bash

# langs=("tr" "pt" "de")
langs=("tr" "pt")

if ! command -v xgettext &> /dev/null
then
	echo "xgettext could not be found."
	echo "you can install the package with 'apt install gettext' command on debian."
	exit
fi


echo "updating pot file"
xgettext -o po/pardus-power-manager.pot --files-from=po/files

for lang in ${langs[@]}; do
	if [[ -f po/$lang.po ]]; then
		echo "updating $lang.po"
		msgmerge -o po/$lang.po po/$lang.po po/pardus-power-manager.pot
	else
		echo "creating $lang.po"
		cp po/pardus-power-manager.pot po/$lang.po
	fi
done
