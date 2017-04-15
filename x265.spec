Summary:    H.265/HEVC encoder
Name:       x265
Version:    2.2
Release:    3%{?dist}
URL:        http://x265.org/
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License:    GPLv2+ and BSD

Source0:    https://bitbucket.org/multicoreware/%{name}/downloads/%{name}_%{version}.tar.gz

# link test binaries with shared library
Patch1:     x265-test-shared.patch
# fix building as PIC
Patch2:     x265-pic.patch
Patch3:     x265-high-bit-depth-soname.patch
Patch4:     x265-detect_cpu_armhfp.patch

BuildRequires:  cmake
BuildRequires:  yasm

%ifnarch armv7hl armv7hnl s390 s390x
BuildRequires:  numactl-devel
%endif

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the highest
performance on a wide variety of hardware platforms.

This package contains the command line encoder.

%package libs
Summary:    H.265/HEVC encoder library

%description libs
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library.

%package devel
Summary:    H.265/HEVC encoder library development files
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the highest
performance on a wide variety of hardware platforms.

This package contains the shared library development files.

%prep
%autosetup -p1 -n %{name}_%{version}

%build
# High depth libraries (from source/h265.h):
#   If the requested bitDepth is not supported by the linked libx265,
#   it will attempt to dynamically bind x265_api_get() from a shared
#   library with an appropriate name:
#     8bit:  libx265_main.so
#     10bit: libx265_main10.so

build() {
%cmake -G "Unix Makefiles" \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    $* \
    ../source
%make_build
}

# High depth 10/12 bit libraries are supported only on 64 bit. They require
# disabled AltiVec instructions for building on ppc64/ppc64le.
%ifarch x86_64 aarch64 ppc64 ppc64le
mkdir 10bit; pushd 10bit
    build -DENABLE_CLI=OFF -DENABLE_ALTIVEC=OFF -DHIGH_BIT_DEPTH=ON
popd

mkdir 12bit; pushd 12bit
    build -DENABLE_CLI=OFF -DENABLE_ALTIVEC=OFF -DHIGH_BIT_DEPTH=ON -DMAIN12=ON
popd
%endif

# 8 bit base library + encoder
mkdir 8bit; pushd 8bit
    build
popd

%install
for i in 8 10 12; do
    if [ -d ${i}bit ]; then
        pushd ${i}bit
            %make_install
            # Remove unversioned library, should not be linked to
            rm -f %{buildroot}%{_libdir}/libx265_main${i}.so
        popd
    fi
done

find %{buildroot} -name "*.a" -delete

%check
for i in 8 10 12; do
    if [ -d ${i}bit ]; then
        pushd ${i}bit
            LD_LIBRARY_PATH=%{buildroot}%{_libdir} test/TestBench || :
        popd
    fi
done

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/x265

%files libs
%license COPYING
%{_libdir}/libx265.so.102
%ifarch x86_64 aarch64 ppc64 ppc64le
%{_libdir}/libx265_main10.so.102
%{_libdir}/libx265_main12.so.102
%endif

%files devel
%doc doc/*
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Mon Apr 10 2017 Simone Caronni <negativo17@gmail.com> - 2.2-3
- Use source from multicoreware website.
- Clean up SPEC file a bit (formatting, 80 char wide descriptions).
- Enable shared 10/12 bit libraries on 64 bit architectures.

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
