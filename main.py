'''
reference:
qemu-system-x86_64 \\
    -enable-kvm \\
    -m 2G \\
    -machine q35,accel=kvm \\
    -smp 4,cores=2 \\
    -cpu Penryn,vendor=GenuineIntel,kvm=on,+sse3,+sse4.2,+aes,+xsave,+avx,+xsaveopt,+xsavec,+xgetbv1,+avx2,+bmi2,+smep,+bmi1,+fma,+movbe,+invtsc \\
    -device isa-applesmc,osk="$OSK" \\
    -smbios type=2 \\
    -drive if=pflash,format=raw,readonly,file="$OVMF/OVMF_CODE.fd" \\
    -drive if=pflash,format=raw,file="$OVMF/OVMF_VARS-1024x768.fd" \\
    -vga qxl \\
    -device ich9-intel-hda -device hda-output \\
    -usb -device usb-kbd -device usb-mouse \\
    -netdev user,id=net0 \\
    -device e1000-82545em,netdev=net0,id=net0,mac=52:54:00:c9:18:27 \\
    -device ich9-ahci,id=sata \\
    -drive id=ESP,if=none,format=qcow2,file=ESP.qcow2 \\
    -device ide-hd,bus=sata.2,drive=ESP \\
    -drive id=InstallMedia,format=raw,if=none,file=BaseSystem.img \\
    -device ide-hd,bus=sata.3,drive=InstallMedia \\
'''
import time
print('Loading colorama...')
start = time.time()
try:
    from colorama import *
except ImportError:
    print('[FATAL] Failed to load colorama due to an import error! Quit.')
    exit(1)
except Exception as e:
    print(f'[FATAL] Failed to load colorama! {e} Quit.')
    exit(1)
end = time.time()
print(Fore.GREEN  + f'colorama loaded in {end - start} seconds')
print(Fore.GREEN + 'Spinup Version 1.1' + Fore.RESET)
print(Fore.GREEN + 'Loading json...' + Fore.RESET)
totalstart = time.time()
start = time.time()
try:
    import json
except ImportError:
    print(Fore.RED + '[FATAL] Failed to load json due to an import error! Quit.' + Fore.RESET)
    exit(1)
except Exception as e:
    print(Fore.RED + f'[FATAL] Failed to load json! {e} Quit.' + Fore.RESET)
    exit(1)
end = time.time()
print(Fore.GREEN  + f'json loaded in {end - start} seconds' + Fore.RESET)
print(Fore.GREEN + 'Loading click...' + Fore.RESET)
start = time.time()
try:
    import click
except ImportError:
    print(Fore.RED + '[FATAL] Failed to load click due to an import error! Quit.' + Fore.RESET)
    exit(1)
except Exception as e:
    print(Fore.RED + f'[FATAL] Failed to load click! {e} Quit.' + Fore.RESET)
    exit(1)
end = time.time()
print(Fore.GREEN  + f'click loaded in {end - start} seconds' + Fore.RESET)
print(Fore.GREEN + 'Loading OS-related modules...' + Fore.RESET)
start = time.time()
try:
    import os.path
    import os
except ImportError:
    print(Fore.RED + '[FATAL] Failed to load OS-related modules due to an import error! Quit.' + Fore.RESET)
    exit(1)
except Exception as e:
    print(Fore.RED + f'[FATAL] Failed to load OS-related modules! {e} Quit.' + Fore.RESET)
    exit(1)
end = time.time()
print(Fore.GREEN  + f'OS-related modules loaded in {end - start} seconds' + Fore.RESET)
print(Fore.GREEN + 'Loading requests module...' + Fore.RESET)
start = time.time()
try:
    import requests
except ImportError:
    print(Fore.RED + '[FATAL] Failed to load requests due to an import error! Quit.' + Fore.RESET)
    exit(1)
except Exception as e:
    print(Fore.RED + f'[FATAL] Failed to load requests! {e} Quit.' + Fore.RESET)
    exit(1)   
end = time.time()
print(Fore.GREEN + f'requests loaded in {end - start} seconds' + Fore.RESET)
start = time.time()
try:
    import subprocess
except ImportError:
    print(Fore.RED + '[FATAL] Failed to load subprocess due to an import error! Quit.' + Fore.RESET)
    exit(1)
except Exception as e:
    print(Fore.RED + f'[FATAL] Failed to load subprocess! {e} Quit.' + Fore.RESET)
    exit(1)   
