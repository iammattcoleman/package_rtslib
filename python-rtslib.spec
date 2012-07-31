%global oname rtslib-fb

Name:           python-rtslib
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        API for RisingTide Systems generic SCSI target
Version:        2.1.fb18
Release:        1%{?dist}
URL:            https://github.com/agrover/rtslib-fb/
Source:         https://github.com/downloads/agrover/%{oname}/%{oname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-ipaddr python-ethtool python-devel epydoc
Requires:       python-ipaddr python-ethtool

%package doc
Summary:	Documentation for python-rtslib
Group:		Documentation
Requires:	%{name} = %{version}-%{release}


%description
API for generic Linux SCSI kernel target.

%description doc
API documentation for rtslib, to configure the generic Linux SCSI
kernel target.

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build
mkdir -p doc/html
epydoc --no-sourcecode --html -n rtslib -o doc/html rtslib/*.py

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/var/lib/target/fabric
cp specs/* %{buildroot}/var/lib/target/fabric


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}
/var/lib/target
%doc COPYING README

%files doc
%doc doc/html

%changelog
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

* Fri Feb 8 2012 Andy Grover <agrover@redhat.com> - 2.1.fb9-1
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
