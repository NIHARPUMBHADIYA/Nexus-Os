//! Ollama integration and process lifecycle manager

pub struct OllamaManager {
    endpoint: String,
}

impl OllamaManager {
    pub fn new(endpoint: String) -> Self {
        Self { endpoint }
    }

    pub fn endpoint(&self) -> &str {
        &self.endpoint
    }
}
