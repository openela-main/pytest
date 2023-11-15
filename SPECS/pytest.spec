%bcond_without python3

%global pylib_version 1.4.29

Name:           pytest
Version:        3.4.2
Release:        13%{?dist}
Summary:        Simple powerful testing with Python
License:        MIT
URL:            http://pytest.org
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

# The tests in this specfile use pytest-timeout
# When building pytest for the first time with new Python version
# that is not possible as it depends on pytest.
# It's also not possible on systems that don't build pytest-timeout at all.
%bcond_with timeout

BuildArch:      noarch

%description
py.test provides simple, yet powerful testing for Python.

%package -n python2-%{name}
Summary:        Simple powerful testing with Python
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-setuptools_scm
BuildRequires:  python2-py >= %{pylib_version}
BuildRequires:  python2-attrs
%if %{with timeout}
BuildRequires:  python2-pytest-timeout
%endif
BuildRequires:  python2-pluggy
BuildRequires:  python2-funcsigs
BuildRequires:  python2-six
Requires:       python2-attrs
Requires:       python2-funcsigs
Requires:       python2-pluggy
Requires:       python2-six
Requires:       python2-setuptools
Requires:       python2-py >= %{pylib_version}
%{?python_provide:%python_provide python2-%{name}}
Obsoletes:      %{name} < 2.8.7-3

%description -n python2-%{name}
py.test provides simple, yet powerful testing for Python.

%if %{with python3}
%package -n python3-%{name}
Summary:        Simple powerful testing with Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-py >= %{pylib_version}
BuildRequires:  python3-hypothesis
BuildRequires:  python3-attrs
%if %{with timeout}
BuildRequires:  python3-pytest-timeout
%endif
BuildRequires:  python3-pluggy
BuildRequires:  python3-six
Requires:       python3-attrs
Requires:       python3-pluggy
Requires:       python3-six
Requires:       python3-setuptools
Requires:       python3-py >= %{pylib_version}
%{?python_provide:%python_provide python3-%{name}}
Obsoletes:      platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
py.test provides simple, yet powerful testing for Python.

%endif

%prep
%autosetup

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python2_version}
ln -snf pytest-%{python2_version} %{buildroot}%{_bindir}/pytest-2
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python2_version}
ln -snf py.test-%{python2_version} %{buildroot}%{_bindir}/py.test-2
%if %{with python3}
%py3_install
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python3_version}
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest-3
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python3_version}
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test-3
%endif

