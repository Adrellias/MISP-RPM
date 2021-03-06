Name:	    misp
Version:	2.4.88
Release:	4%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source0:	fake-tgz.tgz
Source1:    misp.conf
Source2:    misp-httpd.pp
Source3:    misp-bash.pp
Source4:    misp-ps.pp
Source5:    misp-workers.service
Source6:    start-misp-workers.sh

BuildArch:      noarch
BuildRequires:  git, python-devel, python-pip, libxslt-devel, zlib-devel
BuildRequires:  php > 7.0
BuildRequires:  python-lxml, python-dateutil, python-six, curl
BuildRequires:  python-setuptools, wget
BuildRequires:  php-pear-Crypt_GPG
Requires:	    httpd, redis, libxslt, zlib
Requires:       php > 7.0
Requires:       python-lxml, python-dateutil, python-six
Requires:	    python-cybox, python-stix, php-redis
Requires:       php-pear-Crypt_GPG
Requires:       python-magic, python-pydeep, python-pymisp, python34-pymisp
Requires:       lief-python, python-mixbox

%description
MISP - malware information sharing platform & threat sharing

%prep
%setup -q -n fake-tgz

%build

%install
mkdir -p $RPM_BUILD_ROOT/var/www
git clone https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP
cd $RPM_BUILD_ROOT/var/www/MISP
git checkout tags/v%{version}
git config core.filemode false
git submodule init
git submodule update
wget https://getcomposer.org/download/1.2.1/composer.phar -O composer.phar
cd $RPM_BUILD_ROOT/var/www/MISP/app
php composer.phar require kamisama/cake-resque:4.1.2
php composer.phar config vendor-dir Vendor
php composer.phar install
mkdir -p $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config
cp -fa $RPM_BUILD_ROOT/var/www/MISP/INSTALL/setup/config.php $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config/config.php
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/local/sbin
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT/usr/local/sbin

%files
%defattr(-,apache,apache,-)
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
/var/www/MISP
%config(noreplace) /etc/httpd/conf.d/misp.conf
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
%defattr(-,root,root,-)
/usr/local/sbin/start-misp-workers.sh

%post
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/terms
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/scripts/tmp
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Plugin/CakeResque/tmp
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/tmp
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/orgs
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/custom
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_unified 1
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp'
restorecon -v '/var/www/MISP/app/tmp'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/'
restorecon -v '/var/www/MISP/app/tmp/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/logs/'
restorecon -v '/var/www/MISP/app/tmp/logs/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache'
restorecon -v '/var/www/MISP/app/tmp/cache'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/'
restorecon -v '/var/www/MISP/app/tmp/cache/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/feeds'
restorecon -v '/var/www/MISP/app/tmp/cache/feeds'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/models'
restorecon -v '/var/www/MISP/app/tmp/cache/models'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/persistent'
restorecon -v '/var/www/MISP/app/tmp/cache/persistent'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/views'
restorecon -v '/var/www/MISP/app/tmp/cache/views'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Config/config.php'
restorecon -v '/var/www/MISP/app/Config/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
restorecon -v '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Plugin/CakeResque/Config/config.default.php'
restorecon -v '/var/www/MISP/app/Plugin/CakeResque/Config/config.php'
semodule -i /usr/share/MISP/policy/selinux/misp-httpd.pp
semodule -i /usr/share/MISP/policy/selinux/misp-bash.pp
semodule -i /usr/share/MISP/policy/selinux/misp-ps.pp

%changelog
* Sat Mar 3 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch - 2.4.88-4
- updated to MISP version 2.4.88
- added systemctl unit for misp-workers

* Tue Jan 16 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.8.86
- updated to MISP version 2.4.86

* Thu Jan 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.85
- updated to MISP version 2.4.85
- added misp-*.pp selinux policies

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muelemann@switch.ch>
- fixes and optimizations after install tests

* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- adapted to use the php-pear RPMs

* Wed Nov 09 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- first version for centos
