SERVICE=systemd

build:
	: do nothing

install: install-common install-$(SERVICE)

install-common:
	mkdir -p $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv client $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv service $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv udev-trigger $(DESTDIR)/usr/share/pardus/power-manager

install-none:

uninstall-none:

install-systemd:
	mkdir -p $(DESTDIR)/lib/systemd/system/
	install data/ppm.systemd \
	    $(DESTDIR)/lib/systemd/system/ppm.service

uninstall: uninstall-common uninstall-$(SERVICE)

uninstall-common:
	rm -rf $(DESTDIR)/usr/share/pardus/power-manager

uninstall-systemd:
	rm -f  $(DESTDIR)/lib/systemd/system/ppm.service
