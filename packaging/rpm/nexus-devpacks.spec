Name:           nexus-devpacks
Version:        2026.1.0
Release:        1%{?dist}
Summary:        NEXUS OS Curated Developer Environment Packs
License:        Apache-2.0
URL:            https://github.com/nexus-os/nexus

Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

Requires:       python3
Requires:       python3-pyqt6
Requires:       nexus-core >= 2026.1.0
Requires:       podman
Requires:       git

%description
NEXUS OS Developer Packs provides 15 curated one-click development environments
(Full-Stack, AI/ML, Vibe Coder, Robotics, Embedded, Cybersecurity, DevOps, etc.)
with automated dependency resolution and zero-conflict deduplication.

%prep
%autosetup

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 tools/run_devpacks.py %{buildroot}%{_bindir}/nexus-devpacks

%files
%{_bindir}/nexus-devpacks

%changelog
* Sun Nov 23 2026 NEXUS OS Systems Engineering <team@nexus-os.org> - 2026.1.0-1
- Initial release of Developer Packs orchestrator.
