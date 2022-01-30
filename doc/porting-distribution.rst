Porting distribution for teaiso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create **teaiso/src/distro/xxxx** file **xxxx** is distro name. You can copy paste from **none** file.

This functions required: 

.. list-table:: **Function and meaning**
   :widths: 25 50
   :header-rows: 1

   * - Function
     - Meaning

   * - tool_init
     - Distribution creating tool installer. For example, Debian uses debootstrap and this function download and install debootstrap.

   * - create_rootfs
     - Execute distribution creator tool or download rootfs.

   * - populate_rootfs
     - Installing live packages or generating live initial ramdisks.
     
   * - install_packages
     - Reading **packages** variable from profile and installing.

   * - make_pkglist
     - Creating installed package list

   * - generate_isowork
     - Creating iso template. Scannig and writing grub.cfg file.

   * - customize_airootfs
     - Execute this function after package installation.

   * - clear_rootfs
     - Clearing packages, cache file and other garbage files.

Variables: **codename**, **rootfs**, **repository**, **packages** (array), **workdir**, **grub_cfg**, **arch**, **interactive**
