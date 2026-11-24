//! Configuration definitions for Nexus AI Core

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NexusAIConfig {
    pub listen_addr: String,
    pub proxy_port: u16,
    pub ollama_endpoint: String,
    pub omniroute_endpoint: String,
    pub idle_timeout_minutes: u32,
    pub safe_vram_headroom_mb: u64,
}

impl Default for NexusAIConfig {
    fn default() -> Self {
        Self {
            listen_addr: "127.0.0.1".to_string(),
            proxy_port: 11430,
            ollama_endpoint: "http://127.0.0.1:11434".to_string(),
            omniroute_endpoint: "http://127.0.0.1:20128/v1".to_string(),
            idle_timeout_minutes: 15,
            safe_vram_headroom_mb: 2048, // 2GB headroom for desktop compositor
        }
    }
}
