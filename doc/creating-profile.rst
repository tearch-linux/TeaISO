Teaiso profile creation
^^^^^^^^^^^^^^^^^^^^^^^
You can prefer template or from scratch. 

1. If you want to create profile from template, Must run this command:

.. code-block:: shell

	mkteaiso -c xxxx
	# xxx is profile template name

Available Templates: **debian**, **archlinux**, **sulin**, **tearch**, **ubuntu**, **none**

**Note:** None is dummy profile template, mostly used by debugging.

2. If you want to create profile from scratch, profile directory structure:

.. code-block:: shell

	├── airootfs
	│   └── ...
	├── grub.cfg
	├── packages
	│    └── ...
	└── profile.yaml

* airootfs directory store files that will merge with rootfs.
* packages directory store package files that will install into rootfs.
* grub.cfg file is header of grub config. Teaiso scan kernel and automatically merge with this config.
* profile.yaml file is main configuration file. You can configure distribution settings with this file.

profile.yaml
============
This file is distribution configuration file. Example file here:

.. code-block:: yaml

	name: custom-debian
	distro: debian
	codename: testing
	publisher: Debian GNU/Linux <https://debian.org>
	label: DEBIAN_TEAISO
	codename: testing
	application_id: Debian Linux Live/Rescue Media
	airootfs_directory: airootfs
	iso_merge: iso_merge
	arch: x86_64
	grub_cfg: grub.cfg
	linux_args: quiet splash
	keyring_package: debian-archive-keyring
	packages:
	 - packages.x86_64
	file_permissions:
	 - /etc/shadow|0:0:400
	customize_isowork_pre:
	 - customize-isowork-pre.sh
	customize_isowork:
	 - customize-isowork.sh
	customize_airootfs:
	 - customize-airootfs.sh
	 customize_airootfs_pre:
	 - customize-airootfs-pre.sh

* **customize_airootfs_pre** execute in chroot before installing packages.
* **customize_airootfs** execute in chroot after installing packages.
* **customize_isowork_pre** execute in workdir before creating squashfs
* **customize_isowork** execute in workdir before creating iso file

If **distro** is archlinux or tearch, You can define **pacman** variable. This variable copy your pacman.conf file into chroot before creating rootfs.

If **distro** is debian, You can define **variant** variable. This variable set debootstrap variant.
