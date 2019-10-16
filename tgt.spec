Name:           tgt
Version:        1.0.79
Release:        1
Summary:        The SCSI target daemon and utility programs
License:        GPLv2
Group:          Networking/Other
URL:            http://stgt.sourceforge.net/
Source0:        https://github.com/fujita/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        tgtd.service
Source2:        sysconfig.tgtd
Source3:        targets.conf
Source4:        sample.conf
Source5:        tgtd.conf

BuildRequires:  docbook-style-xsl
BuildRequires:  libaio-devel
BuildRequires:  libxslt-devel
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  xsltproc

%description
The SCSI target package contains the daemon and tools to setup a SCSI targets.
Currently, software iSCSI targets are supported.

%prep
%autosetup -p1

%build
%make_build 

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_mandir}/man5
%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/tgt
%{__install} -d %{buildroot}%{_sysconfdir}/tgt/conf.d
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig

%{__install} -p -m 0755 scripts/tgt-setup-lun %{buildroot}%{_sbindir}
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}
%{__install} -p -m 0755 scripts/tgt-admin %{buildroot}/%{_sbindir}/tgt-admin
%{__install} -p -m 0644 doc/manpages/targets.conf.5 %{buildroot}/%{_mandir}/man5
%{__install} -p -m 0644 doc/manpages/tgtadm.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0644 doc/manpages/tgt-admin.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0644 doc/manpages/tgt-setup-lun.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/tgtd
%{__install} -p -m 0600 %{SOURCE3} %{buildroot}%{_sysconfdir}/tgt
%{__install} -p -m 0600 %{SOURCE4} %{buildroot}%{_sysconfdir}/tgt/conf.d
%{__install} -p -m 0600 %{SOURCE5} %{buildroot}%{_sysconfdir}/tgt

pushd usr
%make_install PREFIX=%{_prefix}

#post
#systemd_post tgtd.service

#preun
#systemd_preun tgtd.service

#postun
# don't restart daemon on upgrade
#systemd_postun

%files
%doc README doc/README.iscsi doc/README.iser doc/README.lu_configuration doc/README.mmc doc/README.ssc
%{_sbindir}/tgt-setup-lun
%{_sbindir}/tgt-admin
%{_sbindir}/tgtadm
%{_sbindir}/tgtimg
%{_sbindir}/tgtd
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_unitdir}/tgtd.service
%{_sysconfdir}/tgt
%{_sysconfdir}/tgt/conf.d
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/tgtd
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tgt/targets.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tgt/tgtd.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tgt/conf.d/sample.conf
