%if 0%{?fedora}
%global with_python3 1
%endif

%global oname rtslib-fb

Name:           python-rtslib
License:        ASL 2.0
Group:          System Environment/Libraries
Summary:        API for Linux kernel LIO SCSI target
Version:        2.1.fb63
Release:        1%{?dist}
URL:            https://fedorahosted.org/targetcli-fb/
Source:         https://fedorahosted.org/released/targetcli-fb/%{oname}-%{version}.tar.gz
Source1:        target.service
Patch0:         0001-disable-xen_pvscsi.patch
BuildArch:      noarch
BuildRequires:  python-devel epydoc python-setuptools systemd-units
Requires:       python-kmod python-six python2-pyudev
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif

%description
API for generic Linux SCSI kernel target. Includes the 'target'
service and targetctl tool for restoring configuration.


%package doc
Summary:        Documentation for python-rtslib
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
API documentation for rtslib, to configure the generic Linux SCSI
multiprotocol kernel target.


%if 0%{?with_python3}
%package -n python3-rtslib
Summary:        API for Linux kernel LIO SCSI target
Group:          System Environment/Libraries
Requires:       python3-kmod python3-six python3-pyudev

%description -n python3-rtslib
API for generic Linux SCSI kernel target.
%endif


%package -n target-restore
Summary:        Systemd service for targetcli/rtslib
Group:          System Environment/Libraries
%if 0%{?with_python3}
Requires:       python3-rtslib = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n target-restore
Systemd service to restore the LIO kernel target settings
on system restart.


