Name:      freexl
Version:   1.0.1
Release:   0%{?dist}
Summary:   Library to extract data from within an Excel spreadsheet 
Group:     System Environment/Libraries
License:   MPLv1.1 or GPLv2+ or LGPLv2+
URL:       http://www.gaia-gis.it/FreeXL
Source0:   http://www.gaia-gis.it/FreeXL/%{name}-%{version}.tar.gz 
BuildRequires: doxygen

%description
FreeXL is a library to extract valid data
from within an Excel spreadsheet (.xls)

Design goals:
    * simple and lightweight
    * stable, robust and efficient
    * easily and universally portable
    * completely ignore any GUI-related oddity

%package devel
Summary:  Development Libraries for FreeXL
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --enable-gcov=no --disable-static
make %{?_smp_mflags}

# Mailed the author on Dec 5th 2011
# Preserve date of header file
sed -i 's/^INSTALL_HEADER = \$(INSTALL_DATA)/& -p/' headers/Makefile.in

# Generate HTML documentation and clean unused installdox script
doxygen
rm -f html/installdox


%check
make check

# Clean up
pushd examples
  make clean
popd


%install
make install DESTDIR=%{buildroot}

# Delete undesired libtool archives
rm -f %{buildroot}%{_libdir}/lib%{name}.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%doc COPYING AUTHORS README
%{_libdir}/lib%{name}.so.*

%files devel
%doc examples html
%{_includedir}/freexl.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/freexl.pc


%changelog
* Mon Jul 13 2015 Jason Staph <jas322@arl.psu.edu> 1.0.1
- Update to latest upstream

* Tue Jun 19 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0d-1
- New upstream bugfix release

* Fri Jan 13 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-3
- Remove coverage tests and BR for lcov (fail in Rawhide)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan 08 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-1
- Correct versioning scheme to post-release
- Correct Source and setup macro accordingly

* Fri Nov 18 2011 Volker Fröhlich <volker27@gmx.at> 1.0.0-0.1.a
- Move development lib symlink to devel
- Don't build static lib
- Add README
- Build with enable-gcov
- BR lcov and doxygen
- Shorten description and summary
- Use macros in Source tag
- Add check section
- Change version and release
- Correct URL
- Correct to multiple licensing scenario
- Drop defattr
- Add pkgconfig and isa macro to devel's BR
- Use upstream tarball, as file size is different
- Remove EPEL 5 specific elements

* Wed Nov 26 2010 Peter Hopfgartber <peter.hopfgartner@r3-gis.com> 1.0.0a-0.1
- Initial packaging
