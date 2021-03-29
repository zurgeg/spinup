#!/bin/bash
qemu-sytem-x86-64 \
	-machine q35,kernel_irq_chip=on,accel=kvm \
	-cpu Skylake-Client,kvm=off,+sse2,+sse3,+sse4.2,+aes,+xsave,+avx,+xsaveopt,+xgetbv1,+avx2,+bmi2,+smep,+bmi1,+fma,+movbe,+invtsc \
	-smp 8,cores=4 \
	-device ich9-ahci,id=sata \
	-drive id=drive0,if=none,format=qcow2,file=testing.qcow2 \
	-device ide-hd,bus=sata.0,drive=drive0 \
	-drive if=pflash,format=raw,readonly,file="firmware/OVMF.fd" \
