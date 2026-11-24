"""
NEXUS OS — Bootable ISO & Distribution Packaging Test Suite (`tests/test_iso_distribution.py`)
Verifies:
1. ISO image generation and SHA256 checksum integrity.
2. ECMA-119 (ISO9660) PVD and El Torito boot catalog binary standards.
3. Bootloader configurations (GRUB2 UEFI & ISOLINUX BIOS).
4. Fedora Live Workstation Kickstart specification validity.
5. bootc Containerfile reproducible image-mode definition.
6. RPM packaging specifications (nexus-core, nexus-desktop, nexus-devpacks).
7. Virtual Machine test harness execution and 13-stage boot verification.
"""

import os
import sys
import json
import struct
import hashlib
from pathlib import Path
import unittest

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from tools.build_iso import NexusISOBuilder
from tools.vm_test_harness import NexusVMTestHarness


class TestISODistribution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Build the ISO image once for the test suite
        builder = NexusISOBuilder()
        cls.manifest = builder.build()
        cls.iso_path = Path(cls.manifest["iso_path"])
        cls.checksum_path = Path(cls.manifest["checksum_path"])

    def test_01_iso_generation_and_checksum_integrity(self):
        """Verify that ISO image and SHA256 checksum exist and match."""
        self.assertTrue(self.iso_path.exists())
        self.assertGreater(self.iso_path.stat().st_size, 1024 * 1024)
        self.assertTrue(self.checksum_path.exists())

        # Verify SHA256 matches actual file hash
        sha256 = hashlib.sha256()
        with open(self.iso_path, "rb") as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        expected_hash = sha256.hexdigest()
        stored_hash = self.checksum_path.read_text(encoding="utf-8").split()[0]
        self.assertEqual(stored_hash, expected_hash)

    def test_02_iso_ecma119_and_el_torito_binary_standards(self):
        """Verify ISO9660 Primary Volume Descriptor and El Torito catalog offsets."""
        with open(self.iso_path, "rb") as f:
            # Sector 16: PVD
            f.seek(16 * 2048)
            pvd = f.read(2048)
            self.assertEqual(pvd[0], 0x01)
            self.assertEqual(pvd[1:6], b"CD001")
            volume_id = pvd[40:72].decode("ascii").strip()
            self.assertEqual(volume_id, "NEXUS_OS_2026_1")

            # Sector 17: El Torito Volume Descriptor
            f.seek(17 * 2048)
            el_torito = f.read(2048)
            self.assertEqual(el_torito[0], 0x00)
            self.assertEqual(el_torito[1:6], b"CD001")
            self.assertIn(b"EL TORITO SPECIFICATION", el_torito)

            # Sector 19: Boot Catalog Validation Entry
            f.seek(19 * 2048)
            catalog = f.read(2048)
            self.assertEqual(catalog[0], 0x01) # Header ID
            self.assertEqual(catalog[30], 0x55) # Key byte 1
            self.assertEqual(catalog[31], 0xAA) # Key byte 2

            # Checksum of 16 16-bit words must equal 0 mod 65536
            word_sum = sum(struct.unpack("<16H", catalog[0:32])) & 0xFFFF
            self.assertEqual(word_sum, 0)

    def test_03_bootloader_configurations(self):
        """Verify GRUB2 UEFI and ISOLINUX BIOS menu files specify correct kernel arguments."""
        staging_dir = Path(base_dir) / "build" / "iso" / "root"
        grub_cfg = staging_dir / "EFI" / "BOOT" / "grub.cfg"
        isolinux_cfg = staging_dir / "isolinux" / "isolinux.cfg"

        self.assertTrue(grub_cfg.exists())
        self.assertTrue(isolinux_cfg.exists())

        grub_text = grub_cfg.read_text(encoding="utf-8")
        self.assertIn("root=live:CDLABEL=NEXUS_OS_2026_1", grub_text)
        self.assertIn("rd.live.image", grub_text)

        iso_text = isolinux_cfg.read_text(encoding="utf-8")
        self.assertIn("root=live:CDLABEL=NEXUS_OS_2026_1", iso_text)

    def test_04_kickstart_specification(self):
        """Verify Fedora 41 Live Workstation Kickstart configuration."""
        ks_path = Path(base_dir) / "packaging" / "kickstart" / "nexus-live-workstation.ks"
        self.assertTrue(ks_path.exists())
        content = ks_path.read_text(encoding="utf-8")

        self.assertIn("autopart --type=btrfs", content)
        self.assertIn("@kde-desktop", content)
        self.assertIn("plasma-workspace-wayland", content)
        self.assertIn("pipewire", content)
        self.assertIn("podman", content)
        self.assertIn("liveuser", content)
        self.assertIn("privacy.telemetry_enabled", content)

    def test_05_bootc_containerfile(self):
        """Verify cloud-native bootc Containerfile image-mode specification."""
        cfile_path = Path(base_dir) / "packaging" / "bootc" / "Containerfile"
        self.assertTrue(cfile_path.exists())
        content = cfile_path.read_text(encoding="utf-8")

        self.assertIn("FROM quay.io/fedora/fedora-bootc:41", content)
        self.assertIn("plasma-workspace-wayland", content)
        self.assertIn("kwin-wayland", content)
        self.assertIn("nexus-firstboot.sh", content)

    def test_06_rpm_specifications(self):
        """Verify RPM spec files for core, desktop, and devpacks."""
        rpm_dir = Path(base_dir) / "packaging" / "rpm"
        specs = ["nexus-core.spec", "nexus-desktop.spec", "nexus-devpacks.spec"]
        for s in specs:
            sp = rpm_dir / s
            self.assertTrue(sp.exists(), f"Missing spec file: {s}")
            content = sp.read_text(encoding="utf-8")
            self.assertIn("Name:", content)
            self.assertIn("Version:", content)
            self.assertIn("%changelog", content)

    def test_07_vm_test_harness_execution(self):
        """Run full 13-stage VM boot simulation and verification harness."""
        harness = NexusVMTestHarness(str(self.iso_path))
        results = harness.run_all_tests()
        self.assertTrue(results["all_passed"], "VM boot simulation harness failed")
        self.assertEqual(results["stages_count"], 13)


if __name__ == "__main__":
    unittest.main()
