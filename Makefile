SERVICE=systemd

build:
	: do nothing

install: install-common install-$(SERVICE)

install-common:
	mkdir -p $(DESTDIR)/usr/share/pardus/power-manager
	mkdir -p $(DESTDIR)/usr/libexec/
	cp -prfv client $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv common $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv service $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv udev-trigger $(DESTDIR)/usr/share/pardus/power-manager
	install data/ppm-service.sh $(DESTDIR)/usr/libexec/pardus-power-manager

install-none:

uninstall-none:

install-udev:
	mkdir -p $(DESTDIR)/lib/udev/rules.d/
	install -m644 udev-trigger/ppm.rule $(DESTDIR)/lib/udev/rules.d/99-ppm.rules
	echo "#!/bin/sh" > $(DESTDIR)/usr/libexec/ppm-trigger
	echo "exec python3 /usr/share/pardus/ppm/udev-trigger/main.py" >> $(DESTDIR)/usr/libexec/ppm-trigger

install-systemd:
	mkdir -p $(DESTDIR)/lib/systemd/system/
	install data/ppm.systemd \
	    $(DESTDIR)/lib/systemd/system/ppm.service

uninstall: uninstall-common uninstall-$(SERVICE)

uninstall-common:
	rm -rf $(DESTDIR)/usr/share/pardus/power-manager

uninstall-systemd:
	rm -f  $(DESTDIR)/lib/systemd/system/ppm.service
