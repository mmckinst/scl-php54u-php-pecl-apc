%if 0%{?scl:1}
%scl_package php-pecl-apc
%endif

%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}
%{?!pecl_xmldir: %{expand: %%global pecl_xmldir %{pecl_phpdir}/.pkgxml}}

%define php_extdir %(%{_bindir}/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)                     
%global php_zendabiver %((echo 0; %{_bindir}/php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global php_version %((echo 0; %{_bindir}/php-config --version 2>/dev/null) | tail -1)
%define pecl_name APC
%{?!_without_php_ver_tag: %define php_ver_tag .php%{php_major_version}}

#%%define patchver p1

Summary:        APC caches and optimizes PHP intermediate code
Name:           %{?scl_prefix}php-pecl-apc
Version:        3.1.13
Release:        3.ius%{?dist}
License:        PHP
Group:          Development/Languages
Vendor:         IUS Community Project 
URL:            http://pecl.php.net/package/APC
Source:         http://pecl.php.net/get/APC-%{version}.tgz
Source1:        apc.ini

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts:      %{?scl_prefix}php-mmcache %{?scl_prefix}php-eaccelerator
Conflicts:      %{?scl_prefix}php-zend-optimizer %{?scl_prefix}phpzend-optimizer
BuildRequires:  %{?scl_prefix}php-devel %{?scl_prefix}php-cli httpd-devel %{?scl_prefix}php-pear
BuildRequires:  pcre-devel

Requires:       %{?scl_prefix}php-zend-abi = %{php_zendabiver}
Provides:      	%{?scl_prefix}php-pecl(%{pecl_name}) = %{version}

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

# FIX ME: This should be removed before/after RHEL 5.6 is out
# See: https://bugs.launchpad.net/ius/+bug/691755


%description
APC is a free, open, and robust framework for caching and optimizing PHP
intermediate code.

%prep
%setup -q -n %{pecl_name}-%{version}

%build
%{_bindir}/phpize
%configure --enable-apc-memprotect --with-apxs=%{_sbindir}/apxs --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Install the package XML file
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/apc.ini


# Fix the charset of NOTICE
iconv -f iso-8859-1 -t utf8 NOTICE >NOTICE.utf8
mv NOTICE.utf8 NOTICE

%post
%{__pecl} install --nodeps --soft --force --register-only --nobuild %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc TECHNOTES.txt CHANGELOG LICENSE NOTICE TODO INSTALL apc.php
%config(noreplace) %{_sysconfdir}/php.d/apc.ini
%{php_extdir}/apc.so
%{pecl_xmldir}/%{pecl_name}.xml
%{_includedir}/php/ext/apc/apc_serializer.h

%changelog
* Tue Jan 28 2014 Mark McKinstry <mmckinst@nexcess.net> - 3.1.13-3.ius
- convert to scl style rpm
- use bindir macro to we get the scl binaries

* Thu Jul 25 2013 Ben Harper <ben.harper@rackspace.com> - 3.1.13-2.ius
- removing Requires for php54:
  https://bugs.launchpad.net/ius/+bug/1204492

* Mon May 06 2013 Ben Harper <ben.harper@rackspace.com> - 3.1.13-1.ius
- reverting version to rebuild due to:
  https://bugs.launchpad.net/ius/+bug/1115670

* Thu Jan 10 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.1.14-1.ius
- Latest Beta sources, not yet a Stable branch with PHP 5.4 support.
  https://bugs.launchpad.net/ius/+bug/1098124

* Mon Nov 12 2012 Ben Harper <ben.harper@rackspace.com> - 3.1.13-1.ius
- Latest upstream sources 
    
* Tue Aug 21 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0:3.1.11-3.ius
- Rebuilding against php54-5.4.6-2.ius as it is now using bundled PCRE.

* Fri May 04 2012 Dustin Henry Offutt <dustin.offutt@rackspace.com> - 0:3.1.11-2.ius
- Latest upstream sources
- Jump to release 2 as release 1 build not pushed to LP

* Fri May 04 2012 Dustin Henry Offutt <dustin.offutt@rackspace.com> - 0:3.1.10-1.ius
- Build for PECL APC 3.1.10 (beta)

* Thu Apr 19 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0:3.1.9-1.ius
- Porting from php53u-pecl-apc to php54-pecl-apc
