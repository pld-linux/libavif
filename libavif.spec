# TODO: AVM (when actual codec library released)
#
# Conditional build:
%bcond_without	aom		# AOM for encoding/decoding
%bcond_without	man		# man pages
%bcond_with	dav1d		# dav1d for decoding
%bcond_with	libgav1		# libgav1 for decoding
%bcond_with	rav1e		# rav1e for encoding
%bcond_with	svtav1		# SVT-AV1 for encoding
#
Summary:	Library for encoding and decoding .avif files
Summary(pl.UTF-8):	Biblioteka do kodowania i dekodowania plików .avif
Name:		libavif
Version:	1.2.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AOMediaCodec/libavif/releases
Source0:	https://github.com/AOMediaCodec/libavif/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ec292cb8d51c0aa02f9fd5ef2419c853
# cmake/Modules/LocalLibargparse.cmake /AVIF_LIBARGPARSE_GIT_TAG
%define	libargparse_gitref	ee74d1b53bd680748af14e737378de57e2a0a954
Source1:	https://github.com/kmurray/libargparse/archive/%{libargparse_gitref}/libargparse-%{libargparse_gitref}.tar.gz
# Source1-md5:	e8f6d28aa9039973c40d31186ed22de7
URL:		https://github.com/AOMediaCodec/libavif
%{?with_aom:BuildRequires:	aom-devel}
BuildRequires:	cmake >= 3.13
%{?with_dav1d:BuildRequires:	dav1d-devel}
BuildRequires:	gcc >= 5:3.2
%{?with_libgav1:BuildRequires:	libgav1-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsharpyuv-devel
# C++14
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libxml2-devel >= 2.0
# 1813+ preferred
BuildRequires:	libyuv-devel >= 0.1755
%{?with_man:BuildRequires:	pandoc}
%{?with_rav1e:BuildRequires:	rav1e-devel}
BuildRequires:	rpmbuild(macros) >= 1.745
%{?with_svtav1:BuildRequires:	svt-av1-devel}
BuildRequires:	zlib-devel
%requires_ge_to	libyuv libyuv-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library aims to be a friendly, portable C implementation of the
AV1 Image File Format, as described here:
<https://aomediacodec.github.io/av1-avif/>.

%description -l pl.UTF-8
Ta biblioteka powstała jako przyjazna, przenośna implementacja w C
obsługa formatu obrazów AV1, opisanego w dokumencie
<https://aomediacodec.github.io/av1-avif/>.

%package devel
Summary:	Header files for libavif library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libavif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libavif library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libavif.

%package tools
Summary:	Tools to encode and decode AVIF files
Summary(pl.UTF-8):	Narzędzia do kodowania i dekodowania plików AVIF
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to encode and decode AVIF files.

%description tools -l pl.UTF-8
Narzędzia do kodowania i dekodowania plików AVIF.

%prep
%setup -q -a1
%{__mv} libargparse-%{libargparse_gitref} ext/libargparse

%build
install -d ext/libargparse/build
%cmake -B ext/libargparse/build -S ext/libargparse \
	-DBUILD_SHARED_LIBS=OFF
%{__make} -C ext/libargparse/build

%cmake -B build \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DAVIF_BUILD_APPS=ON \
	%{cmake_on_off man AVIF_BUILD_MAN_PAGES} \
	%{?with_aom:-DAVIF_CODEC_AOM=SYSTEM} \
	%{?with_dav1d:-DAVIF_CODEC_DAV1D=SYSTEM} \
	%{?with_libgav1:-DAVIF_CODEC_LIBGAV1=SYSTEM} \
	%{?with_rav1e:-DAVIF_CODEC_RAV1E=SYSTEM} \
	%{?with_svtav1:-DAVIF_CODEC_SVT=SYSTEM} \
	-DAVIF_LIBSHARPYUV=SYSTEM \
	-DAVIF_LIBXML2=SYSTEM

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md SECURITY.md
%attr(755,root,root) %{_libdir}/libavif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavif.so.16

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavif.so
%{_includedir}/avif
%{_pkgconfigdir}/libavif.pc
%{_libdir}/cmake/libavif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avifdec
%attr(755,root,root) %{_bindir}/avifenc
%attr(755,root,root) %{_bindir}/avifgainmaputil
%if %{with man}
%{_mandir}/man1/avifdec.1*
%{_mandir}/man1/avifenc.1*
%endif
