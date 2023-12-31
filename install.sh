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

# Add Czech locale and regenerate
CZECH_LOCALE="cs_CZ.UTF-8 UTF-8"
grep -qxF "$CZECH_LOCALE" /etc/locale.gen || echo -e "$CZECH_LOCALE" | sudo tee --append /etc/locale.gen
sudo locale-gen

# Install fish, change shell and set fish theme
sudo pacman -S fish --noconfirm
sudo chsh -s $(which fish) rstasta
yes | fish -c 'fish_config theme save "Nord"'
ln -sf $DOTFILES/fish/config.fish $CONFIG_PATH/fish/config.fish

# Install pacman packages
sudo pacman -S neovim kitty hyprland-git nvidia-dkms nvidia-settings qt5-wayland qt5ct libva libva-nvidia-driver-git linux-headers \
linux-zen-headers github-cli google-chrome pavucontrol rofi-lbonn-wayland waybar dunst ttf-font-awesome ttf-arimo-nerd noto-fonts \
ttf-iosevka network-manager-applet mc ntfs-3g steam brightnessctl docker docker-compose wireguard-tools visual-studio-code-bin grim slurp \
xdg-desktop-portal-hyprland xdg-desktop-portal-gtk kodi btrfs-assistant snapper cronie snap-pac grub-btrfs snap-pac-grub polkit-kde-agent \
protonup-qt parsec-bin subversion kdesvn zip unzip cups cups-pdf avahi nss-mdns yay gimp vlc libreoffice-fresh dolphin dolphin-plugins \
breeze godot hyprpaper spotify swaylock-effects wl-clipboard --noconfirm

### Hyprland and NVIDIA ###
# Set GRUB parameters
NVIDIA_GRUB="nvidia_drm.modeset=1"
grep -q "$NVIDIA_GRUB" /etc/default/grub || sudo sed -i "s/quiet/quiet $NVIDIA_GRUB/" /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg

# Set mkinitcpio
NVIDIA_MKINIT="nvidia nvidia_modeset nvidia_uvm nvidia_drm"
grep -q "$NVIDIA_MKINIT" /etc/mkinitcpio.conf || sudo sed -i "s/MODULES=(btrfs)/MODULES=(btrfs $NVIDIA_MKINIT)/" /etc/mkinitcpio.conf
sudo mkinitcpio --config /etc/mkinitcpio.conf --generate /boot/initframs-custom.img

# Set nvidia.conf
NVIDIA_CONF="options nvidia-drm modeset=1"
sudo touch /etc/modprobe.d/nvidia.conf
grep -qxF "$NVIDIA_CONF" /etc/modprobe.d/nvidia.conf || echo "$NVIDIA_CONF" | sudo tee --append /etc/modprobe.d/nvidia.conf

# Symling Hyprland config
rm -rf $CONFIG_PATH/hypr
ln -sf $DOTFILES/hypr $CONFIG_PATH/hypr
### Hyprland and NVIDIA ###

# Waybar
rm -rf $CONFIG_PATH/waybar
ln -sf $DOTFILES/waybar $CONFIG_PATH/waybar

# Rofi
rm -rf $CONFIG_PATH/rofi
ln -sf $DOTFILES/rofi $CONFIG_PATH/rofi

# hyprpaper
rm -rf $CONFIG_PATH/hyprpaper
ln -sf $DOTFILES/hyprpaper $CONFIG_PATH/hyprpaper

# Dunst
rm -rf $CONFIG_PATH/dunst
ln -sf $DOTFILES/dunst $CONFIG_PATH/dunst

# Kitty
rm -rf $CONFIG_PATH/kitty
ln -sf $DOTFILES/kitty $CONFIG_PATH/kitty

# Lutris and dependencies
sudo pacman -S --needed wine-staging giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls \
mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error \
lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo \
sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama \
ncurses lib32-ncurses ocl-icd lib32-ocl-icd libxslt lib32-libxslt libva lib32-libva gtk3 \
lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader lib32-vkd3d \
vkd3d python-protobuf vulkan-tools lutris --noconfirm

# Oh My Fish
curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install > install
chmod +x install
./install --noninteractive
rm install
fish -c "omf install bobthefish"

# Set user groups
sudo usermod -aG video,docker rstasta

# Enable services
sudo systemctl enable docker
sudo systemctl enable cronie
sudo systemctl enable grub-btrfsd
sudo systemctl enable cups
sudo systemctl enable avahi-daemon
