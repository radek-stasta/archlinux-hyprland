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
sudo pacman -S \
  neovim                      `# console text editor` \
  kitty                       `# terminal` \
  hyprland-git                `# desktop environment` \
  nvidia-dkms                 `# nvidia driver` \
  nvidia-settings             `# nvidia settings` \
  qt5-wayland                 `# needed for nvidia driver` \
  qt5ct                       `# needed for nvidia driver` \
  libva                       `# needed for nvidia driver` \
  libva-nvidia-driver-git     `# needed for nvidia driver` \
  linux-headers               `# kernel headers` \
  linux-zen-headers           `# zen kernel headers` \
  github-cli                  `# console app to connect to Github` \
  google-chrome               `# Google Chrome browser` \
  pavucontrol                 `# Pulse Audio control` \
  rofi-lbonn-wayland          `# application launcher` \
  dunst                       `# notification daemon` \
  ttf-font-awesome            `# font for icons` \
  ttf-arimo-nerd              `# font for icons` \
  noto-fonts                  `# noto family font` \
  ttf-iosevka                 `# Iosevka font` \
  network-manager-applet      `# status bar applet for network manager` \
  mc                          `# Midnight commander` \
  ntfs-3g                     `# library for connecting to ntfs partition` \
  steam                       `# Steam ` \
  brightnessctl               `# library for controlling display brightness` \
  docker                      `# Docker` \
  docker-compose              `# Docker compose plugin` \
  wireguard-tools             `# wireguard` \
  grim                        `# screenshot utility` \
  slurp                       `# library for selecting region for screenshots` \
  xdg-desktop-portal-hyprland `# library for windows to communicate with each other` \
  xdg-desktop-portal-gtk      `# library for windows to communicate with each other` \
  kodi                        `# Kodi` \
  btrfs-assistant             `# application to manage btrfs partitions` \
  snapper                     `# library for btrfs snapshots` \
  cronie                      `# library for automatic tasks` \
  snap-pac                    `# pacman hooks for btrfs snapshots` \
  grub-btrfs                  `# library for btrfs snapshots in grub` \
  snap-pac-grub               `# library for btrfs snapshots in grub` \
  polkit-kde-agent            `# library for password propagation to other apps` \
  protonup-qt                 `# application to manage proton versions` \
  parsec-bin                  `# Parsec` \
  subversion                  `# Subversion` \
  kdesvn                      `# graphical svn client` \
  zip                         `# library for zipin files` \
  unzip                       `# library for unziping files` \
  cups                        `# library for printing` \
  cups-pdf                    `# library for printing to pdf` \
  avahi                       `# library needed for printing` \
  nss-mdns                    `# library needed for printing` \
  yay                         `# AUR helper` \
  gimp                        `# Gimp` \
  vlc                         `# VLC media player` \
  libreoffice-fresh           `# Libre Office` \
  nautilus                    `# nautilus file manager` \
  nordzy-icon-theme-git       `# icon theme` \
  godot                       `# Godot game engine` \
  hyprpaper                   `# library for desktop wallpaper` \
  spotify                     `# Spotify` \
  swaylock-effects            `# library for lock screen` \
  wl-clipboard                `# library for clipboard from different screens` \
  pipewire                    `# multimedia framework needed for eww widgets` \
  wireplumber                 `# library needed for pipewire and eww widgets` \
  xwaylandvideobridge         `# library needed for streaming windows` \
  remmina                     `# remote desktop client` \
  freerdp                     `# library for rdp access in remmina` \
  htop                        `# system monitor` \
  eww                         `# Elkowars wacky widgets` \
  python                      `# python` \
  python-pipx                 `# python package manager` \
  jq                          `# json parser for bash` \
  playerctl                   `# library for media control in console` \
  jre-openjdk                 `# Java JRE` \
  webstorm                    `# Webstorm IDE` \
  nodejs-lts-hydrogen         `# Node.js` \
  npm                         `# npm for Node.js` \
  firefox                     `# Firefox browser` \
  nginx                       `# nginx server` \
--noconfirm

# Install yay packages
yay -S nordzy-cursors --noconfirm

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

# eww
rm -rf $CONFIG_PATH/eww
ln -sf $DOTFILES/eww $CONFIG_PATH/eww

# Cursor
rm -rf $HOME/.icons
ln -sf $DOTFILES/icons $HOME/.icons

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

# Install python modules
python -m venv $HOME/.venv
$HOME/.venv/bin/python -m pip install --upgrade pip
$HOME/.venv/bin/python -m pip install bs4
$HOME/.venv/bin/python -m pip install selenium

# Set user groups
sudo usermod -aG video,docker rstasta

# Set Gnome specific properties
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
gsettings set org.gnome.desktop.interface cursor-theme Nordzy-cursors
gsettings set org.gnome.desktop.interface icon-theme Nordzy

# Enable services
sudo systemctl enable docker
sudo systemctl enable cronie
sudo systemctl enable grub-btrfsd
sudo systemctl enable cups
sudo systemctl enable avahi-daemon
