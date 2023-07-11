SERVICE=systemd

build:
	: do nothing

install: install-common install-$(SERVICE) install-udev

install-common:
	mkdir -p $(DESTDIR)/usr/share/pardus/power-manager/
	mkdir -p $(DESTDIR)/etc/xdg/autostart/
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/libexec/
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/etc/pardus/
	mkdir -p $(DESTDIR)/usr/share/polkit-1/actions
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/status/
	cp -prfv client $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv settings $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv common $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv service $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv data $(DESTDIR)/usr/share/pardus/power-manager
	cp -prfv udev-trigger $(DESTDIR)/usr/share/pardus/power-manager
	echo "#!/bin/sh" > $(DESTDIR)/usr/libexec/pardus-power-manager
	cp -prvf data/ppm.policy $(DESTDIR)/usr/share/polkit-1/actions
	cp -pfv data/*.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/status/
	echo "exec python3 /usr/share/pardus/power-manager/service/main.py" >> $(DESTDIR)/usr/libexec/pardus-power-manager
	echo "exec python3 /usr/share/pardus/power-manager/client/cli.py \$$@" > $(DESTDIR)/usr/bin/ppm
	cp data/ppm-settings.desktop $(DESTDIR)/usr/share/applications/
	cp data/ppm-autostart.desktop $(DESTDIR)/etc/xdg/autostart/
	chmod +x $(DESTDIR)/usr/libexec/pardus-power-manager
	chmod +x $(DESTDIR)/usr/bin/ppm

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
	rm -rf $(DESTDIR)/usr/share/applications/ppm-settings.desktop
	rm -rf $(DESTDIR)/etc/xdg/autostart/data/ppm-autostart.desktop

uninstall-systemd:
	rm -f  $(DESTDIR)/lib/systemd/system/ppm.service


uninstall-openrc:
	rm -f $(DESTDIR)/etc/init.d/ppm
