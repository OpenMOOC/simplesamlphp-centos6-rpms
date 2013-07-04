%global ssp simplesamlphp
%global module_name userregistration

Name: userregistration
Version: 0.1.0
Release: 1%{?dist}
Summary: Module of simpleSAMLphp that allow manage users of a ldap authsource 

Group: Applications/Internet
License: LGPLv2
URL: https://github.com/OpenMOOC/userregistration
Source0: https://github.com/OpenMOOC/userregistration/archive/userregistration-v%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?el6}
Requires: openldap
Requires: openldap-clients
Requires: openldap-servers
Requires: phpldapadmin
Requires: php-ldap
Requires: simplesamlphp
%endif 

BuildArch: noarch
 
%description
Module of simpleSAMLphp linked with a ldap authsource to make actions over user
accounts:
* Register user, password reset, email change, etc
* Has an admin panel to manage masive user accounts.
This module is an element of the OpenMOOC project.

%prep
%setup -q -b 0 -n userregistration-0.1.0

%build

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config
cp config-templates/module_userregistration.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/module_userregistration.php

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{module_name}
cp -pr * ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{module_name}

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(644,root,root,755)

%dir %{_sysconfdir}/%{ssp}/config
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/module_userregistration.php

%{_libdir}/%{ssp}/modules/%{module_name}

%doc doc/ README.txt LICENSE.txt

%changelog
* Mon Jul 3 2013 <smartin@yaco.es> - 0.1.0-1
- initial package