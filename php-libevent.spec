%define modname libevent
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B02_%{modname}.ini

Summary:	Libevent - event notification
Name:		php-%{modname}
Version:	0.0.5
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/libevent/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libevent-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension is a wrapper for libevent - event notification library.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-2mdv2012.0
+ Revision: 795470
- rebuild for php-5.4.x

* Tue Apr 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-1
+ Revision: 789000
- 0.0.5

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-5
+ Revision: 761262
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-4
+ Revision: 696438
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-3
+ Revision: 695413
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-2
+ Revision: 646655
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-1mdv2011.0
+ Revision: 630304
- 0.0.4

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-9mdv2011.0
+ Revision: 629817
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-8mdv2011.0
+ Revision: 628138
- ensure it's built without automake1.7
- rebuilt against libevent 2.x

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-6mdv2011.0
+ Revision: 600502
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-5mdv2011.0
+ Revision: 588840
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-4mdv2010.1
+ Revision: 514566
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-3mdv2010.1
+ Revision: 485399
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-2mdv2010.1
+ Revision: 468182
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-1mdv2010.0
+ Revision: 452910
- import php-libevent


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-1mdv2010.0
- initial Mandriva package
