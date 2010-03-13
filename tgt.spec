%bcond_without iser
%bcond_with fcoe

Name:           tgt
Version:        1.0.2
Release:        %mkrel 3
Summary:        The SCSI target daemon and utility programs
Group:          Networking/Other
License:        GPL
URL:            http://stgt.sourceforge.net/
Source0:        http://stgt.sourceforge.net/releases/%{name}-%{version}.tar.gz
# initscript stolen from fedora
Source1:        tgtd.init
# from git
Patch100:	tgt-1.0.2-tgtimg_man.patch
# Patch1 adapted from fedora
Patch1:         scsi-target-utils-dynamic-link-iser.patch
Patch2:		tgt-1.0.2-warnings.patch
# Patch3 from debian
Patch3:		make-tgt-setup-lun-executable
BuildRoot:	%{_tmppath}/%{name}-%{version}
%if %with iser
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
Suggests:	libibverbs1, librdmacm
%endif

%description
The SCSI target package contains the daemon and tools to setup a SCSI targets.
Currently, software iSCSI targets are supported.

%prep
%setup -q -n tgt-%{version}
%patch100 -p1
%if %with iser
%patch1 -p1 -b .dynamic-link-iser
%endif
%patch2 -p1 -b .warnings
%patch3 -p1 -b .perl

sed -i -e 's/-g -O2/$(RPM_OPT_FLAGS)/' usr/Makefile

%build
%make RPM_OPT_FLAGS="%{optflags} -fno-strict-aliasing" \
%if %with iser
ISCSI_RDMA=1 \
%endif
%if %with fcoe
FCOE=1 \
%endif
ISCSI=1

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_initrddir}
install %{SOURCE1} %{buildroot}%{_initrddir}/tgtd

%post
%_post_service tgtd

%preun
%_preun_service tgtd

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, root)
%doc README doc/README.* doc/*.txt conf/examples/*
%{_sbindir}/tgtd
%{_sbindir}/tgtadm
%{_sbindir}/tgt-setup-lun
%{_sbindir}/tgt-admin
%{_sbindir}/tgtimg
%{_mandir}/man8/*
%{_initrddir}/tgtd
%config(noreplace) %{_sysconfdir}/tgt/targets.conf
%exclude %{_sysconfdir}/tgt/examples
