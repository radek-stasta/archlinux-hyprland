# Variables
CONFIG_PATH="$HOME/.config"
DOTFILES="$PWD/dotfiles"

# Enable chaotic aur
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 3056513887B78AEB
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' --noconfirm
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' --noconfirm
CHAOTIC_MIRROR="[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist"
grep -qxF "[chaotic-aur]" /etc/pacman.conf || echo -e "$CHAOTIC_MIRROR" | sudo tee --append /etc/pacman.conf

# System update
sudo pacman -Syyu --noconfirm

### Hyprland ###
# Install Hyprland
sudo pacman -S hyprland-git nvidia-dkms qt5-wayland qt5ct libva libva-nvidia-driver-git --noconfirm

# Set GRUB parameters
NVIDIA_GRUB="nvidia_drm.modeset=1"
grep -q "$NVIDIA_GRUB" /etc/default/grub || sudo sed -i "s/quiet/quiet $NVIDIA_GRUB/" /etc/default/grub
# sudo grub-mkconfig -o /boot/grub/grub.cfg

# Symling Hyprland config
rm -rf $CONFIG_PATH/hypr
ln -sf $DOTFILES/hypr $CONFIG_PATH/hypr

# Install pacman packages
sudo pacman -S kitty --noconfirm
