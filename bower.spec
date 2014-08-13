# TODO
# - use system node deps
#
# Conditional build:
%bcond_with	npm		# build with npm installing vendors on package install
%bcond_without	bundled		# build npm vendors bundled

Summary:	A package manager for the web
Name:		bower
Version:	1.3.9
Release:	0.7
License:	MIT
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/bower/-/%{name}-%{version}.tgz
# Source0-md5:	b5e2e8f895144d22ec26a76fd6065ab5
URL:		http://bower.io/
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
%if %{with bundled}
BuildRequires:	npm
%endif
%if %{with npm}
Requires:	npm
%endif
Requires:	nodejs >= 0.10.0
%if %{without npm} && %{without bundled}
Requires:	nodejs-abbrev >= 1.0.4
Requires:	nodejs-archy >= 0.0.2
Requires:	nodejs-bower-config >= 0.5.2
Requires:	nodejs-bower-endpoint-parser >= 0.2.2
Requires:	nodejs-bower-json >= 0.4.0
Requires:	nodejs-bower-logger >= 0.2.2
Requires:	nodejs-bower-registry-client >= 0.2.0
Requires:	nodejs-cardinal >= 0.4.0
Requires:	nodejs-chalk >= 0.5.0
Requires:	nodejs-chmodr >= 0.1.0
Requires:	nodejs-decompress-zip >= 0.0.6
Requires:	nodejs-fstream >= 0.1.22
Requires:	nodejs-fstream-ignore >= 0.0.6
Requires:	nodejs-glob >= 4.0.2
Requires:	nodejs-graceful-fs >= 3.0.1
Requires:	nodejs-handlebars >= 1.3.0
Requires:	nodejs-inquirer >= 0.5.1
Requires:	nodejs-insight >= 0.4.1
Requires:	nodejs-is-root >= 0.1.0
Requires:	nodejs-junk >= 0.3.0
Requires:	nodejs-lockfile >= 0.4.2
Requires:	nodejs-lru-cache >= 2.5.0
Requires:	nodejs-mkdirp >= 0.5.0
Requires:	nodejs-mout >= 0.9.1
Requires:	nodejs-nopt >= 3.0.0
Requires:	nodejs-opn >= 0.1.1
Requires:	nodejs-osenv >= 0.1.0
Requires:	nodejs-p-throttler >= 0.0.1
Requires:	nodejs-promptly >= 0.2.0
Requires:	nodejs-q >= 1.0.1
Requires:	nodejs-request >= 2.36.0
Requires:	nodejs-request-progress >= 0.3.0
Requires:	nodejs-retry >= 0.6.0
Requires:	nodejs-rimraf >= 2.2.0
Requires:	nodejs-semver >= 2.3.0
Requires:	nodejs-shell-quote >= 1.4.1
Requires:	nodejs-stringify-object >= 0.2.0
Requires:	nodejs-tar >= 0.1.17
Requires:	nodejs-tmp >= 0.0.23
Requires:	nodejs-update-notifier >= 0.2.0
Requires:	nodejs-which >= 1.0.5
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bower works by fetching and installing packages from all over, taking
care of hunting, finding, downloading, and saving the stuff you're
looking for. Bower keeps track of these packages in a manifest file,
bower.json. How you use packages is up to you. Bower provides hooks to
facilitate using packages in your tools and workflows.

Bower is optimized for the front-end. Bower uses a flat dependency
tree, requiring only one version for each package, reducing page load
to a minimum.

%prep
%setup -qc
mv package/* .

%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' bin/*
chmod a+rx bin/*

%if %{with bundled}
%build
npm install .
chmod -R a+rX node_modules
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/%{name}}
cp -pr lib bin templates package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{name}
ln -s %{nodejs_libdir}/%{name}/bin/%{name} $RPM_BUILD_ROOT%{_bindir}

%if %{with bundled}
cp -a node_modules $RPM_BUILD_ROOT%{nodejs_libdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with npm}
# hack to setup node modules until system deps are available
%post
test -d %{nodejs_libdir}/%{name}/node_modules && exit 0
cd %{nodejs_libdir}/%{name}
npm install

%postun
if [ "$1" = 0 ]; then
	rm -r %{nodejs_libdir}/%{name}/node_modules
fi
%endif

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md CONTRIBUTING.md HOOKS.md LICENSE
%attr(755,root,root) %{_bindir}/bower
%dir %{nodejs_libdir}/%{name}
%{nodejs_libdir}/%{name}/package.json
%{nodejs_libdir}/%{name}/templates
%{nodejs_libdir}/%{name}/lib
%dir %{nodejs_libdir}/%{name}/bin
%attr(755,root,root) %{nodejs_libdir}/%{name}/bin/*

%if %{with bundled}
%defattr(-,root,root,-)
%{nodejs_libdir}/%{name}/node_modules
%endif
