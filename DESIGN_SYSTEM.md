# NEXUS Aether Design System

> **Specification Version:** 2.0.0  
> **Target Frameworks:** Qt 6 / QML, Kirigami, Slint, Modern Web, KWin Shaders  
> **Core Aesthetic:** Professional Developer Minimalist, macOS-level Refinement, Clean KDE Flexibility, Precision Geometry  

---

## 1. Design Philosophy

The **NEXUS Aether Design System** is engineered specifically for software engineers, systems programmers, AI practitioners, and technical creators. 

### Core Tenets:
1. **Developer-First Elegance**: Restrained, functional, uncluttered surfaces. Avoid gratuitous glow, distracting neon outlines, or visual noise.
2. **Harmonious Geometry**: Consistent, rounded corner radiuses across every window, card, dialog, floating dock, and input control.
3. **High-Information Density with Visual Breathing Room**: Compact, proportional spacing scale and clear optical hierarchy that maximizes code and terminal real estate.
4. **Accessible Contrast (WCAG 2.1 AA+)**: Crisp contrast across all dark and light themes.
5. **Fluid, Subtle Motion**: Micro-interactions that inform state changes (<180ms) with zero latency for power users, plus complete compliance with reduced-motion preferences.

---

## 2. Corner Radii Hierarchy

All NEXUS OS user interfaces adhere strictly to the **Corner Radii Tokens**:

```
+-----------------------------------------------------------------------------+
| TOKEN        | VALUE  | PRIMARY APPLICATION                                 |
+--------------+--------+-----------------------------------------------------+
| radius-sm    | 10px   | Buttons, text inputs, search fields, tags, micro-UI |
| radius-md    | 14px   | Cards, dropdown menus, code blocks, popovers        |
| radius-lg    | 20px   | Modal dialogs, window panels, settings cards        |
| radius-xl    | 24px   | Floating Dock, Universal Spotlight HUD, Overlays    |
| radius-xxl   | 28px   | Application main windows, system shell viewports    |
| radius-pill  | 9999px | Status badges, search pills, segmented tab pills    |
+-----------------------------------------------------------------------------+
```

---

## 3. Spacing Scale

The spacing scale provides predictable spatial cadence across all layouts:

```
+-------------------------------------------------------------------------+
| TOKEN    | VALUE | USAGE                                                |
+----------+-------+------------------------------------------------------+
| space-1  | 2px   | Micro borders, inline separators                     |
| space-2  | 4px   | Tight badge margins, dot spacings                    |
| space-3  | 8px   | Button icon gaps, compact item padding               |
| space-4  | 12px  | Input padding, dock item spacing, card headers       |
| space-5  | 16px  | Standard card internal padding, toolbar margins      |
| space-6  | 20px  | Modal margins, section gutters                       |
| space-7  | 24px  | Window outer gutters, dashboard layouts              |
| space-8  | 32px  | Major section separations                            |
| space-9  | 40px  | Hero headers                                         |
| space-10 | 48px  | Large screen layout gutters                          |
| space-12 | 64px  | Desktop viewport outer margins                       |
+-------------------------------------------------------------------------+
```

---

## 4. Semantic Color System

NEXUS OS defines 12 core semantic color tokens that adapt seamlessly across dark and light palettes.

### 4.1. Semantic Color Token Roles
- `background`: Canvas background of active applications and desktop shell.
- `secondaryBackground`: Recessed sidebars, toolbars, and input field backgrounds.
- `surface`: Elevated cards, toolbars, and container components.
- `elevatedSurface`: High-elevation overlays, floating dock, modal dialogs, and popovers.
- `border`: Subtle, low-contrast component and panel separators.
- `primaryText`: High-contrast body text and titles (95% contrast).
- `secondaryText`: Muted metadata, descriptions, git tags, and subtitles.
- `tertiaryText`: Disabled states, subtle shortcut hints, and placeholders.
- `accent`: Primary brand and focus indicator (user-customizable).
- `success`: Positive states, clean working trees, successful builds, online services.
- `warning`: Cautions, high VRAM alerts, dirty git branches.
- `error`: Destructive actions, compiler errors, container crashes.
- `info`: System information, downloading models, active background tasks.

