%global gitdate 20140411

%global commit 6eb075c70e2f91a9c45a90677bd46e8fb0432655
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Direct Rendering Manager runtime library
Name: libepoxy
Version: 1.2
Release: 0.2.%{gitdate}git%{shortcommit}%{?dist}
License: MIT
URL: http://github.com/anholt/libepoxy
# github url - generated archive
Source0: https://github.com/anholt/libepoxy/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires: pkgconfig automake autoconf libtool
BuildRequires: mesa-libGL-devel mesa-libEGL-devel
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
%setup -qn %{name}-%{commit}

%build
autoreconf -fiv || exit 1
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete -print

%check
make check

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
* Fri Apr 11 2014 Dave Airlie <airlied@redhat.com> 1.2-0.2.20140411git6eb075c
- update to latest git snapshot

* Thu Mar 27 2014 Dave Airlie <airlied@redhat.com> 1.2-0.1.20140307gitd4ad80f
- initial git snapshot

