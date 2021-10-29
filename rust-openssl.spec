Summary:	OpenSSL bindings for the Rust programming language
Name:		rust-openssl
Version:	0.10.37
Release:	0.1
License:	Apache License, Version 2.0 and the MIT
Group:		Development/Tools
#Source0Download: https://github.com/sfackler/rust-openssl/releases
Source0:	https://github.com/sfackler/rust-openssl/archive/openssl-v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e03345b0419a75c2fa15584e3367c608
# cd %{name}-%{version}
# cargo vendor
# cd ..
# tar cJf %{name}-%{version}-vendor.tar.xz %{name}-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-%{version}-vendor.tar.xz
# Source1-md5:	9981857e6e6dc4fa1b579dcbde207101
URL:		https://github.com/sfackler/rust-openssl
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSSL bindings for the Rust programming language.

%prep
%setup -q -n %{name}-openssl-v%{version} -b1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export PKG_CONFIG_ALLOW_CROSS=1
export RUST_BACKTRACE=full

cargo -vv build --release --frozen \
%ifarch x32
	--target x86_64-unknown-linux-gnux32
%endif

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
