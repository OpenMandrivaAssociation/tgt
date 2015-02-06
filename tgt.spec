%bcond_without iser
%bcond_with fcoe

Name:           tgt
Version:        1.0.33
Release:        2
Summary:        The SCSI target daemon and utility programs
Group:          Networking/Other
License:        GPL
URL:            http://stgt.sourceforge.net/
Source0:        http://stgt.sourceforge.net/releases/%{name}-%{version}.tar.gz
# initscript stolen from fedora
Source1:        tgtd.init
%if %with iser
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
buildrequires:  librdmacm
buildrequires:  xsltproc
Suggests:	libibverbs1, librdmacm
%endif

%description
The SCSI target package contains the daemon and tools to setup a SCSI targets.
Currently, software iSCSI targets are supported.

%prep
%setup -q -n tgt-%{version}

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
%{_sysconfdir}/tgt/examples


%changelog
* Sat Mar 13 2010 Luca Berra <bluca@mandriva.org> 1.0.2-2mdv2010.1
+ Revision: 518663
- add FCOE support
- really make iSer optional
- make tgt-setup-lun executable (debian)

* Fri Mar 12 2010 Luca Berra <bluca@mandriva.org> 1.0.2-1mdv2010.1
+ Revision: 518602
- create tgt

