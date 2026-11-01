Name:           hashicorp-repo
Version:        1
Release:        0
Summary:        HashiCorp's official RPM repository for Zypper
License:        GPL-3.0-or-later
URL:            https://github.com/lyra-os-linux/hashicorp
Source0:        hashicorp.repo
Source1:        hashicorp.asc
BuildArch:      noarch
BuildRequires:  gpg2

%description
Registers HashiCorp's official RPM repository
(rpm.releases.hashicorp.com/RHEL/9/$basearch/stable) together with HashiCorp's package signing
key (D55C 0D1A C78A 8D81 26CB 631C FC9C A96A CA02 6560). The key is pinned
in this package because the repository does not publish repomd.xml.key; the
user still approves it the first time, in Vega or in Zypper. This package
carries no HashiCorp binary: it only makes `zypper install terraform vagrant` resolve
against HashiCorp's own repository.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/zypp/repos.d/hashicorp.repo
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/hashicorp-repo/hashicorp.asc

%check
repo=%{buildroot}%{_sysconfdir}/zypp/repos.d/hashicorp.repo
grep -qxF 'baseurl=https://rpm.releases.hashicorp.com/RHEL/9/$basearch/stable' "$repo"
grep -qxF 'gpgkey=file://%{_datadir}/hashicorp-repo/hashicorp.asc' "$repo"
grep -qxF 'gpgcheck=1' "$repo"
grep -qxF 'repo_gpgcheck=1' "$repo"
grep -qxF 'priority=90' "$repo"
# The shipped key must be exactly HashiCorp's package signing key.
export GNUPGHOME=$(mktemp -d)
fingerprints=$(gpg --batch --show-keys --with-colons %{buildroot}%{_datadir}/hashicorp-repo/hashicorp.asc | awk -F: '/^pub/{p=1;next} /^fpr/ && p {print $10; p=0}')
rm -rf "$GNUPGHOME"
test "$fingerprints" = "D55C0D1AC78A8D8126CB631CFC9CA96ACA026560"

%files
%dir %{_sysconfdir}/zypp
%dir %{_sysconfdir}/zypp/repos.d
%config(noreplace) %{_sysconfdir}/zypp/repos.d/hashicorp.repo
%dir %{_datadir}/hashicorp-repo
%{_datadir}/hashicorp-repo/hashicorp.asc

%changelog