---

## 5. Built-In Themes (9 Initial Themes)

NEXUS OS ships with 9 curated themes out of the box:

```
+--------------------------------------------------------------------------------------------+
| THEME           | TYPE  | BG COLOR | SURFACE  | ACCENT   | DESCRIPTION                     |
+-----------------+-------+----------+----------+----------+---------------------------------+
| Midnight        | Dark  | #0B0D14  | #171B2B  | #6366F1  | Default Obsidian dark aesthetic |
| Nord            | Dark  | #242933  | #3B4252  | #88C0D0  | Clean arctic polar night        |
| Dracula         | Dark  | #1E1F29  | #343746  | #BD93F9  | Gothic developer palette        |
| Catppuccin      | Dark  | #181825  | #313244  | #CBA6F7  | Soothing pastel low-strain dark |
| Tokyo Night     | Dark  | #16161E  | #24283B  | #7AA2F7  | Cybernetic downtown Tokyo blues |
| Terminal Green  | Dark  | #050B06  | #0F1E12  | #22C55E  | Monochromatic hacker phosphor   |
| Paper Light     | Light | #FBFBFA  | #FFFFFF  | #4F46E5  | High-contrast crisp book paper  |
| AMOLED          | Dark  | #000000  | #121212  | #6366F1  | True #000000 pure OLED black    |
| Deep Space      | Dark  | #030712  | #0D1938  | #0284C7  | Interstellar cosmic navy        |
+--------------------------------------------------------------------------------------------+
```

### 5.1. Customizable Accent Colors
Users can select custom accent colors or override the theme default:
- **Nexus Indigo**: `#6366F1`
- **Cyber Emerald**: `#10B981`
- **Amber Glow**: `#F59E0B`
- **Crimson Red**: `#EF4444`
- **Sky Cyan**: `#06B6D4`
- **Electric Violet**: `#8B5CF6`
- **Rose Blush**: `#F43F5E`
- **Deep Sky**: `#0284C7`

---

## 6. Community Theme Architecture

NEXUS OS features a declarative JSON schema for community themes located at `src/design-system/themes/schema.json`.

To install or create a custom community theme:
1. Create a JSON file in `~/.config/nexus/themes/<theme-id>.json`.
2. Follow the required schema:
```json
{
  "id": "solarized-dark",
  "name": "Solarized Dark",
  "author": "Community Creator",
  "version": "1.0.0",
  "type": "dark",
  "colors": {
    "background": "#002B36",
    "secondaryBackground": "#073642",
    "surface": "#073642",
    "elevatedSurface": "#0E4856",
    "border": "#1A5666",
    "borderFocus": "#268BD2",
    "primaryText": "#93A1A1",
    "secondaryText": "#586E75",
    "tertiaryText": "#657B83",
    "accent": "#268BD2",
    "accentHover": "#2AA198",
    "accentSubtle": "#003F4D",
    "success": "#859900",
    "successSubtle": "#0F4010",
    "warning": "#B58900",
    "warningSubtle": "#403305",
    "error": "#DC322F",
    "errorSubtle": "#421514",
    "info": "#2AA198",
    "infoSubtle": "#0A3B37"
  }
}
```

---

## 7. Reusable Component Library

The design system implements 17 reusable Qt6/QML and CSS components:

