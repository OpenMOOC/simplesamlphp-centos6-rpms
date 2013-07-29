# Remaining issues:
#
# [U] = should be done at/by upstream simpleSAMLphp
#
# - [U] how to enable modules? writing an "enable" file in 
#   /usr/share/simplesamlphp/modules/<NAME> is NOT a solution, enable them 
#   through some config file in /etc/simplesamlphp IS.
#   PATCH provided: http://code.google.com/p/simplesamlphp/issues/detail?id=475
# - [U] we really cannot set a default pw from the post section! We should 
#   probably patch and upstream a simpleSAMLphp fail (or warning in web 
#   interface, like when using HTTP instead of HTTPS if the default salt value 
#   is still there. Other options: use Debian approach with separate secrets
#   PATCH provided: http://code.google.com/p/simplesamlphp/issues/detail?id=476
# - the default certs are probably a bad idea! maybe not install them? of fail
#   if they were not replaced? Maybe we can generate some certificates, like
#   is done for the dovecot IMAP server package...
# - certs need to be moved to /etc/pki/simplesamlphp  (like e.g. dovecot case)
# - deal with SELinux (try to enable metarefresh to make sure it actually 
#   works and write stuff to /var/lib/simplesamlphp/metadata) also fix default
#   metarefresh default location to write metadata perhaps...
# - deal with the logfile in /var/log/simplesamlphp
# - get rid of the included copy of OpenID php and libxmlsec PHP stuff in the 
#   lib/ directory, package them separately!
# - also get rid of included jquery, jquery-ui library
# - do something with the cron stuff, maybe already prepare cron.d entries? 
# - fix attributemap, is this still needed? if the user needs to modify this 
#   it should really go to /etc/simplesamlphp. Debian has it in 
#   /etc/simplesamlphp
# - add a README.dist including information about setting the salt, the 
#   password, module enablement, SELinux and enabling the various plugins...
# - [Fixed] fix the execute bit on non-scripts
# - [U] make it possible to modify the paths in config.php to the config and
#   metadata directory so symlinks are no longer needed
#   ISSUE: http://code.google.com/p/simplesamlphp/issues/detail?id=349
# - [Fixed] make it possible to modify the paths in config.php and
#   metadata directory 
#   ISSUE: http://code.google.com/p/simplesamlphp/issues/detail?id=349
# - fix the license info, there are lots of licenses involved in this project
#   see the Debian package for a list of licenses...
# - somehow make this package work with previously created RPM packages 
#   (smooth upgrade path)

Name: simplesamlphp
Version: 1.11.0
Release: 1%{?dist}
Summary: PHP SAML 2.0 service provider and identity provider

Group: Applications/Internet
License: LGPLv2
URL: http://simplesamlphp.org/
Source0: http://simplesamlphp.googlecode.com/files/simplesamlphp-%{version}.tar.gz
Patch0: simplesamlphp-config-dirs-v1.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?el6}
Requires: php-fpm >= 5.2.10
Requires: php-xml
Requires: php-pdo
Requires: openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
%endif 


# LDAP is not a core requirement
# Requires: php53-ldap
# Mysql is not a core requirement 
# Requires: php53-mysql

# This packages don't exist on Red Hat > 5.8
# Requires: php-mcrypt
# Requires: php-pecl-radius

BuildArch: noarch
 
%description
SimpleSAMLphp is an award-winning application written in native PHP 
that deals with authentication. The project is led by UNINETT, has a 
large user base, a helpful user community and a large set of 
external contributors.

SimpleSAMLphp is having a main focus on providing support for:

    SAML 2.0 as a Service Provider.
    SAML 2.0 as a Identity Provider.

But also supports some other identity protocols, such as Shibboleth 
1.3, A-Select, CAS, OpenID, WS-Federation and OAuth.

%prep
%setup -q -b 0
%patch0 -p0

%build

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config
cp config/config.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config/config.php
cp config/authsources.php ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config/authsources.php

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pki
cp -pr cert ${RPM_BUILD_ROOT}%{_sysconfdir}/pki/%{name}

install -m 0770 -d -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}/data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}/metadata

