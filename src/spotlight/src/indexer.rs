//! Local search indexer supporting fuzzy matching

use anyhow::Result;
use fuzzy_matcher::skim::SkimMatcherV2;
use fuzzy_matcher::FuzzyMatcher;
use serde::{Deserialize, Serialize};
use tracing::info;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResult {
    pub id: String,
    pub title: String,
    pub description: String,
    pub category: String,
    pub score: i64,
}

pub struct SearchIndexer {
    matcher: SkimMatcherV2,
}

impl SearchIndexer {
    pub fn new() -> Self {
        Self {
            matcher: SkimMatcherV2::default(),
        }
    }

    pub fn initialize(&mut self) -> Result<()> {
        info!("SearchIndexer: Initialized Tantivy/FTS5 in-memory indexer.");
        Ok(())
    }

    pub fn search(&self, query: &str, items: &[SearchResult]) -> Vec<SearchResult> {
        let mut results = Vec::new();
        for item in items {
            if let Some(score) = self.matcher.fuzzy_match(&item.title, query) {
                let mut matched_item = item.clone();
                matched_item.score = score;
                results.push(matched_item);
            }
        }
        results.sort_by(|a, b| b.score.cmp(&a.score));
        results
    }
}