| Component | QML Component | Key Features |
| :--- | :--- | :--- |
| **Button** | `NexusButton.qml` | Variants: `primary`, `secondary`, `subtle`, `outline`, `danger`, `ghost`. Shapes: `rounded` (10px), `pill`. Loading spinner, hover animations. |
| **Icon Button** | `NexusIconButton.qml` | Hover states, active accent states, built-in tooltip positioning. |
| **Input** | `NexusInput.qml` | Leading icon, placeholder, clear button, password echo mode, validation error badge. |
| **Search Field** | `NexusSearchField.qml` | Leading search icon, clear button, keyboard shortcut pill (`Win+Space` / `Ctrl+K`). |
| **Card** | `NexusCard.qml` | Interactive hover elevation, top accent strip, title/subtitle header. |
| **Dialog** | `NexusDialog.qml` | Modal overlay with backdrop blur, centered card (20px radius), confirm/cancel buttons. |
| **Popover** | `NexusPopover.qml` | Floating container with 14px radius and elevation shadow. |
| **Menu** | `NexusMenu.qml` | Dropdown items with icons, shortcut indicators, separators, and hover highlights. |
| **Tooltip** | `NexusTooltip.qml` | Compact 10px pill with high-contrast text and subtle hover delay. |
| **Tabs** | `NexusTabs.qml` | Variants: `segmented` (inset container), `pills` (rounded pills), `underline`. |
| **Toggle** | `NexusToggle.qml` | Animated switch, checkbox with check icon, radio button with dot indicator. |
| **Progress** | `NexusProgress.qml` | Linear bar with determinate value (0.0-1.0) and indeterminate wave; circular spinner. |
| **Notification** | `NexusNotification.qml` | Toast banners with variants: `info`, `success`, `warning`, `error`; dismiss button. |
| **Dock Item** | `NexusDockItem.qml` | Floating dock application item with hover lift (-6px), running indicator dot, badge count. |
| **Window Header** | `NexusWindowHeader.qml` | Traffic light controls (close, minimize, maximize), centered title, action button slot. |
| **Sidebar Nav** | `NexusSidebar.qml` | Navigation list with active indicator pill, icon, label, and counter badge. |
| **Badge** | `NexusBadge.qml` | Status pill with dot indicator, numeric count pill, tag badge. |

---

## 8. Typography Scale

- **UI Interface Font**: `'Inter', 'Segoe UI', system-ui, sans-serif`
- **Monospace Code Font**: `'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace`

```
+-------------------------------------------------------------------------+
| TOKEN        | SIZE  | LINE HEIGHT | WEIGHT | PRIMARY USE               |
+--------------+-------+-------------+--------+---------------------------+
| display      | 28px  | 36px        | 600    | Main DevHub & Welcome     |
| h1           | 22px  | 28px        | 600    | Primary section titles    |
| h2           | 18px  | 24px        | 600    | Card & modal headers      |
| h3           | 15px  | 20px        | 600    | Group & sidebar headers   |
| body-lg      | 15px  | 22px        | 400    | Readme text, dialog body  |
| body         | 13px  | 18px        | 400    | Standard UI text          |
| body-sm      | 12px  | 16px        | 400    | Descriptions, subtitles   |
| caption      | 11px  | 14px        | 500    | Metadata, git tags, pills |
| code         | 12px  | 18px        | 400    | Code snippets, file paths |
+-------------------------------------------------------------------------+
```

---

## 9. Animation & Motion Tokens

```
+-------------------------------------------------------------------------+
| TOKEN           | DURATION | EASING                     | USAGE         |
+-----------------+----------+----------------------------+---------------+
| durationFast    | 120ms    | cubic-bezier(0.16, 1, 0.3, 1)| Hover, clicks |
| durationNormal  | 180ms    | cubic-bezier(0.16, 1, 0.3, 1)| Tabs, dialogs |
| durationSlow    | 280ms    | cubic-bezier(0.16, 1, 0.3, 1)| Theme shifts  |
+-------------------------------------------------------------------------+
```

When `NexusTheme.reducedMotion` is enabled, all duration tokens collapse to `0ms`.

---

## 10. Running the Design System Showcase

You can run and preview the design system in two environments:

### Native Desktop Preview (PyQt6 / QML):
```bash
python tools/showcase.py
```

### Interactive Web Preview (Browser):
```bash
python tools/preview_server.py
# Opens at http://localhost:8080
```

### Automated Test Verification:
```bash
python tests/test_design_system.py
```