end = time.time()
print(Fore.GREEN + f'subprocess loaded in {end - start} seconds' + Fore.RESET)
print(Fore.GREEN + f'All modules loaded in {end - totalstart} seconds!' + Fore.RESET)
try:
    uname = os.uname()
except:
    uname = 'Windows'
if uname != 'Windows':
    LIBSPINUP_BASE = '~/.libspinup'
else:
    print(Fore.YELLOW + '[WARNING] Spinup Scripts are designed only for use on Linux hosts' + Fore.RESET)
    LIBSPINUP_BASE = os.path.join(os.environ['APPDATA'], 'LibSpinup')
LIBSPINUP_SCRIPT_LOCATION = os.path.join(LIBSPINUP_BASE, 'scripts')
LIBSPINUP_DISK_LOCATION = os.path.join(LIBSPINUP_BASE,'disks')
if not os.path.exists(LIBSPINUP_BASE):
    os.mkdir(LIBSPINUP_BASE)
    os.mkdir(LIBSPINUP_SCRIPT_LOCATION)
if not os.path.exists(LIBSPINUP_SCRIPT_LOCATION):
    os.mkdir(LIBSPINUP_SCRIPT_LOCATION)
@click.group()
def cli():
    pass
@cli.command()
@click.argument('file')
@click.argument('vm')
def create_drives(file, vm):
    '''FILE: Spinup File,
    VM: VM Name
    '''
    if not vm.startswith('spinup://'):
        print(Fore.RED + '[FATAL] This command is only for use with LibSpinup VMs')
        print(Fore.GREEN + '[INFO] For more information, see the documentation.')
        exit(1)
    try:
        vmfile = json.load(open(file))
    except Exception as e:
        print(Fore.RED + f'[FATAL] Can\'t load Spinup File. {e}\nQuit.' + Fore.RESET)
        exit(1)
    try:
        vmfile["disks"] = vmfile["drives"]
    except:
        pass
    for i in vmfile["disks"]:
        file = i["file"]
        format_ = i["format"]
        size = i.get('size','16G')
        print(Fore.GREEN + f'Run: qemu-img -f {format_} {file} {size}' + Fore.RESET)
        if uname != 'Windows':
            subprocess.Popen(['qemu-img','create',f'-f {format_}',file,size])
        else:
            print(Fore.YELLOW + 'qemu-img not supported on Windows, not running.' + Fore.RESET)

