Name:           nexus-core
Version:        2026.1.0
Release:        1%{?dist}
Summary:        NEXUS OS Core Daemons, AI Infrastructure and Spotlight Service
License:        Apache-2.0
URL:            https://github.com/nexus-os/nexus

Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust >= 1.80
BuildRequires:  cargo
BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros

Requires:       python3
Requires:       sqlite
Requires:       podman
Recommends:     ollama

%description
Core systems daemons for NEXUS OS:
- nexus-aid: Local loopback proxy (port 11430), hardware governor and credential vault
- nexus-searchd: High-speed SQLite FTS5 file and code symbol indexer

%prep
%autosetup

%build
# Build Rust components
cargo build --release

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/nexus

install -m 0755 target/release/nexus-aid %{buildroot}%{_bindir}/nexus-aid
install -m 0644 packaging/systemd/nexus-aid.service %{buildroot}%{_unitdir}/nexus-aid.service
install -m 0644 packaging/systemd/nexus-ollama.service %{buildroot}%{_unitdir}/nexus-ollama.service
install -m 0644 packaging/systemd/nexus-omniroute.service %{buildroot}%{_unitdir}/nexus-omniroute.service

%post
%systemd_post nexus-aid.service

%preun
%systemd_preun nexus-aid.service

%postun
%systemd_postun_with_restart nexus-aid.service

%files
%{_bindir}/nexus-aid
%{_unitdir}/nexus-aid.service
%{_unitdir}/nexus-ollama.service
%{_unitdir}/nexus-omniroute.service
%dir %{_sysconfdir}/nexus

%changelog
* Sun Nov 23 2026 NEXUS OS Systems Engineering <team@nexus-os.org> - 2026.1.0-1
- Production release of NEXUS OS core services.
