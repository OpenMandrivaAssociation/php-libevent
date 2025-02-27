%define modname libevent
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B02_%{modname}.ini

Summary:	Libevent - event notification
Name:		php-%{modname}
Version:	0.1.0
Release:	2
Group:		Development/PHP
License:	PHP License
Url:		https://pecl.php.net/package/libevent/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pkgconfig(libevent)

%description
This extension is a wrapper for libevent - event notification library.

%prep

%setup -qn %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x \
	--with-libdir=%{_lib} \
	--with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
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

%files 
%doc CREDITS package*.xml 
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{_libdir}/php/extensions/%{soname}

