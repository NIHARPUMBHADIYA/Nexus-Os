//! NEXUS OS Spotlight Search Engine & Daemon
//!
//! Provides instant local fuzzy search across apps, files, git repositories,
//! and developer environments.

mod dbus;
mod indexer;

use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber)
        .expect("Failed to set tracing subscriber");

    info!("Starting NEXUS Spotlight Daemon (nexus-searchd) v{}", env!("CARGO_PKG_VERSION"));

    let mut indexer = indexer::SearchIndexer::new();
    indexer.initialize()?;

    info!("Spotlight search index ready. Listening for query events...");
    Ok(())
}
