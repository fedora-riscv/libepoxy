#global gitdate 20140411

%global commit e2c33af5bfcfc9d168f9e776156dd47c33f428b3
#global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: epoxy runtime library
Name: libepoxy
Version: 1.3.1
Release: 4%{?dist}
License: MIT
URL: http://github.com/anholt/libepoxy
# github url - generated archive
#ource0: https://github.com/anholt/libepoxy/archive/%{commit}/%{name}-%{commit}.tar.gz
Source0: https://github.com/anholt/libepoxy/archive/v%{version}/v%{version}.tar.gz

Patch0: 0001-egl-Be-somewhat-aware-of-EGL-client-extensions.patch

BuildRequires: automake autoconf libtool
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: python3

%description
A library for handling OpenGL function pointer management.

%package devel
Summary: Development files for libepoxy
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .clientext

%build
autoreconf -vif || exit 1
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete -print

%check
# In theory this is fixed in 1.2 but we still see errors on most platforms
# https://github.com/anholt/libepoxy/issues/24
%ifnarch %{arm} aarch64 %{power64} s390x
make check
%else
make check ||:
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_libdir}/libepoxy.so.0
%{_libdir}/libepoxy.so.0.0.0

%files devel
%dir %{_includedir}/epoxy/
%{_includedir}/epoxy/*
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Adam Jackson <ajax@redhat.com> - 1.3.1-3
- Fix detection of EGL client extensions

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 05 2015 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libepoxy 1.3.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Dave Airlie <airlied@redhat.com> 1.2-3
- update GL registry files (add new EGL extension)

* Wed Mar 25 2015 Adam Jackson <ajax@redhat.com> 1.2-2
- Fix description to not talk about DRM
- Sync some small bugfixes from git

* Mon Oct 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- Update to 1.2 GA
- Don't fail build on make check failure for some architectures

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Dave Airlie <airlied@redhat.com> 1.2-0.2.20140411git6eb075c
- update to latest git snapshot

* Thu Mar 27 2014 Dave Airlie <airlied@redhat.com> 1.2-0.1.20140307gitd4ad80f
- initial git snapshot