@cli.command()
@click.argument('file')
@click.option('--script-location', default='boot.sh', help="Where to store generated file")
def generate(file,script_location=''):
    """FILE: File to generate from"""
    using_libspinup = False
    firm_path = 'firmware'
    if script_location.startswith('spinup://'):
        vm_name = script_location.replace('spinup://','')
        vm_loc = script_location.replace('spinup://',LIBSPINUP_SCRIPT_LOCATION + '/')
        firm_path = script_location.replace('spinup://',LIBSPINUP_DISK_LOCATION + '/firmware')
        script_location = vm_loc + '.sh'
        using_libspinup = True
    try:
        vmfile = json.load(open(file))
    except Exception as e:
        print(Fore.RED + f'[FATAL] Can\'t load Spinup File. {e}\nQuit.' + Fore.RESET)
        exit(1)
    script = open(script_location, 'w')
    keys = list(vmfile.keys())
    sataport = 0
    pcieport = 0
    VGA_MODE = 'qxl'
    script.write('#!/bin/bash\n')
    script.write('qemu-sytem-x86-64 \\\n\t-machine ')
    if 'machine' in keys:
        mach_keys = list(vmfile['machine'].keys())
        mach = vmfile['machine']
        if 'type' in mach_keys:
            script.write(mach_['type'])
        else:
            script.write('q35')
        if 'prop' in mach_keys:
            script.write(f',prop={mach["prop"]}')
        if 'enable_kernel_irq_chip' in mach_keys:
            if mach[kernel_irq_chip]:
                v = 'on'
            else:
                v = 'off'
            script.write(f',kernel_irq_chip={v}')
        else:
            script.write(f',kernel_irq_chip=on')
        if 'accelerator' in mach_keys:
            script.write(f',accel={mach["accelerator"]}')
    else:
        print(Fore.YELLOW + '[WARNING] Machine options were not specified, falling back to default.')
        print(Fore.BLUE + 'If you get an error upon boot, use machine options to change the accelerator to not KVM' + Fore.RESET)
        script.write('q35,kernel_irq_chip=on,accel=kvm')
    script.write(' \\\n')
    if 'cpu' in keys:
        cpu_keys = list(vmfile['cpu'].keys())
        cpu = vmfile['cpu']
        if 'model' in cpu_keys:
            script.write(f'\t-cpu {cpu["model"]}')
        else:
            script.write('\t-cpu Skylake-Client')
        if 'vendor' in cpu_keys:
            script.write(f',vendor={cpu["vendor"]}')
        if 'kvm' in cpu_keys:
            if cpu[kvm]:
                print(Fore.YELLOW + '[WARNING] KVM being set to on is not needed for KVM acceleration\nAdditionally, it **will** prevent you from using NVIDIA cards under this VM')
                script.write(f',kvm=on')
            else:
                script.write(f',kvm=off')
        else:
            script.write(',kvm=off')
        if 'supported_instructions' in cpu_keys:
            supported_instructions = cpu['supported_instructions']
        else:
            supported_instructions = ['sse2','sse3','sse4.2','aes','xsave','avx','xsaveopt','xgetbv1','avx2','bmi2','smep','bmi1','fma','movbe','invtsc']
        for i in supported_instructions:
            script.write(f',+{i}')
        script.write(' \\\n\t-smp ')
        if 'cores' in cpu_keys:
            script.write(f"{cpu['cores'] * 2},cores={cpu['cores']}")
        else:
            print(Fore.YELLOW + '[WARNING] Number of cores was not specified. Falling back to 2.' + Fore.RESET)
            script.write("4,cores=2")
        script.write(" \\\n")
        if 'drives' in keys:
            vmfile['disks'] = vmfile['drives']
            keys.append('disks')
        if 'disks' in keys:
            '''
            Reference:     
            -device ich9-ahci,id=sata \\
            -drive id=ESP,if=none,format=qcow2,file=ESP.qcow2 \\
            -device ide-hd,bus=sata.2,drive=ESP \\
            '''
            script.write('\t-device ich9-ahci,id=sata')
            for drive in vmfile['disks']:
                script.write(' \\\n\t')
                id_ = drive['id']
                format_ = drive['format']
                file_ = drive['file']
                if using_libspinup:
                    script.write(f'-drive id={id_},if=none,format={format_},file=\"{vm_loc + "/" + file_}\" \\\n\t')
                else:
                    script.write(f'-drive id={id_},if=none,format={format_},file=\"{file_}\" \\\n\t')
                script.write(f'-device ide-hd,bus=sata.{sataport},drive={id_}')
                sataport += 1
            script.write(' \\\n\t')
        if 'pci_passthrough' in keys:
            print(Fore.YELLOW + '[WARNING] Enabling PCI passthrough requires a change in the GRUB bootloader.' + Fore.RESET)
            VGA_MODE = 'none' # Change the default VGA mode
            script.write('\t-device pcie-root-port,bus=pcie.0,multifunction=on,port=1,chassis=1,id=port.1')
            for device in vmfile['pci_passthrough']:
                script.write(f' \\\n\t-device vfio-pcie,host={device},bus=port.{pcieport},multifunction=on')
                pcieport += 1    
            script.write(' \\\n\t')
        if 'virtual_display_mode' in keys:
            print(Fore.YELLOW + '[WARNING] If you are trying to do GPU Passthrough, the display mode is automatically set to none')
            script.write(f'-vga {vmfile["vga"]} \\\n\t')
        else:
            script.write(f'-vga {VGA_MODE} \\\n\t')
        if 'qemu_args' in keys:
            for i in vmfile['qemu_args']:
                script.write(f'\t-{i["argument"]} {i["value"]} \\\n')
            script.write('\t')
        if 'misc' in keys:
            misc_keys = list(vmfile['misc'].keys())
            misc = vmfile['misc']
            if 'use_ovmf' in misc_keys:
                if misc['use_ovmf']:
                    ovmf_fd_path = os.path.join(firm_path, 'OVMF.fd')
                    if not os.path.exists(firm_path):
                        os.mkdir('firmware')
                    if not os.path.exists(ovmf_fd_path):
                        print(Fore.GREEN + '[NOTE] Donwloading OVMF Firmware' + Fore.RESET)
                        r = requests.get('https://github.com/clearlinux/common/blob/master/OVMF.fd?raw=true')
                        if r.status_code != 200:
                            print(Fore.RED + '[FATAL] Could not download OVMF. Quit.' + Fore.RESET)
                            exit(1)
                        with open(ovmf_fd_path, 'wb') as f:
                            f.write(r.content)
                        print(Fore.GREEN + '[OK] Downloaded OVMF!' + Fore.RESET)
                    script.write(f'-drive if=pflash,format=raw,readonly,file="{ovmf_fd_path}" \\\n')
cli()   