mkdir -p ${RPM_BUILD_ROOT}%{_defaultdocdir}/%{name}
cp -pr docs/* ${RPM_BUILD_ROOT}%{_defaultdocdir}/%{name}/

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}
cp -pr * ${RPM_BUILD_ROOT}%{_libdir}/%{name}
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/config 
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/metadata 
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/data 
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/cert
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/log 
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/docs
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/COPYING

install -m 0770 -d -p ${RPM_BUILD_ROOT}%{_datadir}/log/%{name}

ln -sf %{_sysconfdir}/%{name}/config ${RPM_BUILD_ROOT}%{_libdir}/%{name}/config

%clean
rm -rf ${RPM_BUILD_ROOT}


%pre
if [ -z "$(/usr/bin/getent group %{name})" ]; then
    /usr/sbin/groupadd -r %{name}
fi

if [ -z "$(/usr/bin/getent passwd %{name})" ]; then
    /usr/sbin/useradd -r -N -s /bin/false %{name}
    /usr/bin/gpasswd -a %{name} %{name}
	/usr/bin/gpasswd -a apache %{name}
fi


%postun
/usr/bin/gpasswd -d apache %{name}
if [ -n "$(/usr/bin/getent passwd %{name})" ]; then
    /usr/sbin/userdel %{name}
fi

%files
%defattr(644,root,%{name},755)

%dir %attr(775,%{name},%{name}) %{_datadir}/log/%{name}

%dir %attr(750,root,%{name}) %{_sysconfdir}/pki/%{name}
%attr(640,root,%{name}) %config(noreplace) %{_sysconfdir}/pki/%{name}/*

%dir %{_sysconfdir}/%{name}
%attr(640,root,%{name}) %config(noreplace) %{_sysconfdir}/%{name}/*

%dir %attr(750,root,%{name}) %{_libdir}/%{name}

%{_libdir}/%{name}/attributemap
%{_libdir}/%{name}/bin
%{_libdir}/%{name}/config-templates
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/extra
%{_libdir}/%{name}/lib
%{_libdir}/%{name}/metadata-templates
%{_libdir}/%{name}/schemas
%{_libdir}/%{name}/templates
%{_libdir}/%{name}/www
%{_libdir}/%{name}/config

%{_libdir}/%{name}/modules/aggregator2
%{_libdir}/%{name}/modules/radius
%{_libdir}/%{name}/modules/aggregator
%{_libdir}/%{name}/modules/saml
%{_libdir}/%{name}/modules/cas
%{_libdir}/%{name}/modules/riak
%{_libdir}/%{name}/modules/multiauth
%{_libdir}/%{name}/modules/aselect
%{_libdir}/%{name}/modules/openidProvider
%{_libdir}/%{name}/modules/casserver
%{_libdir}/%{name}/modules/smartnameattribute
%{_libdir}/%{name}/modules/saml2debug
%{_libdir}/%{name}/modules/openid
%{_libdir}/%{name}/modules/negotiate
%{_libdir}/%{name}/modules/papi
%{_libdir}/%{name}/modules/expirycheck
%{_libdir}/%{name}/modules/autotest
%{_libdir}/%{name}/modules/logpeek
%{_libdir}/%{name}/modules/authmyspace
%{_libdir}/%{name}/modules/consentAdmin
%{_libdir}/%{name}/modules/authfacebook
%{_libdir}/%{name}/modules/exampleattributeserver
%{_libdir}/%{name}/modules/portal
%{_libdir}/%{name}/modules/authtwitter
%{_libdir}/%{name}/modules/authwindowslive
%{_libdir}/%{name}/modules/themefeidernd
%{_libdir}/%{name}/modules/metaedit
%{_libdir}/%{name}/modules/cron
%{_libdir}/%{name}/modules/authYubiKey
%{_libdir}/%{name}/modules/consentSimpleAdmin
%{_libdir}/%{name}/modules/sanitycheck
%{_libdir}/%{name}/modules/discopower
%{_libdir}/%{name}/modules/authlinkedin
%{_libdir}/%{name}/modules/metarefresh
%{_libdir}/%{name}/modules/core
%{_libdir}/%{name}/modules/authorize
%{_libdir}/%{name}/modules/exampleauth
%{_libdir}/%{name}/modules/ldap
%{_libdir}/%{name}/modules/oauth
%{_libdir}/%{name}/modules/smartattributes
%{_libdir}/%{name}/modules/statistics
%{_libdir}/%{name}/modules/memcacheMonitor
%{_libdir}/%{name}/modules/sqlauth
%{_libdir}/%{name}/modules/modinfo
%{_libdir}/%{name}/modules/consent
%{_libdir}/%{name}/modules/cdc
%{_libdir}/%{name}/modules/adfs
%{_libdir}/%{name}/modules/InfoCard
%{_libdir}/%{name}/modules/authcrypt
%{_libdir}/%{name}/modules/preprodwarning
%{_libdir}/%{name}/modules/authX509

%{_defaultdocdir}/%{name}
%dir %attr(770,root,%{name}) %{_localstatedir}/lib/%{name}
%attr(770,root,%{name}) %{_localstatedir}/lib/%{name}/data
%attr(770,root,%{name}) %{_localstatedir}/lib/%{name}/metadata

%doc docs/ COPYING

%changelog
* Mon Jul 1 2013 <smartin@yaco.es> <aperezaranda@yaco.es> - 1.11.0-1
- initial package based on previous work by Gijs Molenaar, Xander Jansen, F. Kooman
