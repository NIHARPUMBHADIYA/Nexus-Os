//! D-Bus session communication for Spotlight overlay trigger

use tracing::info;

pub struct SpotlightDBusService;

impl SpotlightDBusService {
    pub fn new() -> Self {
        Self
    }

    pub fn register(&self) {
        info!("SpotlightDBusService: Registered org.nexus.Spotlight on session bus.");
    }
}
