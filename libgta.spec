#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library to read and write Generic Tagged Arrays (GTAs)
Summary(pl.UTF-8):	Biblioteka od odczytu i zapisu GTA (ogólnych tablic etykietowanych)
Name:		libgta
Version:	1.0.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://download.savannah.nongnu.org/releases/gta/%{name}-%{version}.tar.xz
# Source0-md5:	60bba54c4be60d11bf531300db6673c2
URL:		http://gta.nongnu.org/libgta.html
BuildRequires:	bzip2-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libgta is a portable library that implements the Generic Tagged Array
(GTA) file format. This file format has the following features:

* GTAs can store any kind of data in multidimensional arrays
* GTAs can optionally use simple tags to store rich metadata
* GTAs are streamable, which allows direct reading from and writing to
  pipes, network sockets, and other non-seekable media
* GTAs can use ZLIB, BZIP2, or XZ compression, allowing a tradeoff
  between compression/decompression speed and compression ratio
* Uncompressed GTA files allow easy out-of-core data access for very
  large arrays.

%description -l pl.UTF-8
libgta to przenośna biblioteka zawierająca implementację formatu GTA
(Generic Tagged Array - ogólnych tablic etykietowanych). Format ten ma
następujące cechy:
- może przechowywać dowolny rodzaj danych w tablicach wielowymiarowych
- opcjonalnie może wykorzystywać proste etykiety do przechowywania
  bogatych metadanych
- daje się obrabiać strumieniowo, co pozwala na bezpośredni odczyt i
  zapis do potoków, gniazd sieciowych i innych nośników nie
  obsługujących przewijania
- może wykorzystywać kompresję ZLIB, BZIP2 lub XZ, pozwalając na
  kompromis między szybkością kompresji/dekompresji a współczynnikiem
  upakowania
- w przypadku nieskompresowanych plików możliwy jest łatwy dostęp do
  danych nawet dla bardzo dużych tablic.

%package devel
Summary:	Header files for GTA library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GTA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bzip2-devel
Requires:	xz-devel
Requires:	zlib-devel

%description devel
Header files for GTA library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GTA.

%package static
Summary:	Static GTA library
Summary(pl.UTF-8):	Statyczna biblioteka GTA
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GTA library.

%description static -l pl.UTF-8
Statyczna biblioteka GTA.

%package apidocs
Summary:	GTA API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GTA
Group:		Documentation

%description apidocs
API and internal documentation for GTA library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GTA.

%prep
%setup -q

%build
%configure \
	%{!?with_apidocs:--disable-reference} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_datadir}/cmake/Modules}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/example-*.c* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/FindGTA.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
# packaged in -apidocs
%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}/reference}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libgta.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgta.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgta.so
%{_includedir}/gta
%{_pkgconfigdir}/gta.pc
%{_datadir}/cmake/Modules/FindGTA.cmake
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libgta.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/reference/*.{css,html,js,png}
%endif
