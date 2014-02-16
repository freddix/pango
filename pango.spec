%define		apiver	1.8.0

Summary:	System for layout and rendering of internationalized text
Name:		pango
Version:	1.36.2
Release:	1
Epoch:		1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.36/%{name}-%{version}.tar.xz
# Source0-md5:	253026c7132c22e52cefd998ba89a742
Patch0:		%{name}-multi-arch.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.12.16-4
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1:2.10.91
BuildRequires:	freetype-devel
BuildRequires:	glib-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gtk-doc
BuildRequires:	harfbuzz-devel >= 0.9.21
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXft-devel >= 2.3.1-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		march		64
%define		_sysconfdir	/etc/pango%{march}
%else
%define		march		%{nil}
%define		_sysconfdir	/etc/pango
%endif

%description
System for layout and rendering of internationalized text.

%package devel
Summary:	System for layout and rendering of internationalized text
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	cairo-devel

%description devel
Developer files for pango.

%package modules
Summary:	System for layout and rendering of internationalized text
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description modules
System for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%package view
Summary:	Pango text viewer
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description view
Pango text viewer.

%package apidocs
Summary:	Pango API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Pango API documentation.

%prep
%setup -q
%patch0 -p1

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
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

touch $RPM_BUILD_ROOT%{_sysconfdir}/pango.modules

# useless (modules loaded through libgmodule)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{,%{name}/%{apiver}/modules/}*.la

%ifarch %{x8664}
mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules{,%{march}}
mv $RPM_BUILD_ROOT%{_mandir}/man1/pango-querymodules{,%{march}}.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
umask 022
pango-querymodules%{march} > %{_sysconfdir}/pango.modules ||:

%postun -p /usr/sbin/ldconfig

%post modules
umask 022
pango-querymodules%{march} > %{_sysconfdir}/pango.modules ||:

%postun modules
umask 022
pango-querymodules%{march} > %{_sysconfdir}/pango.modules ||:

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/pango-querymodules%{march}
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

%dir %{_sysconfdir}
%ghost %{_sysconfdir}/pango.modules
%{_mandir}/man1/pango-querymodules%{march}.1*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libpango*-1.0.so
%{_pkgconfigdir}/pango*.pc
%{_includedir}/pango-1.0
%{_datadir}/gir-1.0/*.gir

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pango/%{apiver}/modules/*.so

%files view
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pango-view
%{_mandir}/man1/pango-view.1*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango

