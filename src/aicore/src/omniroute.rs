//! OmniRoute integration and gateway lifecycle manager for NEXUS OS
//! OmniRoute runs by default on http://127.0.0.1:20128/v1

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OmniRouteStatus {
    pub endpoint: String,
    pub dashboard_url: String,
    pub is_online: bool,
    pub latency_ms: f64,
}

pub struct OmniRouteManager {
    endpoint: String,
    dashboard_url: String,
}

impl OmniRouteManager {
    pub fn new(endpoint: String, dashboard_url: String) -> Self {
        Self {
            endpoint,
            dashboard_url,
        }
    }

    pub fn endpoint(&self) -> &str {
        &self.endpoint
    }

    pub fn dashboard_url(&self) -> &str {
        &self.dashboard_url
    }
}
