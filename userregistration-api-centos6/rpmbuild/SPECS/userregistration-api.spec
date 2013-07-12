%global ssp simplesamlphp
%global module_name userregistrationApi
%global module_source userregistrationApi-userregistration-apiv0.1.0

Name: userregistration-api
Version: 0.1.0
Release: 1%{?dist}
Summary: An extension for the userregistration module that implements an API

Group: Applications/Internet
License: LGPLv2
URL: https://github.com/OpenMOOC/userregistrationApi
Source0: https://github.com/OpenMOOC/userregistrationApi/archive/userregistration-apiv%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?el6}
Requires: userregistration
%endif 

BuildArch: noarch
 
%description
An extension for the userregistration module that implements an API.
Enable an API REST to allow 3rd party components to update some values of the
users from the userregistration data source.

The userregistration is a module of simpleSAMLphp linked with a ldap authsource 
to make actions over user accounts:
* Register user, password reset, email change, etc
* Has an admin panel to manage masive user accounts.
This module is an element of the OpenMOOC project.

%prep
%setup -q -b 0 -n %module_source

%post
echo "The userregistrationApi module was sucessfully installed and was enabled, please config the %{_sysconfdir}/%{ssp}/config/module_userregistration-api.php file"

%build

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config
cp config-templates/module_userregistration-api.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{ssp}/config/module_userregistration-api.php

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{module_name}
cp -pr * ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{module_name}
touch ${RPM_BUILD_ROOT}%{_libdir}/%{ssp}/modules/%{module_name}/enable

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(644,root,root,755)

%dir %{_sysconfdir}/%{ssp}/config
%attr(640,root,simplesamlphp) %config(noreplace) %{_sysconfdir}/%{ssp}/config/module_userregistration-api.php

%{_libdir}/%{ssp}/modules/%{module_name}

%doc docs/ README.md

%changelog
* Mon Jul 12 2013 <smartin@yaco.es> - 0.1.0-1
- initial package
