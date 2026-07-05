%global debug_package %{nil}

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# Note: these are for OpenMandriva use ONLY.
# For your own builds, please get your own set of keys.
%define    google_api_key AIzaSyDlD0VWLAKJn_2zjq4X70wDy8Ra7YIIuoM

Summary:		A native YouTube client
Name:		minitube
Version:		4.0
Release:		1
Group:		Video/Players
License:		GPLv3+
Url:		https://flavio.tordini.org/minitube
Source0:	https://github.com/flaviotordini/minitube/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch0:		minitube-4.0-fix-mpvwidget.patch
#Patch1:		fix-build-with-mpv035.patch
BuildRequires:		desktop-file-utils
BuildRequires:		make
BuildRequires:		qmake-qt6
BuildRequires:		qt6-qttools-linguist
BuildRequires:		qt6-qttools
BuildRequires:		pkgconfig(libvlc)
BuildRequires:		pkgconfig(mpv)
BuildRequires:		pkgconfig(phonon4qt6)
BuildRequires:		pkgconfig(Qt6Core)
BuildRequires:		pkgconfig(Qt6DBus)
BuildRequires:		pkgconfig(Qt6Gui)
BuildRequires:		pkgconfig(Qt6Network)
BuildRequires:		pkgconfig(Qt6OpenGL)
BuildRequires:		pkgconfig(Qt6OpenGLWidgets)
BuildRequires:		pkgconfig(Qt6Qml)
BuildRequires:		pkgconfig(Qt6Sql)
BuildRequires:		pkgconfig(Qt6Widgets)
BuildRequires:		pkgconfig(tgvoip)
# Minitube no longer supports anything other than the vlc phonon.
Requires:	phonon4qt6-vlc
Requires:	vlc-plugin-gnutls
Requires:	qt5-database-plugin-sqlite

%description
This is a native YouTube client. With it you can watch YouTube videos in a new
way: you type a keyword, the program gives you an endless video stream.
It does not require the Flash Player and it strives to create a new TV-like
experience. It is not about cloning the original Youtube web interface.

%files
%doc TODO CHANGES AUTHORS
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/metainfo/org.tordini.flavio.%{name}.metainfo.xml
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*

#-----------------------------------------------------------------------------

%prep
%autosetup -p1

# More debug msgs
sed -i -e '/QT_NO_DEBUG_OUTPUT/d' minitube.pro

# Remove bundled qtsingleapplication: we use the system one
#rm -r src/qtsingleapplication


%build
#USE_SYSTEM_QTSINGLEAPPLICATION=1 \
%set_build_flags
qmake-qt6 \
	PREFIX=%{_prefix} \
	DEFINES+=APP_GOOGLE_API_KEY=%{google_api_key}
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}

# Fix .desktop file
desktop-file-edit --remove-category="Network" %{buildroot}%{_datadir}/applications/%{name}.desktop
