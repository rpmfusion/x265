Summary: H.265/HEVC encoder
Name: x265
Version: 2.2
Release: 2%{?dist}
URL: http://x265.org/
Source0: https://ftp.videolan.org/pub/videolan/x265/%{name}_%{version}.tar.gz
# link test binaries with shared library
Patch1: x265-test-shared.patch
# fix building as PIC
Patch2: x265-pic.patch
Patch4: x265-detect_cpu_armhfp.patch
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License: GPLv2+ and BSD
BuildRequires: cmake
%ifnarch armv7hl armv7hnl s390 s390x
BuildRequires: numactl-devel
%endif
BuildRequires: yasm

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the command line encoder.

%package libs
Summary: H.265/HEVC encoder library

%description libs
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library.

%package devel
Summary: H.265/HEVC encoder library development files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library development files.

%prep
%autosetup -p1 -n %{name}_%{version}

%build
%cmake -G "Unix Makefiles" \
 -DCMAKE_SKIP_RPATH:BOOL=YES \
 -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
 -DENABLE_PIC:BOOL=ON \
 -DENABLE_TESTS:BOOL=ON \
 source
%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/libx265.a

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} test/TestBench || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/x265

%files libs
%license COPYING
%{_libdir}/libx265.so.102

%files devel
%doc doc/*
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Dominik Mierzejewski <rpm@greysector.net> - 2.2-1
- update to 2.2
- spell out SO version in file list
- fix typo in patch

* Mon Nov 07 2016 Sérgio Basto <sergio@serjux.com> - 2.1-1
- Update to 2.1

* Thu Aug 18 2016 Sérgio Basto <sergio@serjux.com> - 1.9-3
- Clean spec, Vascom patches series, rfbz #4199, add license tag

* Tue Jul 19 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.9-2
- use https for source URL
- enable NUMA support
- make sure Fedora compiler flags are used on ARM

* Fri Apr 08 2016 Adrian Reber <adrian@lisas.de> - 1.9-1
- Update to 1.9

* Sun Oct 25 2015 Dominik Mierzejewski <rpm@greysector.net> 1.8-2
- fix building as PIC
- update SO version in file list

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.8-1
- Update to 1.8
- Avoid tests for now

* Wed Apr 15 2015 Dominik Mierzejewski <rpm@greysector.net> 1.6-1
- update to 1.6 (ABI bump, rfbz#3593)
- release tarballs are now hosted on videolan.org
- drop obsolete patches

* Thu Dec 18 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-6
- fix build on armv7l arch (partially fix rfbz#3361, patch by Nicolas Chauvet)
- don't run tests on ARM for now (rfbz#3361)

* Sun Aug 17 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-5
- don't include contributor agreement in doc
- make sure /usr/share/doc/x265 is owned
- add a comment noting which files are BSD-licenced

* Fri Aug 08 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-4
- don't create bogus soname (patch by Xavier)

* Thu Jul 17 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-3
- fix tr call to remove DOS EOL
- build the library with -fPIC on arm and i686, too

* Sun Jul 13 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-2
- use version in source URL
- update License tag
- fix EOL in drag-uncrustify.bat
- don't link test binaries with shared binary on x86 (segfault)

* Thu Jul 10 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-1
- initial build
- fix pkgconfig file install location
- link test binaries with shared library
