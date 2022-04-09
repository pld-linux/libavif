#
# Conditional build:
%bcond_without	aom		# AOM for encoding/decoding
%bcond_with	dav1d		# dav1d for decoding
%bcond_with	libgav1		# libgav1 for decoding
%bcond_with	rav1e		# rav1e for encoding
%bcond_with	svtav1		# SVT-AV1 for encoding
#
Summary:	Library for encoding and decoding .avif files
Summary(pl.UTF-8):	Biblioteka do kodowania i dekodowania plików .avif
Name:		libavif
Version:	0.10.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AOMediaCodec/libavif/releases
Source0:	https://github.com/AOMediaCodec/libavif/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	42e783d32c8d5ae2d763edccebcc63a5
URL:		https://github.com/AOMediaCodec/libavif
%{?with_aom:BuildRequires:	aom-devel}
BuildRequires:	cmake >= 3.5
%{?with_dav1d:BuildRequires:	dav1d-devel}
BuildRequires:	gcc >= 5:3.2
%{?with_libgav1:BuildRequires:	libgav1-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
# 1813+ preferred
BuildRequires:	libyuv-devel >= 0.1755
%{?with_rav1e:BuildRequires:	rav1e-devel}
BuildRequires:	rpmbuild(macros) >= 1.745
%{?with_svtav1:BuildRequires:	svt-av1-devel}
BuildRequires:	zlib-devel
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

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_aom:-DAVIF_CODEC_AOM=ON} \
	%{?with_dav1d:-DAVIF_CODEC_DAV1D=ON} \
	%{?with_libgav1:-DAVIF_CODEC_LIBGAV1=ON} \
	%{?with_rav1e:-DAVIF_CODEC_RAV1E=ON} \
	%{?with_svtav1:-DAVIF_CODEC_SVT=ON}

%{__make}

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
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libavif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavif.so.14

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavif.so
%{_includedir}/avif
%{_pkgconfigdir}/libavif.pc
%{_libdir}/cmake/libavif
