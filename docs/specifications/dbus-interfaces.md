# Specification: D-Bus Interfaces

All inter-process communication between Nexus background daemons and user-space GUI applications occurs over the user session D-Bus.

## 1. org.nexus.Search (`nexus-searchd`)
- **Service Name**: `org.nexus.Search`
- **Object Path**: `/org/nexus/Search`
- **Interface**: `org.nexus.Search`

### Methods:
- `Query(s term, as categories, u limit) -> (aa{sv} results)`
- `IndexStatus() -> (a{sv} status)`
- `TriggerReindex(as paths) -> (b success)`

---

## 2. org.nexus.Spotlight (`nexus-spotlight`)
- **Service Name**: `org.nexus.Spotlight`
- **Object Path**: `/org/nexus/Spotlight`
- **Interface**: `org.nexus.Spotlight`

### Methods:
- `Toggle()`
- `ShowWithQuery(s query)`
- `Hide()`

---

## 3. org.nexus.AICore (`nexus-aid`)
- **Service Name**: `org.nexus.AICore`
- **Object Path**: `/org/nexus/AICore`
- **Interface**: `org.nexus.AICore`

### Methods:
- `GetHardwareStatus() -> (a{sv} status)`
- `GetActiveModels() -> (as models)`
- `UnloadModel(s model_name) -> (b success)`
- `GetProxyPort() -> (u port)`