# remove shebangs from all scripts - python 2
find %{buildroot}%{python2_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

%if %{with python3}
# remove shebangs from all scripts - python 3
find %{buildroot}%{python3_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;
%endif

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
# Skip "metafunc" tests, since these require pythyon2-hypothesis
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{buildroot}%{_bindir}/pytest-%{python2_version} -r s testing \
  -k 'not non_ascii_paste_text' \
  --ignore 'testing/python/metafunc.py' \
  %if %{with timeout}
  --timeout=30
  %endif

%if %{with python3}
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/pytest-%{python3_version} -r s testing \
  -k 'not non_ascii_paste_text' \
  %if %{with timeout}
  --timeout=30
  %endif
%endif

%files -n python2-%{name}
%doc CHANGELOG.rst
%doc README.rst
%doc CONTRIBUTING.rst
%license LICENSE
%{_bindir}/pytest-2
%{_bindir}/pytest-%{python2_version}
%{_bindir}/py.test-2
%{_bindir}/py.test-%{python2_version}
%{python2_sitelib}/pytest-*.egg-info/
%{python2_sitelib}/_pytest/
%{python2_sitelib}/pytest.py*

%if %{with python3}
%files -n python3-%{name}
%doc CHANGELOG.rst
%doc README.rst
%doc CONTRIBUTING.rst
%license LICENSE
%{_bindir}/pytest-3
%{_bindir}/pytest-%{python3_version}
%{_bindir}/py.test-3
%{_bindir}/py.test-%{python3_version}
%{python3_sitelib}/pytest-*.egg-info/
%{python3_sitelib}/_pytest/
%{python3_sitelib}/pytest.py
%{python3_sitelib}/__pycache__/pytest.*
%endif

%changelog
* Thu Apr 25 2019 Tomas Orsava <torsava@redhat.com> - 3.4.2-13
- Bumping due to problems with modular RPM upgrade path
- Resolves: rhbz#1695587

* Tue Oct 09 2018 Lumír Balhar <lbalhar@redhat.com> - 3.4.2-12
- Remove unversioned provides
- Resolves: rhbz#1628242

* Wed Aug 08 2018 Lumír Balhar <lbalhar@redhat.com> - 3.4.2-11
- Remove unversioned binaries from python2 subpackage
- Resolves: rhbz#1613343

* Tue Jul 31 2018 Lumír Balhar <lbalhar@redhat.com> - 3.4.2-10
- Make possible to disable python3 subpackage

* Fri Jul 13 2018 Lumír Balhar <lbalhar@redhat.com> - 3.4.2-9
- First version for python27 module

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-8
- Allow Python 2 for build
  see https://hurl.corp.redhat.com/rhel8-py2

* Fri Jun 22 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-7
- Remove BuildRequires on python2-hypothesis, a circular dependency
- Explicitly BuildRequire python-attrs

* Tue Jun 19 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-6
- Don't use timeout in tests
  https://bugzilla.redhat.com/show_bug.cgi?id=1592940
- Add missing BuildRequires

* Thu Jun 07 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-5
- Remove optional BuildRequires for %%check
  https://bugzilla.redhat.com/show_bug.cgi?id=1588445

* Mon May 28 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-4
- Drop python2-argcomplete from BuildRequires

* Mon May 28 2018 Petr Viktorin <pviktori@redhat.com> - 3.4.2-3
- Use python3-sphinx to build the documentation
- Skip the `non_ascii_paste_text` test, which needs internet access

* Thu Mar 15 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.4.2-2
- Add Requires for required modules

* Wed Mar 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.2.3-3
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.2.3-2
- Remove platform-python subpackage
- Cleanup conditionals

* Sat Oct  7 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.3-1
- Update to 3.2.3.

* Sat Sep  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.2-1
- Update to 3.2.2.
- Move BRs to their respective subpackages.
- Enable the platform-python subpackage only on F27+.

* Thu Aug 24 2017 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-3
- Rebuilt for rhbz#1484607

* Fri Aug 11 2017 Petr Viktorin <pviktori@redhat.com> - 3.2.1-2
- Add subpackage for platform-python (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Wed Aug  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.1-1
- Update to 3.2.1.

* Wed Aug 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.2.0-1
- 3.2.0.

* Sun Jul 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.3-1
- Update to 3.1.3.
- Update BRs.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun  3 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.1-1
- Update to 3.1.1.
- Add BR on setuptools_scm.

* Wed Mar 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.7-1
- Update to 3.0.7.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.6-1
- Update to 3.0.6.
- Drop patch applied upstream.

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.5-2
- Rebuild for Python 3.6

* Tue Dec  6 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.5-1
- Update to 3.0.5.

* Mon Nov 28 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-1
- Update to 3.0.4.

* Fri Sep 30 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.
- Update requirements.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.2-1
- Update to 2.9.2.

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sat Apr  9 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.1-1
- Update to 2.9.1.
- Packaging updates.

* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-2
- Use new python macros
- Fix python3 package file ownership

* Sun Jan 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.7-1
- Update to 2.8.7.

* Fri Jan 22 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.6-1
- Update to 2.8.6.

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-1
- Update to 2.8.5

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-3
- Re-enable pexpect in tests

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.2-1
- Update to 2.8.2.

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 2.7.3-2
- Rebuilt for Python3.5 rebuild

* Thu Sep 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.3-1
- Update to 2.7.3.
- Provide additional symlinks to the pytest executables (rhbz#1249891).

* Mon Sep 14 2015 Orion Poplawski <orion@cora.nwra.com> - 2.7.2-2
- Provide python2-pytest, use python_provide macro

* Thu Jun 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.2-1
- Update to 2.7.2.
- Small fixes.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.1-1
- Update to 2.7.1.

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.0-1
- Update to 2.7.0.
- Apply updated Python packaging guidelines.
- Mark LICENSE with %%license.

* Tue Dec  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.4-1
- Update to 2.6.4.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.3-1
- Update to 2.6.3.

* Fri Aug  8 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.0-1
- Update to 2.6.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 2.5.2-2
- Redbuild for python 3.4

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-2
- Only run tests from the 'testing' subdir in %%check.

* Sat Oct  5 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-1
- Update to 2.4.2.
- Add buildroot's bindir to PATH while running the testsuite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-3
- Disable tests using pexpect for now, fails on F19.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-2
- Use python-sphinx for rhel > 6 (rhbz#973318).
- Update BR to use python-pexpect instead of pexpect.

* Sat May 25 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-1
- Update to 2.3.5.
- Docutils needed now to build README.html.
- Add some BR optionally used by the testsuite.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.4-1
- Update to 2.3.4.

* Sun Oct 28 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.2-1
- Update to 2.3.2.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Re-enable some tests, ignore others.
- Docs are available in English and Japanese now.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-4
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.
- Disable failing tests for Python3.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-1
- Update to 2.2.4.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.3-1
- Update to 2.2.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Tue Dec 13 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.

* Wed Oct 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.3-1
- Update to 2.1.3.

* Tue Sep 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-2
- Fix: python3 dependencies.

* Sun Aug 28 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-2
- Update Requires and BuildRequires tags.

* Tue Aug  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.

* Mon May 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Mar 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.2-1
- Update to 2.0.2.

* Sun Jan 16 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- New package.
