
%define		_rel	2

Summary:	IBM Advanced System Management Drivers
Name:		ibmasm
Version:	1.0
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
# Taken from CD I got with IBM server
Source0:	%{name}-src-redhat.tgz
URL:		http://www.ibm.com
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/

%description
Utilities for IBM Advanced System Management Drivers

%package -n kernel-misc-ibmasm
Summary:	IBM Advanced System Management Drivers
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel

%description -n kernel-misc-ibmasm
IBM Advanced System Management Drivers

%package -n kernel-smp-misc-ibmasm
Summary:	IBM Advanced System Management Drivers
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel

%description -n kernel-smp-misc-ibmasm
IBM Advanced System Management Drivers

%prep
%setup -q -n %{name}-src
chmod -R u+rwX *

%build
cd src
make \
	INC=/usr/src/linux/include \
	CPU=%{arch} \
	DEBFLAGS="-O2 -D__SMP__"
install -d ../smp
cp ibmasm.o ibmser.o ../smp

make \
	INC=/usr/src/linux/include \
	CPU=%{arch} \
	DEBFLAGS="-O2"
cd ..

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
