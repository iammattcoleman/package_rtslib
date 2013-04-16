%if 0%{?fedora}
%global with_python3 1
%endif

%global oname rtslib-fb

Name:           python-rtslib
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        API for Linux kernel LIO SCSI target
Version:        2.1.fb32
Release:        2%{?dist}
URL:            https://github.com/agrover/rtslib-fb/
# Acquire with
# wget --content-disposition https://github.com/agrover/%{oname}/archive/v%{version}.tar.gz
# and it will save with the name below. Not cool, github.
Source:         https://github.com/agrover/%{oname}/archive/%{oname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel epydoc
Requires:       python-kmod

%if 0%{?with_python3}
BuildRequires:  python3-devel python-tools
%endif

%package doc
Summary:        Documentation for python-rtslib
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description
API for generic Linux SCSI kernel target.

%description doc
API documentation for rtslib, to configure the generic Linux SCSI
multiprotocol kernel target.

%if 0%{?with_python3}
%package -n python3-rtslib
Summary:        API for Linux kernel LIO SCSI target
Group:          System Environment/Libraries

%description -n python3-rtslib
API for generic Linux SCSI kernel target.
%endif

%prep
%setup -q -n %{oname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build
mkdir -p doc/html
epydoc --no-sourcecode --html -n rtslib -o doc/html rtslib/*.py

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --write --nobackups .
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%doc COPYING README

%if 0%{?with_python3}
%files -n python3-rtslib
%{python3_sitelib}/*
%doc COPYING README
%endif

%files doc
%doc doc/html

%changelog
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
