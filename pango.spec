%define		apiver	1.8.0

Summary:	System for layout and rendering of internationalized text
Name:		pango
Version:	1.31.2
Release:	1
Epoch:		1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.31/%{name}-%{version}.tar.xz
# Source0-md5:	ec3c1f236ee9bd4a982a5f46fcaff7b9
URL:		http://www.pango.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	harfbuzz-devel
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXft-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
System for layout and rendering of internationalized text.

%package devel
Summary:	System for layout and rendering of internationalized text
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Developer files for pango.

%package modules
Summary:	System for layout and rendering of internationalized text
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	cairo-devel

%description modules
System for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%package apidocs
Summary:	Pango API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Pango API documentation.

%prep
%setup -q

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--enable-introspection=yes	\
	--enable-man			\
	--with-html-dir=%{_gtkdocdir}	\
	--with-included-modules=basic-fc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pango

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

touch $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/%{apiver}/modules/*.la

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{be@latin,en@shaw,ps}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
umask 022
pango-querymodules > %{_sysconfdir}/pango/pango.modules ||:

%postun -p /usr/sbin/ldconfig

%post modules
umask 022
pango-querymodules > %{_sysconfdir}/pango/pango.modules ||:

%postun modules
umask 022
pango-querymodules > %{_sysconfdir}/pango/pango.modules ||:

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_bindir}/pango-view
%attr(755,root,root) %ghost %{_libdir}/libpango-1.0.so.?
%attr(755,root,root) %ghost %{_libdir}/libpangocairo-1.0.so.?
%attr(755,root,root) %ghost %{_libdir}/libpangoft2-1.0.so.?
%attr(755,root,root) %ghost %{_libdir}/libpangoxft-1.0.so.?
%attr(755,root,root) %{_libdir}/libpango-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%dir %{_libdir}/pango
%dir %{_libdir}/pango/%{apiver}
%dir %{_libdir}/pango/%{apiver}/modules

%dir %{_sysconfdir}/pango
%ghost %{_sysconfdir}/pango/pango.modules
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libpango*-1.0.so
# pkgconfig file missing deps
%{_libdir}/libpango*-1.0.la
%{_pkgconfigdir}/pango*.pc
%{_includedir}/pango-1.0
%{_datadir}/gir-1.0/*.gir

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pango/%{apiver}/modules/*.so

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango

