SERVICE=systemd

build:
	: do nothing

install: install-common install-$(SERVICE) install-udev

install-common:
	mkdir -p $(DESTDIR)/usr/share/pardus/power-manager
	mkdir -p $(DESTDIR)/usr/libexec/
	cp -prfv client $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv common $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv service $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv udev-trigger $(DESTDIR)/usr/share/pardus/power-manager
	echo "#!/bin/sh" > $(DESTDIR)/usr/libexec/pardus-power-manager
	echo "exec python3 /usr/share/pardus/power-manager/service/main.py" >> $(DESTDIR)/usr/libexec/pardus-power-manager
	chmod +x $(DESTDIR)/usr/libexec/pardus-power-manager

install-none:

uninstall-none:

install-udev:
	mkdir -p $(DESTDIR)/lib/udev/rules.d/ $(DESTDIR)/usr/libexec/
	install -m644 udev-trigger/ppm.rule $(DESTDIR)/lib/udev/rules.d/99-ppm.rules
	echo "#!/bin/sh" > $(DESTDIR)/usr/libexec/ppm-trigger
	echo "exec python3 /usr/share/pardus/power-manager/udev-trigger/main.py" >> $(DESTDIR)/usr/libexec/ppm-trigger
	chmod +x $(DESTDIR)/usr/libexec/ppm-trigger

install-systemd:
	mkdir -p $(DESTDIR)/lib/systemd/system/
	install data/ppm.systemd \
	    $(DESTDIR)/lib/systemd/system/ppm.service

install-openrc:
	mkdir --p $(DESTDIR)/etc/init.d/
	install data/ppm.openrc $(DESTDIR)/etc/init.d/ppm

uninstall: uninstall-common uninstall-$(SERVICE) uninstall-udev

uninstall-udev:
	rm -f $(DESTDIR)/lib/udev/rules.d/99-ppm.rules
	rm -f $(DESTDIR)/usr/libexec/ppm-trigger

uninstall-common:
	rm -rf $(DESTDIR)/usr/share/pardus/power-manager
	rm -f $(DESTDIR)/usr/libexec/pardus-power-manager

uninstall-systemd:
	rm -f  $(DESTDIR)/lib/systemd/system/ppm.service


uninstall-openrc:
	rm -f $(DESTDIR)/etc/init.d/ppm
