%undefine _ld_as_needed
%global _disable_lto 1
%global _disable_ld_no_undefined 1

%define	major		3
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d
%define oldlibname %mklibname %{name} %major

# BLAS lib
%global blaslib flexiblas

%bcond_without	blas
%bcond_without	boost
%bcond_with		cgns
%bcond_without	eigen
%bcond_without	fft
%bcond_without	gmp
%bcond_without	hdf5
%bcond_without	kwloc
%bcond_without	libjpeg
%bcond_without	mpfr
%bcond_with		mpi
%bcond_without	muparser
%bcond_without	netcdf
%bcond_without	opencl
%bcond_with		openmp
%bcond_with		ptscotch
%bcond_with		suitesparse
%bcond_without	yaml
%bcond_without	zlib
%bcond_without	zstd

Summary:	A suite of data structures and routines for solution of partial differential equations
Name:		petsc
Version:	3.23.0
Release:	1
License:	BSD
Group:		System/Libraries
Url:		https://petsc.org/
#Source0:	https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/%{name}-%{version}.tar.gz
Source0:	https://gitlab.com/petsc/petsc/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
# (fedora)
#Patch0:		petsc-3.15.0-fix_sundials_version.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(hwloc)
BuildRequires:	pkgconfig(%{blaslib})
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	pkgconfig(muparser)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(ompi)
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python3dist(mpi4py)
#BuildRequires:	libcgns-devel
#look for static lib only
BuildRequires:	gomp-devel
BuildRequires:	sundials-devel
BuildRequires:	suitesparse-devel

%description
PETSc, the Portable, Extensible Toolkit for Scientific Computation,
pronounced PET-see (/ˈpɛt-siː/), is a suite of data structures and
routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations. It supports MPI, and GPUs
through CUDA, HIP or OpenCL, as well as hybrid MPI-GPU parallelism; it
also supports the NEC-SX Tsubasa Vector Engine. PETSc (sometimes called
PETSc/TAO) also contains the TAO, the Toolkit for Advanced Optimization,
software library.

%files
%license LICENSE
%{_datadir}/petsc

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared objects for PETSc
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{oldlibname} <= %{EVRD}

%description -n %{libname}
%{description}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for the PETSc library
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and headers required to develop software with PETSc.

%files -n %{devname}
%{_includedir}/%{name}*.h
%{_includedir}/%{name}*.hpp
%{_includedir}/%{name}*.mod
%optional %{_includedir}/mpiuni.mod
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}

#--------------------------------------------------------------------

%if %{with python}
%package -n python-%{name}
Summary:	Python bindings for PETSc

BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(cython)
BuildRequires:	python3dist(numpy)
BuildRequires:	python3dist(setuptools)
BuildRequires:  hdf5-devel
Requires:	petsc
 
%description -n python-%{name}
This package provides Python3 bindings for PETSc, the Portable,
Extensible Toolkit for Scientific Computation.

%files -n python-%{name}
%{py_platsitedir}/mpich/%{name}/
%{py_platsitedir}/mpich/%{name}-%{pymodule_version}-py%{python_version}.*-info
%endif	
 
#--------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
#export PATH=%{_libdir}/openmpi/bin/:$PATH
export CC=gcc
export CXX=g++
#export FC=mpifort

#let's do this by hand, the configure script is home made
%before_configure
%configure \
	CC=$CC \
	CXX=$CXX \
	CFLAGS="%{optflags} -O3 -fPIC" \
	CXXFLAGS="%{optflags} -O3 -fPIC" \
	FFLAGS="$FFLAGS -O3 -fPIC" \
	FCFLAGS="$FCFLAGS -O3 -fPIC" \
	LDFLAGS="%{ldflags} -fPIC" \
	--CC_LINKER_FLAGS="$LDFLAGS" \\\
	--FC_LINKER_FLAGS="$LDFLAGS -lgfortran" \\\
	--prefix=%{_prefix} \
	--with-avx512-kernels=0 \
	--with-blaslapack=%{?with_blas:1}%{?!with_blas:0} \
	--with-boost=%{?with_boost:1}%{?!with_boost:0} \
	--with-cgns=%{?with_cgns:1}%{?!with_cgns:0} \
	--with-eigen=%{?with_eigen:1}%{?!with_eigen:0} \
	%{?with_eigen:--with-eigen-dir=%{_prefix}} \
	--with-fftw=%{?with_ffw:1}%{?!with_ffw:0} \
	--with-gmp=%{?with_gmp:1}%{?!with_gmp:0} \
	--with-hdf5=%{?with_hdf5:1}%{?!with_hdf5:0} \
	--with-hwloc=%{?with_hwloc:1}%{?!with_hwloc:0} \
	--with-libjpeg=%{?with_libjpeg:1}%{?!with_libjpeg:0} \
	--with-mpfr=%{?with_mpfr:1}%{?!with_mpfr:0} \
	--with-mpi=%{?with_mpi:1}%{?!with_mpi:0} \
	%{?with_mpi:--with-mpi-dir=%{_libdir}/openmpi} \
	--with-muparser=%{?with_muparser:1}%{?!with_muparser:0} \
	--with-netcdf=%{?with_netcdf:1}%{?!with_netcdf:0} \
	--with-opencl=%{?with_opencl:1}%{?!with_opencl:0} \
	--with-openmp=%{?with_openmp:1}%{?!with_openmp:0} \
	--with-ptscotch=%{?with_ptscotch:1}%{?!with_ptscotch:0} \
	--with-python=%{?with_python:1}%{?!with_python:0} \
	--with-python-exec=%{__python3} \
	%{?with_suitesparse:--with-suitesparse-lib=%{_libdir}} 	\
	%{?with_suitesparse:--with-suitesparse-include=%{_includedir}/suitesparse} \
	--with-suitesparse=%{?with_suitesparse:1}%{?!with_suitesparse:0} \
	--with-valgrind=0 \
	--with-yaml=%{?with_yaml:1}%{?!with_yaml:0} \
	--with-zlib=%{?with_zlib:1}%{?!with_zlib:0} \
	--with-zstd=%{?with_zstd:1}%{?!with_zstd:0} \
	%{nil}

%make_build

%install
%make_install

#the bloody /usr/lib is hardcoded everywhere
%if "%{?_lib}" == "lib64"
pushd %{buildroot}/%{_prefix}
mv -f lib %{_lib}
popd
%endif

#put fortran module files where they should
#mkdir -p %{buildroot}/%{fincludedir}
#mv -f %{buildroot}/%{_includedir}/*.mod %{buildroot}/%{fincludedir}/
sed -i 's|libdir=${prefix}/lib|libdir=${prefix}/%{_lib}|g' %{buildroot}/%{_libdir}/pkgconfig/PETSc.pc
