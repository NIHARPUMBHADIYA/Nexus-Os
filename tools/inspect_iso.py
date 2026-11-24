import os
import struct

ISO_PATH = r"C:\Users\HP\Downloads\cutefish-1.0-nightly-20261119-1449-amd64.iso"

with open(ISO_PATH, "rb") as f:
    # 1. PVD at sector 16
    f.seek(16 * 2048)
    pvd = f.read(2048)
    vol_id = pvd[40:72].decode("latin1", errors="replace").strip()
    root_extent = struct.unpack_from("<I", pvd, 158)[0]
    root_len = struct.unpack_from("<I", pvd, 166)[0]
    print(f"PVD: Volume ID='{vol_id}', Root Extent={root_extent}, Root Len={root_len}")

    # 2. Search for boot configs in first 20MB
    f.seek(0)
    data = f.read(20 * 1024 * 1024)
    for name, target in [
        ("live.cfg", b"label live-amd64"),
        ("grub.cfg", b"menuentry \"Live system"),
        ("menu.cfg", b"menu.cfg"),
        ("stdmenu.cfg", b"stdmenu.cfg")
    ]:
        idx = data.find(target)
        if idx != -1:
            print(f"Found {name} at offset {idx} (sector {idx // 2048})")
        else:
            print(f"{name} not found in first 20MB")
