Summary:	IBM Advanced System Management drivers
Summary(pl):	Sterowniki do Advanced System Management w sprzêcie IBM-a
Name:		ibmasm
Version:	1.0
%define _rel	2
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
# Taken from CD I got with IBM server
Source0:	%{name}-src-redhat.tgz
URL:		http://www.ibm.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/

%description
Utilities for IBM Advanced System Management Drivers.

%description -l pl
Narzêdzia do sterowników do zaawansowanego zarz±dzania systemem
(Advanced System Management) w maszynach IBM-a.

%package -n kernel-misc-ibmasm
Summary:	IBM Advanced System Management drivers
Summary(pl):	Sterowniki do Advanced System Management w sprzêcie IBM-a
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel

%description -n kernel-misc-ibmasm
IBM Advanced System Management drivers.

%description -n kernel-misc-ibmasm -l pl
Sterowniki do zaawansowanego zarz±dzania systemem (Advanced System
Management) w maszynach IBM-a.

%package -n kernel-smp-misc-ibmasm
Summary:	IBM Advanced System Management SMP drivers
Summary(pl):	Sterowniki SMP do Advanced System Management w sprzêcie IBM-a
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel

%description -n kernel-smp-misc-ibmasm
IBM Advanced System Management SMP drivers.

%description -n kernel-smp-misc-ibmasm -l pl
Sterowniki SMP do zaawansowanego zarz±dzania systemem (Advanced System
Management) w maszynach IBM-a.

%prep
%setup -q -n %{name}-src
chmod -R u+rwX *

%build
cd src
%{__make} \
	INC="%{_kernelsrcdir}/include" \
	CPU=%{arch} \
	DEBFLAGS="%{rpmcflags} -D__SMP__"
install -d ../smp
cp ibmasm.o ibmser.o ../smp

%{__make} \
	INC="%{_kernelsrcdir}/include" \
	CPU=%{arch} \
	DEBFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}}

install shlib/libsysSp.so $RPM_BUILD_ROOT%{_libdir}
install exe/{ibmsphalt,ibmsprem,ibmsptxt} $RPM_BUILD_ROOT%{_sbindir}

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install src/{ibmasm.o,ibmser.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install smp/{ibmasm.o,ibmser.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-misc-ibmasm
/sbin/depmod -F /boot/System.map -a

%postun -n kernel-misc-ibmasm
/sbin/depmod -F /boot/System.map -a

%post -n kernel-smp-misc-ibmasm
/sbin/depmod -F /boot/System.map -a

%postun -n kernel-smp-misc-ibmasm
/sbin/depmod -F /boot/System.map -a

%files
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*

%files -n kernel-misc-ibmasm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-ibmasm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
