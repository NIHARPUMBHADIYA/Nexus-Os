Name:           nexus-desktop
Version:        2026.1.0
Release:        1%{?dist}
Summary:        NEXUS OS Aether Desktop Shell and Theme Personalization Engine
License:        MIT
URL:            https://github.com/nexus-os/nexus

Source0:        %{name}-%{version}.tar.gz

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  python3-devel

Requires:       plasma-workspace-wayland
Requires:       kwin-wayland
Requires:       pipewire
Requires:       python3-pyqt6
Requires:       qt6-qtquickcontrols2
Requires:       nexus-core >= 2026.1.0

%description
NEXUS OS Aether Desktop Shell featuring:
- Rounded window management and floating dock
- 10 semantic Aether themes (Midnight, Nord, Tokyo Night, Paper Light, AMOLED Black)
- Universal Spotlight Launcher (Win+Space)
- System Quick Settings and Notification Center
- Built-in Developer Hub and Software Center

%prep
%autosetup

%build
# QML and Python runtime package (pure arch-independent or arch-specific data)

%install
mkdir -p %{buildroot}%{_datadir}/nexus
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_bindir}

cp -r src %{buildroot}%{_datadir}/nexus/
install -m 0755 tools/run_desktop.py %{buildroot}%{_bindir}/nexus-desktop
install -m 0755 tools/run_settings.py %{buildroot}%{_bindir}/nexus-settings
install -m 0755 tools/run_spotlight.py %{buildroot}%{_bindir}/nexus-spotlight

%files
%{_bindir}/nexus-desktop
%{_bindir}/nexus-settings
%{_bindir}/nexus-spotlight
%{_datadir}/nexus

%changelog
* Sun Nov 23 2026 NEXUS OS Systems Engineering <team@nexus-os.org> - 2026.1.0-1
- Initial packaging of NEXUS Aether Desktop Shell.
