%global ssp simplesamlphp
%global theme_module sspopenmooc
%global theme_source sspopenmooc-v0.1.0

Name: openmooc-idp-httpd
Version: 0.1.0
Release: 1%{?dist}
Summary: OpenMOOC IdP: simplesamlphp + userregistration + sspopenmooc

Group: Applications/Internet
License: LGPLv2
URL: https://github.com/OpenMOOC/sspopenmooc/
Source0: https://github.com/OpenMOOC/sspopenmooc/archive/sspopenmooc-v%{version}.tar.gz
Source1: openmooc-idp-config-v%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?el6}
Requires: simplesamlphp
Requires: httpd
Requires: mod_ssl
Requires: php-mcrypt
Requires: php-mbstring
Requires: zlib
Requires: wget
Requires: ntp
Requires: simplesamlphp-userregistration
# simplesamlphp-userregistration dependences for OpenMOOC
Requires: mongodb
Requires: php-pecl-mongo

%endif 

BuildArch: noarch
 
%description
The IdP (Identity Provider) is one of the OpenMOOC platform components.
Is based on SimpleSAMLphp and some extra modules, incluiding a default
openmooc theme.

%prep
%setup -q -b 0 -n %theme_source
%setup -q -b 1 -n openmooc-idp-config-v0.1.0 -c

%build

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{theme_module}
ls -la
cp -pr %theme_source/* ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{theme_module}
ls -la ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{theme_module}

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/metarefresh
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/cron/
touch ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/metarefresh/enable
touch ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/cron/enable

mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{ssp}/metadata/moocng
cp saml20-idp-hosted.php ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{ssp}/metadata/saml20-idp-hosted.php

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/
cp %theme_source/config-templates/module_sspopenmooc.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/module_sspopenmooc.php
cp extended_config.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/extended_config.php
cp config-metarefresh.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/config-metarefresh.php
cp config-sanitycheck.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/config-sanitycheck.php
cp module_cron.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/module_cron.php

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m644 idp.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)

%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/module_sspopenmooc.php
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/extended_config.php
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/config-metarefresh.php
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/config-sanitycheck.php
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/module_cron.php
%attr(640,root,simplesamlphp) %config(noreplace) %{_localstatedir}/lib/%{ssp}/metadata/saml20-idp-hosted.php

%attr(640,root,simplesamlphp) %{_localstatedir}/lib/%{ssp}/metadata/moocng

%attr(644,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/httpd/conf.d/idp.conf

%attr(640,root,simplesamlphp) %{_libdir}/%{ssp}/modules/cron/enable
%attr(640,root,simplesamlphp) %{_libdir}/%{ssp}/modules/metarefresh/enable

%{_libdir}/%{ssp}/modules/%{theme_module}

%changelog
* Mon Jul 10 2013 <smartin@yaco.es> - 0.1.0-1
- initial package
