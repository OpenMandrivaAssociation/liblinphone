%define _disable_rebuild_configure 1
%define _disable_lto 1
%define _disable_ld_no_undefined 1

%define linphone_major 9
%define liblinphone %mklibname %{name} %{linphone_major}
%define devname %mklibname -d %{name}
%define libname_linphonepp %mklibname %{name}++ %{linphone_major}

Summary:	Voice over IP Application
Name:		linphone
Version:	3.12.0
Release:	1
License:	GPLv2+
Group:		Communications
Url:		http://www.linphone.org/
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz
# Source1:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz.sig
Patch1:		linphone-3.12.0-cmake-config-location.patch
# (wally) originally from OpenSUSE, slightly modified
Patch2:	linphone-fix-pkgconfig.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	readline-devel
BuildRequires:	python-pystache
# http://lists.gnu.org/archive/html/linphone-developers/2013-04/msg00016.html

BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(belle-sip)
BuildRequires:	pkgconfig(belcard)
BuildRequires:	pkgconfig(libbzrtp)
BuildRequires:	pkgconfig(libosip2)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(mediastreamer)
BuildRequires:	pkgconfig(ortp) >= 0.23.0
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xv)
BuildRequires:	bctoolbox-static-devel

%description
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

#--------------------------------------------------------------------

%package cli
Summary:        Command Line Interface for %{name}
Group:          Communications/Telephony
Requires:       liblinphone-data >= %{version}-%{release}
Conflicts:      %{name} < 3.12.0-1

%description cli
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files cli
%doc README.md AUTHORS BUGS ChangeLog COPYING
%{_bindir}/linphonec*
%{_bindir}/linphone-daemon*

#--------------------------------------------------------------------

%package -n     liblinphone-data
Summary:        Data files for %{name}
Group:          Communications/Telephony
BuildArch:      noarch
Conflicts:      %{name} < 3.12.0-1

%description -n liblinphone-data
Linphone is an open source SIP Phone, available on mobile and desktop
environments.

%files -n liblinphone-data
%{_datadir}/sounds/linphone/

#--------------------------------------------------------------------


%package -n %{liblinphone}
Summary:	Primary library for %{name}
Group:		System/Libraries
Requires:	liblinphone-data >= %{version}-%{release}

%description -n %{liblinphone}
Primary library for %{name}.

%files -n %{liblinphone}
%{_libdir}/liblinphone.so.%{linphone_major}*

#--------------------------------------------------------------------

%package -n     %{libname_linphonepp}
Summary:        C++ wrapper library for %{name}
Group:          System/Libraries

%description -n %{libname_linphonepp}
C++ wrapper library for %{name}.

%files -n %{libname_linphonepp}
%{_libdir}/liblinphone++.so.%{linphone_major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{liblinphone} = %{version}-%{release}
Requires:	%{libname_linphonepp} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/linphone/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%{_libdir}/cmake/Linphone/

%{_includedir}/linphone++/
%{_libdir}/cmake/LinphoneCxx/

#--------------------------------------------------------------------

%prep
%setup -q
find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%apply_patches

%build
export CC=gcc
export CXX=g++

%cmake \
    -DENABLE_STRICT=NO \
    -DENABLE_STATIC:BOOL=NO \
    -DENABLE_ROOTCA_DOWNLOAD:BOOL=NO \
    -DENABLE_GTK_UI:BOOL=NO \
    -DENABLE_TOOLS:BOOL=NO \
    -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Linphone

%make

%install
%makeinstall_std -C build

#find_lang %{name} --all-name --with-man

# remove unwanted docs, generated if doxygen is installed
rm -rf %{buildroot}%{_docdir}/ortp %{buildroot}%{_docdir}/mediastreamer* %{buildroot}%{_docdir}/%{name}*
