# tinyben

tinyben is an attempt to create a bencharking suite, similar to [phoronix-test-suite](https://www.phoronix-test-suite.com/), but simpler and easier to use. tinyBen is designed to ben <1000 lines of code [1](https://github.com/geohot/minikeyvalue).

We are always supporting (at least) the latest Ubuntu LTS version.

## usage

```bash
python3 -m venv venv
pip3 install -r requirements.txt
python3 run.py 
```
If you need to run with root permission (`apt-get` is part of a benchmark) run instead `sudo venv/bin/python3 runner.py`

https://github.com/rcastellotti/tinyben/blob/40ee71051109a1fbc0cdbcb628b51074fffd5964/run.py#L1-L23
## benchmarks i need now (will be removed)

+ __cpu__ ~> compilation (llvm,linux, imagemagick, godot), lz4
+ __memory__ ~> tinymembench, mbw
+ __I/O__ ~> redis, sqlite


## sample run output
```
  Benchmark Name                                      │ Benchmark Status │ Benchmark Result                              
 ═════════════════════════════════════════════════════╪══════════════════╪══════════════════════════════════════════════ 
  linux compilation (defconfig)                       │        ✅        │ 320.49024271965027 s                          
  ImageMagick compilation (gcc)                       │        ✅        │ 71.90199041366577 s                           
  Godot Game Enging compilation                       │        ✅        │ 399.275563955307 s                            
  llvm-project compilation (ninja)                    │        ✅        │ 742.0720775127411 s                           
  sqlite 2500 insertions                              │        ✅        │ 2.628910541534424 s                           
  lz4 compress ubuntu-22.04.2-desktop-amd64.iso       │        ✅        │ 7.096761703491211 s                          
  lz4 decompress ubuntu-22.04.2-desktop-amd64.iso.lz4 │        ✅        │ 4.68076229095459 s   
  ssvb/tinymembench                                   │        ✅        │ results/tinymembench-2023-06-03-18:40:16.txt  
  redis-benchmark                                     │        ✅        │ results/redis-2023-06-03-18:47:28.csv       
  raas/mbw 1024 MiB                                   │        ✅        │ results/mbw-2023-06-03-18:48:12.txt 
  ```

## instructions to launch an Ubuntu 22.04 qemu vm
```bash
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
sudo qemu-img convert jammy-server-cloudimg-amd64.img jammy.img
sudo qemu-img resize jammy.img +20G
sudo cloud-localds cloud-config-tinyben.iso cloud-config-tinyben.yml
```

`cloud-config-tinyben.yml`
```
password: tb
hostname: tinyben
chpasswd: { expire: False }
ssh_pwauth: True
final_message: "Cloud init is done!"
```

```bash
stty intr ^] &&
sudo qemu-system-x86_64 \
 -enable-kvm \
 -smp 32 \
 -m 32G \
 -drive file=jammy.img,if=none,id=disk0,format=raw \
 -drive file=cloud-config-tinyben.iso,media=cdrom,index=0 \
 -device virtio-scsi-pci,id=scsi0,disable-legacy=on,iommu_platform=true \
 -device scsi-hd,drive=disk0 \
 -nographic \
 -net user,hostfwd=tcp::10022-:22 \
 -net nic 

```