%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build
gzip --stdout doc/targetctl.8 > doc/targetctl.8.gz
gzip --stdout doc/saveconfig.json.5 > doc/saveconfig.json.5.gz
mkdir -p doc/html
epydoc --no-sourcecode --html -n rtslib -o doc/html rtslib/*.py

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
# remove py2 scripts if py3 enabled
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%{__python} setup.py install --skip-build --root %{buildroot} --install-scripts py2scripts
rm -rf %{buildroot}/py2scripts
%else
%{__python} setup.py install --skip-build --root %{buildroot}
%endif

mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/target/backup
mkdir -p %{buildroot}%{_localstatedir}/target/pr
mkdir -p %{buildroot}%{_localstatedir}/target/alua
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/target.service
install -m 644 doc/targetctl.8.gz %{buildroot}%{_mandir}/man8/
install -m 644 doc/saveconfig.json.5.gz %{buildroot}%{_mandir}/man5/

%post -n target-restore
%systemd_post target.service

%preun -n target-restore
%systemd_preun target.service

%postun -n target-restore
%systemd_postun_with_restart target.service

%files
%{python_sitelib}/*
%doc COPYING README.md doc/getting_started.md

%if 0%{?with_python3}
%files -n python3-rtslib
%{python3_sitelib}/*
%doc COPYING README.md doc/getting_started.md
%endif

%files -n target-restore
%{_bindir}/targetctl
%{_unitdir}/target.service
%dir %{_sysconfdir}/target
%dir %{_sysconfdir}/target/backup
%dir %{_localstatedir}/target
%dir %{_localstatedir}/target/pr
%dir %{_localstatedir}/target/alua
%{_mandir}/man8/targetctl.8.gz
%{_mandir}/man5/saveconfig.json.5.gz

%files doc
%doc doc/html

%changelog
* Wed Mar 1 2017 Andy Grover <agrover@redhat.com> - 2.1.fb63-1
- New upstream version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb60-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb60-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 7 2016 Andy Grover <agrover@redhat.com> - 2.1.fb60-1
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Andy Grover <agrover@redhat.com> - 2.1.fb59-1
- New upstream version

* Tue Dec 8 2015 Andy Grover <agrover@redhat.com> - 2.1.fb58-2
- Add patch 0001-disable-xen_pvscsi.patch

* Tue Dec 1 2015 Andy Grover <agrover@redhat.com> - 2.1.fb58-1
- New upstream version

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb57-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug 31 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-4
- Fix deps for python3 pkg

* Fri Aug 28 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-3
- Fix an unowned directory

* Tue Aug 18 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-2
- Move targetctl and scripts to separate 'target-restore' pkg

* Tue Jun 23 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-1
- New upstream version
- Change from 2to3 to python-six

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Andy Grover <agrover@redhat.com> - 2.1.fb53-1
- New upstream version

* Tue Jan 13 2015 Andy Grover <agrover@redhat.com> - 2.1.fb52-1
- New upstream version

* Tue Dec 2 2014 Andy Grover <agrover@redhat.com> - 2.1.fb51-1
- New upstream version

* Wed Sep 24 2014 Andy Grover <agrover@redhat.com> - 2.1.fb50-1
- New upstream version

* Thu Aug 28 2014 Andy Grover <agrover@redhat.com> - 2.1.fb49-1
- New upstream version

* Fri Jun 20 2014 Andy Grover <agrover@redhat.com> - 2.1.fb48-1
- New upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.fb47-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 14 2014 Andy Grover <agrover@redhat.com> - 2.1.fb47-1
- New upstream version

* Tue Feb 18 2014 Andy Grover <agrover@redhat.com> - 2.1.fb46-1
- New upstream version

* Wed Jan 15 2014 Andy Grover <agrover@redhat.com> - 2.1.fb45-1
- New upstream version

* Wed Dec 18 2013 Andy Grover <agrover@redhat.com> - 2.1.fb44-1
- New upstream version

* Wed Dec 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb43-1
- New upstream version
- Remove rtslib-fix-setup.patch

* Wed Nov 6 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-3
- Don't overwrite py2 scripts with py3 scripts

* Mon Nov 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-2
- Update rtslib-fix-setup.patch with backported fixups
- Add in missing systemd requires

* Fri Nov 1 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-1
- New upstream version
- Remove obsolete spec stuff: clean, buildroot
- Add target.service

* Mon Sep 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb40-1
- New upstream version, fixes restore of mappedluns

* Wed Sep 11 2013 Andy Grover <agrover@redhat.com> - 2.1.fb39-1
- New upstream version, fixes fcoe

* Tue Sep 10 2013 Andy Grover <agrover@redhat.com> - 2.1.fb38-1
- New upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb37-1
- New upstream version
- License now Apache 2.0

* Tue Jul 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb36-1
- New upstream version
- Remove fix-tabs.patch

* Fri Jun 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb35-1
- New upstream version
- add fix-tabs.patch

* Thu May 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb34-1
- New upstream version

* Thu May 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb33-1
- New upstream version
- Update source file location

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-2
- Add python3 subpackage

* Tue Apr 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-1
- New upstream version

* Tue Feb 26 2013 Andy Grover <agrover@redhat.com> - 2.1.fb30-1
- New upstream version
- Update description and summary
- Remove patch0, upstream doesn't include usb gadget any more

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb28-1
- New upstream version

* Wed Jan 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb27-1
- Specfiles removed upstream, remove handling
- Refresh no-usb.patch

* Thu Dec 20 2012 Andy Grover <agrover@redhat.com> - 2.1.fb26-1
- New upstream release
- Remove kernel dependency
- Remove python-ethtool and python-ipaddr dependencies

* Tue Nov 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb24-1
- New upstream release

* Tue Oct 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb23-1
- New upstream release

* Thu Sep 6 2012 Andy Grover <agrover@redhat.com> - 2.1.fb22-1
- New upstream release

* Wed Aug 8 2012 Andy Grover <agrover@redhat.com> - 2.1.fb21-1
- New upstream release

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-2
- Add patch no-usb.patch

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-1
- New upstream release. Add kernel version dependency.
- Don't claim python_sitelib

* Thu Aug 2 2012 Andy Grover <agrover@redhat.com> - 2.1.fb19-1
- New upstream release. Add kmod dependency.

* Tue Jul 31 2012 Andy Grover <agrover@redhat.com> - 2.1.fb18-1
- New upstream release. Remove configobj dependency

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Andy Grover <agrover@redhat.com> - 2.1.fb17-1
- New upstream release
- Remove patch retry-target-creation.patch, upstream has alternate
  fix.

* Tue Jun 12 2012 Andy Grover <agrover@redhat.com> - 2.1.fb15-1
- New upstream release

* Wed May 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb14-1
- Update Source URL to proper tarball
- Add patch retry-target-creation.patch
- New upstream release

* Mon Apr 9 2012 Andy Grover <agrover@redhat.com> - 2.1.fb13-1
- New upstream release

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-2
- Add -doc package of epydoc-generated html docs

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-1
- New upstream release

* Tue Feb 21 2012 Andy Grover <agrover@redhat.com> - 2.1.fb11-1
- New upstream release

* Fri Feb 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb9-1
- New upstream release

* Fri Feb 3 2012 Andy Grover <agrover@redhat.com> - 2.1.fb8-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb7-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb6-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb5-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb4-1
- New upstream release

* Tue Jan 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb3-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb2-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb1-1
- Change upstream URL
- New upstream release
- Remove upstreamed patches:
  * python-rtslib-git-version.patch
  * python-rtslib-use-ethtool.patch
  * python-rtslib-update-specpath.patch

* Mon Nov 14 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-8
- Change archive instructions to use gzip -n
- Fix issues raised in Fedora package review (#744349)

* Thu Oct 6 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-7
- Remove patch
  * python-rtslib-del-unused-specs.patch

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 1.99-6
- Update based on review comments
  - Fully document steps to build archive
  - Remove commented-out extraneous text
  - Remove a repeat in Requires line
  - Update git-version.patch to have proper sha1
  - Change location of fabric spec files to /var/lib/target
- Remove unused specs

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99-1
- Initial packaging
