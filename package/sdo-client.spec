#
# spec file for package sdo-client
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           sdo-client
Version:        1.0.0+git20201201.e57e7ca
Release:        0
Summary:        Secure Device Onboard Client
License:        Apache-2.0
Group:          System/Base
URL:            https://github.com/intel/safestringlib/tree/v1.0.0
Source0:        sdo-client-%{version}.tar.xz
Source1:        safestringlib-1.0.0+git20171208.5da1bad.tar.xz
Source2:        sdo-client-service
Source3:        sdoclient.service
Source4:        README
Patch0:         build.patch
Requires:       openssl
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libopenssl-devel
%{?systemd_ordering}

%description
SDO-Client is a portable implementation of the Secure Device Onboarding
(SDO) protocol. This component is portable across multiple environments,
including to various microprocessors (MPUs) and microcontrollers (MCUs).

%package devel
Summary:        Secure Device Onboard Client SDK
Group:          Development/Libraries/C and C++
Requires:       libopenssl-1_1-devel

%description devel
SDO-Client is a portable implementation of the Secure Device Onboarding
(SDO) protocol. This component is portable across multiple environments,
including to various microprocessors (MPUs) and microcontrollers (MCUs).
This package contains all necessary include files and libraries needed
to develop applications that needs to read configuration files from
different locations.

%prep
%setup -q
%setup -q -a 1
%patch0 -p1

%build
cd safestringlib*
mkdir obj
make
cd %{_builddir}/%{name}*
export SAFESTRING_ROOT=%{_builddir}/%{name}-%{version}/safestringlib-1.0.0+git20171208.5da1bad
export BLOB_PATH=%{_sharedstatedir}/%{name}
export RO_BLOB_PATH=%{_datadir}/%{name}
cmake -DTARGET_OS=linux -DBUILD=debug -DMODULES=true .
make
echo -n "8080" > %{_builddir}/%{name}-%{version}/data/manufacturer_port.bin

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_docdir}/%{name}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_datadir}/%{name}/data
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}/data

%{__install} -m 0755 build/linux-client %{buildroot}/%{_bindir}/%{name}
%{__install} -m 0755 %{SOURCE2} %{buildroot}/%{_bindir}/sdo-client-service
%{__install} -D -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}/sdoclient.service
%{__install} -m 0644 %{SOURCE4} %{buildroot}/%{_docdir}/%{name}/README
ln -sf %{_sbindir}/service %{buildroot}%{_sbindir}/rcsdoclient

%{__install} build/*.a %{buildroot}/%{_libdir}
%{__install} include/*.h %{buildroot}/%{_includedir}

%{__install} data/ecdsa* %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/epidprivkey.dat %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/manufacturer* %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/mfg_proxy.dat %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/owner_proxy.dat %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/raw.blob %{buildroot}/%{_datadir}/%{name}/data
%{__install} data/rv_proxy.dat %{buildroot}/%{_datadir}/%{name}/data

%{__install} data/Mfg.blob %{buildroot}/%{_sharedstatedir}/%{name}/data
%{__install} data/Normal.blob %{buildroot}/%{_sharedstatedir}/%{name}/data
%{__install} data/platform_aes_key.bin %{buildroot}/%{_sharedstatedir}/%{name}/data
%{__install} data/platform_hmac_key.bin %{buildroot}/%{_sharedstatedir}/%{name}/data
%{__install} data/platform_iv.bin %{buildroot}/%{_sharedstatedir}/%{name}/data
%{__install} data/Secure.blob %{buildroot}/%{_sharedstatedir}/%{name}/data

%pre
%service_add_pre sdoclient.service

%preun
%service_del_preun sdoclient.service

%post
%service_add_post sdoclient.service

%postun
%service_del_postun sdoclient.service

%files
%license LICENSE
%doc README
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/data/
%{_bindir}/%{name}
%{_bindir}/sdo-client-service
%{_datadir}/%{name}/data/*
%{_sharedstatedir}/%{name}/data/*
%{_unitdir}/sdoclient.service
%{_sbindir}/rcsdoclient

%files devel
%license LICENSE
%{_includedir}/*.h
%{_libdir}/*.a

%changelog
