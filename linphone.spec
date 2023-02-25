%define major 10
%define libname	%mklibname %{name}
%define devname %mklibname %{name} -d
%define libname_linphonepp %mklibname %{name}++

%bcond_without	assistant
%bcond_with	debug
%bcond_without	db
%bcond_with	ldap
%bcond_without	notify
%bcond_with	static
%bcond_with	strict
%bcond_with	tests

Summary:	Voice over IP Application
Name:		linphone
Version:	5.2.23
Release:	1
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/liblinphone/-/archive/%{version}/lib%{name}-%{version}.tar.bz2
Patch0:		linphone-5.0.44-cmake-config-location.patch
Patch1:		linphone-5.2.0-cmake-dont-use-bc_git_version.patch
# (wally) originally from OpenSUSE, slightly modified
Patch2:		linphone-5.2.0-fix-pkgconfig.patch
Patch3:		linphone-4.4.24-fix_xds_version.patch
Patch4:		linphone-5.0.44-dont_check_bctools_version.patch
Patch5:		linphone-5.1.61-fix_compiler_strict-prototypes_warinig.patch
Patch6:		linphone-5.1.61-fix_clang.patch
# required by zxing-cpp
Patch7:		linphone-5.2.23-force-cpp17-standard.patch
# (upstream)
Patch10:	linphone-5.2.0-use_shared_libs.patch


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
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_DATE:BOOL=OFF \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_tests:ON}%{?!without_tests:OFF} \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_DB_STORAGE:BOOL=%{?with_db:ON}%{?!without_db:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!without_ldap:OFF} \
	-DENABLE_ASSISTANT:BOOL=%{?with_assistant:ON}%{?!without_assistant:OFF} \
	-DENABLE_NOTIFY:BOOL=%{?with_notify:ON}%{?!without_notify:OFF} \
	-DENABLE_BUILD_VERBOSE:BOOL=OFF \
	-DENABLE_DEBUG_LOGS:BOOOL=%{?with_debug:ON}%{?!without_debug:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

