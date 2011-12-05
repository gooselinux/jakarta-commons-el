# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name       el
%define short_name      commons-el

%define section         free

%global with_maven      0

Name:           jakarta-commons-el
Version:        1.0
Release:        18.4%{?dist}
Epoch:          0
Summary:        The Jakarta Commons Extension Language
License:        ASL 1.1
Group:          Development/Libraries
URL:            http://jakarta.apache.org/commons/el/
Source0:        http://archive.apache.org/dist/jakarta/commons/el/source/commons-el-%{version}-src.tar.gz
Source1:        http://repo1.maven.org/maven2/commons-el/commons-el/1.0/commons-el-1.0.pom
Patch0:         %{short_name}-%{version}-license.patch
Patch1:         %{short_name}-eclipse-manifest.patch
Patch2:         jakarta-commons-el-enum.patch
BuildArch:      noarch
Requires(post): jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  apache-tomcat-apis
BuildRequires:  junit

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1 -b .license
pushd src/conf
%patch1 -p1
popd
%patch2 -p1

# remove all precompiled stuff
find . -type f -name "*.jar" -exec rm -f {} \;

cat > build.properties <<EOBP
build.compiler=modern
junit.jar=$(build-classpath junit)
servlet-api.jar=$(build-classpath apache-tomcat-apis/tomcat-servlet2.5-api)
jsp-api.jar=$(build-classpath apache-tomcat-apis/tomcat-jsp2.1-api)
servletapi.build.notrequired=true
jspapi.build.notrequired=true
EOBP

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  jar javadoc


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{with_maven}
# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap commons-el commons-el %{version} JPP %{name}
%endif

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt STATUS.html
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}-%{version}.jar
%{_javadir}/%{short_name}.jar
%if %{with_maven}
%{_datadir}/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


%changelog
* Tue Feb 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-18.4
- Drop gcj_support.
- BR apache-tomcat-apis instead of tomcat5-*.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.0-18.2
- Add %%{with_maven} macro
- Fix mixed spaces and tabs
- Fix Group tags

* Thu Sep 09 2009 Fernando Nasser <fnasser@redhat.com> - 0:1.0-18.1
- Merge with upstream for:
  Add pom and depmap fragment
  Removal of ghost symlink
  Some spec file cleanups
- Build without AOT compilation

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-11.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-18
- fix scriptlets

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-17
- fix pom install

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-16
- add pom

* Mon Apr 27 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.0-10.5
- Fix FTBFS: added BR: tomcat5-jsp-2.0-api (resolves BZ#497179).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 David Walluck <dwalluck@redhat.com> 0:1.0-15
- fix component-info.xml

* Wed Jan 21 2009 David Walluck <dwalluck@redhat.com> 0:1.0-14
- fix jar name in repolib

* Tue Jan 20 2009 David Walluck <dwalluck@redhat.com> 0:1.0-13
- fix repolib location

* Tue Jan 20 2009 David Walluck <dwalluck@redhat.com> 0:1.0-12
- add repolib

* Wed Aug 13 2008 David Walluck <dwalluck@redhat.com> 0:1.0-11
- update header

* Wed Aug 13 2008 David Walluck <dwalluck@redhat.com> 0:1.0-10
- build for JPackage 5

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 0:1.0-9.4
- Update OSGi metadata for Eclipse 3.4.

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-9.3
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0-9jpp.2
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0-8jpp.2
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Ben Konrath <bkonrath@redhat.com> - 0:1.0-8jpp.1
- Add eclipse-manifest patch.
  From Fernando Nasser <fnasser@redhat.com>:
- Specify source 1.4 due to use of enum as identifier

* Fri Feb 09 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp.1
- Remove duplicate name tag
- Rebuild

* Thu Aug 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp.1
- Merge with upstream

* Thu Aug 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp
- Fix AOT support

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.0-5jpp_4fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0-5jpp_3fc
- rebuild

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_2fc
- Build with gcj_support enabled
- Add missing BR for jsp (API)

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-6jpp
- Add AOT support

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_1fc
- First build for FC6

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_0fc
- Add gcj_support

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp
- First JPP 1.7 build

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.0-4jpp_6fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_5fc
- bump again for double-long bug on ppc(64)

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_4fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_3fc
- rebuilt

* Tue Jul 19 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Thu Jun 14 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp_1fc
- Upgrade to 1.0-4jpp.

* Thu May 26 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp
- Don't bundle servletapi sources (which weren't used anyway).

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-3jpp_1fc
- Upgrade to 1.0-3jpp.
- Rearrange how BC-compiled stuff is built and installed.
- Don't bundle servletapi sources (which weren't used anyway).

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_3fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_2fc
- BC-compile.

* Thu Jan 20 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_1fc
- Build into Fedora.

* Thu Oct 21 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp_2rh
- Rebuild (no changes)

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0-3jpp
- Rebuild with ant-1.6.2

* Wed Jul 14 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp_1rh
- Merge with upstream version that removes dependency on ant-optional

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0-2jpp
- Upgrade to Ant 1.6.X

* Fri Jan  9 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-1jpp
- First build for JPackage

* Wed Dec 17 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-0.2
- With Javadocs

* Wed Dec 17 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-0.1
- First build
