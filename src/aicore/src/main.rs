//! NEXUS OS AI Core Daemon (`nexus-aid`)
//!
//! Entry point for the local AI proxy multiplexer, hardware governor,
//! OmniRoute gateway, and Ollama backend coordinator.

mod config;
mod hardware;
mod ollama;
mod omniroute;
mod proxy;

use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber)
        .expect("Failed to set tracing subscriber");

    info!("Starting NEXUS OS AI Core Daemon (nexus-aid) v{}", env!("CARGO_PKG_VERSION"));

    let config = config::NexusAIConfig::default();
    info!("AI Proxy listening on {}:{}", config.listen_addr, config.proxy_port);
    info!("OmniRoute Gateway configured at {}", config.omniroute_endpoint);
    info!("Ollama Local Engine configured at {}", config.ollama_endpoint);

    // Initialize hardware watchdog
    let hw = hardware::HardwareMonitor::new();
    hw.log_status();

    // Start local proxy multiplexer
    proxy::start_proxy(config).await?;

    Ok(())
}
