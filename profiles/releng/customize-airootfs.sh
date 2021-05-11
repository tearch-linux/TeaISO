#!/usr/bin/env bash
set -e -u

sed -i 's/#\(en_US\.UTF-8\)/\1/' /etc/locale.gen
locale-gen

sed -i "s/#Server/Server/g" /etc/pacman.d/mirrorlist

# Init Pacman Keys
pacman-key --init
pacman-key --populate archlinux tearch
pacman-key --lsign-key 0AA4D45CBAA86F73