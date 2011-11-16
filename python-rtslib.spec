%global oname rtslib

Name:           python-rtslib
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        API for RisingTide Systems generic SCSI target
Version:        1.99.1.git644eece
Release:        8%{?dist}
# placeholder URL and source entries
# archive created using:
# git clone git://risingtidesystems.com/rtslib.git
# cd rtslib
# git archive 644eece --prefix rtslib-%{version}/ | gzip -n > rtslib-%{version}.tar.gz
URL:            http://www.risingtidesystems.com/git/
Source:         %{oname}-%{version}.tar.gz
Patch1:         %{name}-git-version.patch
Patch2:         %{name}-use-ethtool.patch
Patch3:         %{name}-update-specpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-ipaddr python-ethtool python-configobj python-devel
Requires:       python-ipaddr python-ethtool python-configobj

%description
API for RisingTide Systems generic SCSI target.

%prep
%setup -q -n %{oname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__python} setup.py build

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

%changelog
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
