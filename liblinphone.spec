%define major 10
%define libname %mklibname linphone
%define devname %mklibname linphone -d
%define libname_linphonepp %mklibname linphone++

# exclude unwanted cmake provides
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

# exclude unwanted cmake requires
%global __requires_exclude cmake\\(openldap\\)|cmake\\(OpenLDAP\\) \
	|cmake\\(tunnel\\)|cmake\\(Tunnel\\) \
	|cmake\\(turbojpeg\\)|cmake\\(TurboJpeg\\)

%bcond console_ui		1
%bcond debug			0
%bcond db			1
%bcond example_plugins		0
%bcond java			0
%bcond ldap			0
%bcond qrcode_support		1
%bcond strict			0
%bcond tools			1
%bcond unit_tests		1
%bcond unit_tests_install	0

Summary:	Voice over IP Application
Name:		liblinphone
Version:	5.4.20
Release:	1
License:	GPLv2+
Group:		Communications
URL:		https://www.linphone.org
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
%if %{with ldap}
BuildRequires:	pkgconfig(ldap)
%endif
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(python)
%if %{with qrcode_support}
BuildRequires:	pkgconfig(zxing)
%endif
BuildRequires:	python%{pyver}dist(pystache)
BuildRequires:	python%{pyver}dist(six)
%if %{with db}
BuildRequires:	soci-devel
%endif
BuildRequires:	xsd-devel

%description
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files
%license LICENSE.txt
%if %{with tools}
%doc README.md CHANGELOG.md NEWS
%{_bindir}/liblinphone-auto-answer
%{_bindir}/liblinphone-groupchat-benchmark
%{_bindir}/liblinphone-lpc2xml-test
%{_bindir}/liblinphone-sendmsg
%{_bindir}/liblinphone-test-ecc
%{_bindir}/liblinphone-xml2lpc-test
%endif
%if %{with unit_tests} && %{with unit_tests_install}
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/
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
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_CONSOLE_UI:BOOL=%{?with_console_ui:ON}%{?!with_console_ui:OFF} \
	-DENABLE_DAEMON:BOOL=YES \
	-DENABLE_DATE:BOOL=OFF \
	-DENABLE_DB_STORAGE:BOOL=%{?with_db:ON}%{?!with_db:OFF} \
	-DENABLE_EXAMPLE_PLUGIN:BOOL=%{?with_example_plugins:ON}%{?!with_example_plugins:OFF} \
	-DENABLE_GTK_UI:BOOL=OFF \
	-DENABLE_JAVA:BOOL=%{?with_java:ON}%{?!with_java:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!with_ldap:OFF} \
	-DENABLE_QRCODE:BOOL=%{?with_qrcode_support:ON}%{?!with_qrcode_support:OFF} \
	-DENABLE_ROOTCA_DOWNLOAD:BOOL=OFF \
	-DENABLE_TOOLS:BOOL=%{?with_tools:ON}%{?!with_tools:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_ZRTP:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# FIXME: manually create plugin directory
install -dm 0755 %{buildroot}%{_libdir}/%{name}/plugins

# remove already packaged cmake files
rm -f %{buildroot}%{_datadir}/cmake/LibLinphone/FindSoci.cmake
rm -f %{buildroot}%{_datadir}/cmake/LibLinphone/FindZXing.cmake

# remove unused
rm -f %{buildroot}%{_datadir}/linphone/rootca.pem

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

