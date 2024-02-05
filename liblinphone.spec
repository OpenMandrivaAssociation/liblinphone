%define major 10
%define libname %mklibname linphone
%define devname %mklibname linphone -d
%define libname_linphonepp %mklibname linphone++

# exclude unwanter cmake requires
%global __requires_exclude cmake\\(openldap\\)|cmake\\(OpenLDAP\\) \
	|cmake\\(tunnel\\)|cmake\\(Tunnel\\)

%bcond_without	console_ui
%bcond_with	debug
%bcond_without	db
%bcond_with	example_plugins
%bcond_with	java
%bcond_with	ldap
%bcond_without	qrcode_support
%bcond_with	static
%bcond_with	strict
%bcond_with	tests
%bcond_without tools

Summary:	Voice over IP Application
Name:		liblinphone
Version:	5.3.15
Release:	2
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/liblinphone/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		liblinphone-5.3.6-cmake-config-location.patch
Patch1:		liblinphone-5.2.0-cmake-dont-use-bc_git_version.patch
Patch2:		liblinphone-5.2.0-fix-pkgconfig.patch
Patch3:		liblinphone-5.3.15-use_system_rootca.patch
Patch4:		liblinphone-5.3.6-fix_compiler_strict-prototypes_warinig.patch
Patch5:		liblinphone-5.3.6-fix_clang.patch
Patch6:		liblinphone-5.3.15-add_jsoncpp_dep.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(bellesip)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(libjpeg-turbo)
BuildRequires:	cmake(lime)
BuildRequires:	cmake(mediastreamer2)
%{?with_qrcode_support:
BuildRequires:	cmake(zxing)
}
%{?with_ldap:
BuildRequires:	pkgconfig(ldap)
}
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

%description
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%if %{with tools}
%files
%license LICENSE.txt
%doc README.md CHANGELOG.md NEWS
%{_bindir}/liblinphone-auto-answer
%{_bindir}/liblinphone-lpc2xml-test
%{_bindir}/liblinphone-sendmsg
%{_bindir}/liblinphone-test-ecc
%{_bindir}/liblinphone-xml2lpc-test
%endif

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
%if %{with console_ui}
%{_bindir}/linphonec
%{_bindir}/linphonecsh
%endif
%{_bindir}/linphone-daemon
%{_bindir}/linphone-daemon-pipetest

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
#{_datadir}/linphone/rootca.pem

#--------------------------------------------------------------------


%package -n %{libname}
Summary:	Primary library for linphone
Group:		System/Libraries
Requires:	linphone-data >= %{version}-%{release}

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%dir %{_libdir}/%{name}/plugins/
%if %{with example_plugins}
%{_libdir}/%{name}/plugins/*
%endif
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
%{_datadir}/cmake/LibLinphone
%{_datadir}/cmake/LinphoneCxx

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

# delete bundled libs
rm -rf libxsd

# Fix XSD runtime version mismatch
sed -i -e '/XSD_INT_VERSION/s/!=/</g' $(grep -r -l XSD_INT_VERSION)

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_CONSOLE_UI:BOOL=%{?with_console_ui:ON}%{?!without_console_ui:OFF} \
	-DENABLE_DAEMON:BOOL=YES \
	-DENABLE_DATE:BOOL=OFF \
	-DENABLE_DB_STORAGE:BOOL=%{?with_db:ON}%{?!without_db:OFF} \
	-DENABLE_EXAMPLE_PLUGIN:BOOL=%{?with_example_plugins:ON}%{?!without_example_plugins:OFF} \
	-DENABLE_GTK_UI:BOOL=OFF \
	-DENABLE_JAVA:BOOL=%{?with_java:ON}%{?!without_java:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!without_ldap:OFF} \
	-DENABLE_QRCODE:BOOL=%{?with_qrcode_support:ON}%{?!without_qrcode_support:OFF} \
    -DENABLE_ROOTCA_DOWNLOAD:BOOL=OFF \
	-DENABLE_TOOLS:BOOL=%{?with_tools:ON}%{?!without_tools:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_tests:ON}%{?!without_tests:OFF} \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_ZRTP:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# FIXME: manually create plugin directory
install -dm 0755 %{buildroot}%{_libdir}/%{name}/plugins

# remove unused
rm -f %{buildroot}%{_datadir}/linphone/rootca.pem

