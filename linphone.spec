%define _disable_ld_no_undefined 1
#define _disable_lto 1

%define major 10
%define libname	%mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define libname_linphonepp %mklibname %{name}++ %{major}

Summary:	Voice over IP Application
Name:		linphone
Version:	5.1.45
Release:	1
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/lib%{name}/-/archive/%{version}/lib%{name}-%{version}.tar.bz2
Patch0:		linphone-5.0.44-cmake-config-location.patch
# (wally) originally from OpenSUSE, slightly modified
Patch1:		linphone-5.1.45-fix-pkgconfig.patch
Patch2:		linphone-4.4.24-fix_xds_version.patch
Patch3:		linphone-5.0.44-dont_check_bctools_version.patch

BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(bellesip)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(lime)
BuildRequires:	cmake(mediastreamer2)
BuildRequires:	ninja
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python3
BuildRequires:	python3dist(pystache)
BuildRequires:	python3dist(six)
BuildRequires:	soci-devel
BuildRequires:	xsd-devel

%description
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files
%license LICENSE.txt
%doc README.md CHANGELOG.md NEWS
%{_bindir}/lp-auto-answer
%{_bindir}/lp-sendmsg
%{_bindir}/lp-test-ecc
%{_bindir}/lpc2xml_test
%{_bindir}/xml2lpc_test

#--------------------------------------------------------------------

%package cli
Summary:	Command Line Interface for %{name}
Group:		Communications
Requires:	lib%{name}-data >= %{version}-%{release}
Conflicts:	%{name} < 3.12.0-1

%description cli
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files cli
%license LICENSE.txt
%doc README.md CHANGELOG.md NEWS
%{_bindir}/linphonec*
%{_bindir}/linphone-daemon*

#--------------------------------------------------------------------

%package -n lib%{name}-data
Summary:	Data files for %{name}
Group:		Communications
BuildArch:	noarch
Conflicts:	%{name} < 3.12.0-1

%description -n lib%{name}-data
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files -n lib%{name}-data
%{_datadir}/belr/grammars/
%{_datadir}/sounds/linphone/
%{_datadir}/%{name}/rootca.pem

#--------------------------------------------------------------------


%package -n %{libname}
Summary:	Primary library for %{name}
Group:		System/Libraries
Requires:	lib%{name}-data >= %{version}-%{release}

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#--------------------------------------------------------------------

%package -n %{libname_linphonepp}
Summary:	C++ wrapper library for %{name}
Group:		System/Libraries

%description -n %{libname_linphonepp}
C++ wrapper library for %{name}.

%files -n %{libname_linphonepp}
%{_libdir}/lib%{name}++.so.%{major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname_linphonepp} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/linphone/
%{_includedir}/linphone++/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/Linphone
%{_datadir}/cmake/LinphoneCxx

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n lib%{name}-%{version}
#find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?without_static:OFF} \
	-DENABLE_DATE:BOOL=OFF \
	-DENABLE_UNIT_TESTS:BOOL=OFF \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_STRICT:BOOL=OFF \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

