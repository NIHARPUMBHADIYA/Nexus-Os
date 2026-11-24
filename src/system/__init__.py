"""
NEXUS OS — Linux System Integration Subsystem
Provides the integration abstraction layer and environment compatibility detection.
"""

from .compatibility import CompatibilityDetector, CompatibilityReport, EnvironmentType, HardwareTier, SystemCapabilities
from .system_integration import SystemIntegration
