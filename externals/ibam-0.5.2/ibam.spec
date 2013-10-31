%define version 0.4
%define release 1

Summary: Intelligent Battery Monitor
Name: ibam
Version: %{version}
Release: %{release}
Copyright: GPL
Group: Utilities/System
Source: http://prdownloads.sourceforge.net/ibam/ibam-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-buildroot

%description
IBAM is an advanced battery monitor for laptops, which uses statistical and
adaptive linear methods to provide accurate estimations of minutes of
battery left or of the time needed until full recharge.

%prep
%setup -q
%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ibam krell

%install
install -m 0755 -d $RPM_BUILD_ROOT/usr
install -m 0755 -d $RPM_BUILD_ROOT/usr/local
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/bin
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/lib
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/lib/gkrellm
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/lib/gkrellm/plugins
make install PREFIX=$RPM_BUILD_ROOT/usr

%files
%defattr (-,root,root)
/usr/local/bin/ibam
/usr/local/lib/gkrellm/plugins
