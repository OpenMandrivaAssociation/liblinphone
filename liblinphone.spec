%define major 10
%define libname	%mklibname linphone
%define devname %mklibname linphone -d
%define libname_linphonepp %mklibname linphone++

%bcond_without	assistant
%bcond_with	debug
%bcond_without	db
%bcond_with	ldap
%bcond_without	notify
# (mandian) qrcode support requires c++17 standard enabled
%bcond_with	qrcode_support
%bcond_with	static
%bcond_with	strict
%bcond_with	tests

Summary:	Voice over IP Application
Name:		liblinphone
Version:	5.2.67
Release:	1
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/liblinphone/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		liblinphone-5.0.44-cmake-config-location.patch
Patch1:		liblinphone-5.2.0-cmake-dont-use-bc_git_version.patch
# (wally) originally from OpenSUSE, slightly modified
Patch2:		liblinphone-5.2.0-fix-pkgconfig.patch
Patch3:		liblinphone-4.4.24-fix_xds_version.patch
Patch4:		liblinphone-5.0.44-dont_check_bctools_version.patch
Patch5:		liblinphone-5.1.61-fix_compiler_strict-prototypes_warinig.patch
Patch6:		liblinphone-5.1.61-fix_clang.patch
# required by zxing-cpp
#Patch7:		linphone-5.2.23-force-cpp17-standard.patch
# (upstream)
Patch10:	liblinphone-5.2.0-use_shared_libs.patch


BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(bellesip)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(libjpeg-turbo)
BuildRequires:	cmake(lime)
BuildRequires:	cmake(mediastreamer2)
BuildRequires:	cmake(zxing)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(pystache)
BuildRequires:	python3dist(six)
%{?with_db:
BuildRequires:	soci-devel
}
BuildRequires:	xsd-devel
%{?with_ldap:
BuildRequires:	openldap-devel
}

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

%package -n linphone-cli
Summary:	Command Line Interface for %{name}
Group:		Communications
Requires:	%{name}-data >= %{version}-%{release}
Conflicts:	%{name} < 3.12.0-1

%description -n linphone-cli
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files -n linphone-cli
%license LICENSE.txt
%doc README.md CHANGELOG.md NEWS
%{_bindir}/linphonec*
%{_bindir}/linphone-daemon*

#--------------------------------------------------------------------

%package -n linphone-data
Summary:	Data files for linphone
Group:		Communications
BuildArch:	noarch
Conflicts:	linphone < 3.12.0-1
Provides:	%{name}-data

%description -n linphone-data
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files -n linphone-data
%{_datadir}/belr/grammars/
%{_datadir}/sounds/linphone/
%{_datadir}/linphone/rootca.pem

#--------------------------------------------------------------------


%package -n %{libname}
Summary:	Primary library for linphone
Group:		System/Libraries
Requires:	linphone-data >= %{version}-%{release}

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

#--------------------------------------------------------------------

%package -n %{libname_linphonepp}
Summary:	C++ wrapper library for linphone
Group:		System/Libraries

%description -n %{libname_linphonepp}
C++ wrapper library for linphone.

%files -n %{libname_linphonepp}
%{_libdir}/%{name}++.so.%{major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries for linphone
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname_linphonepp} = %{version}-%{release}
Provides:	linphone-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on linphone.

%files -n %{devname}
%{_includedir}/linphone/
%{_includedir}/linphone++/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/Linphone
%{_datadir}/cmake/LinphoneCxx

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_DATE:BOOL=OFF \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_tests:ON}%{?!without_tests:OFF} \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_DB_STORAGE:BOOL=%{?with_db:ON}%{?!without_db:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!without_ldap:OFF} \
	-DENABLE_ASSISTANT:BOOL=%{?with_assistant:ON}%{?!without_assistant:OFF} \
	-DENABLE_NOTIFY:BOOL=%{?with_notify:ON}%{?!without_notify:OFF} \
	-DENABLE_QRCODE:BOOL=%{?with_qrcode_support:ON}%{?!without_qrcode_support:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

