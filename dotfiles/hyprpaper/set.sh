hyprpaper & disown & sleep 1
wallpaper_dir="$HOME/.config/hyprpaper/wallpapers"
files=($wallpaper_dir/*)
random_file=("${files[RANDOM % ${#files[@]}]}")
hyprctl hyprpaper wallpaper "eDP-1,$random_file"
hyprctl hyprpaper wallpaper "HDMI-A-1,$random_file"
hyprctl hyprpaper wallpaper "DP-1,$random_file"