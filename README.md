# HashiCorp repository registration

RPM packaging for `hashicorp-repo`, a Lyra-authored package that registers
HashiCorp's official RPM repository
(`rpm.releases.hashicorp.com/RHEL/9/$basearch/stable`) so `zypper install terraform vagrant` resolves against
it.

HashiCorp publishes RPM repositories for RHEL, Fedora and Amazon Linux, not for
openSUSE. This package uses the RHEL 9 channel (`RHEL/9/$basearch/stable`):
Terraform is a static binary and Vagrant bundles its own runtime, built for
glibc 2.34, which Leap 16.1 (glibc 2.40) satisfies.

Like [`vscode`](https://github.com/lyra-os-linux/vscode), this package
carries no upstream binary and no `_service`. The difference is the key:
HashiCorp's repository is signed (`repomd.xml.asc`) but does not publish
`repomd.xml.key`, and no distribution package ships HashiCorp's key. So
`hashicorp-repo` ships it at `/usr/share/hashicorp-repo/hashicorp.asc` and points
`gpgkey=` at that file. The user still approves the key the first time, in
Vega (Software → Desenvolvedores → Terraform ou Vagrant) or when Zypper asks.

- `hashicorp.repo`: the Zypper repository definition, with metadata and
  package GPG verification both enabled and third-party priority `90`;
- `hashicorp.asc`: HashiCorp's package signing key,
  `D55C 0D1A C78A 8D81 26CB 631C FC9C A96A CA02 6560`, from
  `https://rpm.releases.hashicorp.com/gpg`;
- `hashicorp-repo.spec`: installs both files, and at build time asserts the
  repository settings and the key fingerprint;
- `hashicorp-repo.changes`: RPM changelog.

## Atualizar a chave

Se a HashiCorp trocar a chave, baixe a nova de
`https://rpm.releases.hashicorp.com/gpg`, confira que ela verifica
`repodata/repomd.xml.asc` do repositório e atualize a impressão digital no
`.spec`, nos testes e neste README.

## Validação

Em cada push para `main` e pull request, o CI executa:

```sh
python3 -m unittest discover -s tests -v
rpmspec -P hashicorp-repo.spec >/dev/null
```

Os testes verificam a URL HTTPS oficial, a chave esperada (pela impressão
digital), `gpgcheck`, `repo_gpgcheck`, prioridade e instalação/remoção
idempotentes do arquivo.

## Credits

Terraform and Vagrant are developed by [HashiCorp](https://www.hashicorp.com/). This package is not
affiliated with or endorsed by HashiCorp; it only points Zypper at their
existing, official repository.
