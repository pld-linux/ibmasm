Summary:	IBM Advanced System Management drivers
Summary(pl.UTF-8):	Sterowniki do Advanced System Management w sprzęcie IBM-a
Name:		ibmasm
Version:	3.0
Release:	0.1
License:	LGPL v2 and GPL v2+
Group:		Applications/System
Source0:	%{name}_user_%{version}.tar.bz2
URL:		http://sourceforge.net/projects/ibmasm/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the tools necessary to control the IBM Advanced
System Management Drivers

%package devel
Summary:	Development environment for the IBM Advanced System Management user-land driver
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The ibmasm-devel package contains the development libraries and header
files of the IBM Advanced System Management drivers

%prep
%setup -q -n %{name}_user_%{version}

%build
%{__make} -C ibmasm/src
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C ibmasm/src install \
	_LIB=%{_libdir} \
	ROOT=$RPM_BUILD_ROOT

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_includedir}/ibmasm
cp -a ibmasm/src/api/libibmasm.h ${RPM_BUILD_ROOT}%{_includedir}/ibmasm
cp -a ibmasm/src/api/rsa.h ${RPM_BUILD_ROOT}%{_includedir}/ibmasm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ibmasm/src/README
%attr(755,root,root) %{_bindir}/evnode
%attr(755,root,root) %{_sbindir}/ibmsphalt
%attr(755,root,root) %{_sbindir}/ibmspup
%attr(755,root,root) %{_libdir}/libsysSp.so.3.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsysSp.so
%{_includedir}/ibmasm
