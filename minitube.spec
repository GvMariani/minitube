%global debug_package %{nil}

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# Note: these are for OpenMandriva use ONLY.
# For your own builds, please get your own set of keys.
%define    google_api_key AIzaSyDlD0VWLAKJn_2zjq4X70wDy8Ra7YIIuoM

Name:		minitube
Version:	3.9.3
Release:	2
Summary:	A native YouTube client
Group:		Video/Players
License:	GPLv3+
URL:		https://flavio.tordini.org/minitube
Source0:	https://github.com/flaviotordini/minitube/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch0:		minitube-use-system-qtsingleapplication.patch
Patch1:		fix-build-with-mpv035.patch

BuildRequires:	make
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(phonon4qt5)
BuildRequires:	qt5-qttools
BuildRequires:	pkgconfig(libvlc)
BuildRequires:	pkgconfig(mpv)
BuildRequires:  pkgconfig(tgvoip)
BuildRequires:	qtsingleapplication-qt5-devel
BuildRequires:	qt5-linguist-tools
# minitube no longer supports anything other than the vlc phonon.
Requires:	phonon4qt5-vlc
Requires:	vlc-plugin-gnutls
Requires:	qt5-database-plugin-sqlite

%description
Minitube is a native YouTube client. With it you can watch YouTube videos in
a new way: you type a keyword, Minitube gives you an endless video stream.
Minitube does not require the Flash Player.

Minitube is not about cloning the original Youtube web interface, it strives
to create a new TV-like experience.

%prep
%autosetup -p1

# more debug msgs
sed -i -e '/QT_NO_DEBUG_OUTPUT/d' minitube.pro

# remove bundled qtsingleapplication
rm -r src/qtsingleapplication

%build
%qmake_qt5 \
	PREFIX=%{_prefix} \
	USE_SYSTEM_QTSINGLEAPPLICATION=1 \
	DEFINES+=APP_GOOGLE_API_KEY=%{google_api_key}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

# fix .desktop file
desktop-file-edit \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc TODO CHANGES AUTHORS
%{_bindir}/minitube
%{_datadir}/minitube/
%{_datadir}/metainfo/org.tordini.flavio.minitube.metainfo.xml
%{_datadir}/applications/minitube.desktop
%{_iconsdir}/hicolor/*/apps/minitube.*
