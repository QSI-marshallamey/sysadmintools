sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo ubuntu-drivers autoinstall
# sudo ubuntu-drivers-common
sudo apt install nvidia-cuda-toolkit gcc-6

nvcc --version