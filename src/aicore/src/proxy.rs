//! OpenAI-compatible HTTP reverse proxy multiplexer

use crate::config::NexusAIConfig;
use axum::{routing::get, Json, Router};
use serde_json::json;
use tracing::info;

pub async fn start_proxy(config: NexusAIConfig) -> anyhow::Result<()> {
    let app = Router::new()
        .route("/v1/models", get(list_models))
        .route("/health", get(health_check));

    let addr = format!("{}:{}", config.listen_addr, config.proxy_port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    info!("AI Core Proxy successfully bound to http://{}", addr);

    axum::serve(listener, app).await?;
    Ok(())
}

async fn health_check() -> Json<serde_json::Value> {
    Json(json!({
        "status": "online",
        "subsystem": "nexus-aid",
        "version": env!("CARGO_PKG_VERSION")
    }))
}

async fn list_models() -> Json<serde_json::Value> {
    Json(json!({
        "object": "list",
        "data": [
            {
                "id": "nexus:default",
                "object": "model",
                "owned_by": "nexus-os"
            }
        ]
    }))
}
