#!/usr/bin/env python3

import os
import json
import argparse
from datetime import datetime


def build_tree(root_path, base_path, timestamps):
    tree = {}

    for entry in sorted(os.listdir(root_path)):
        full_path = os.path.join(root_path, entry)

        if os.path.isdir(full_path):
            subtree = build_tree(full_path, base_path, timestamps)
            if subtree:
                tree[entry] = subtree

        elif entry.lower().endswith(".png"):
            rel_path = os.path.relpath(full_path, base_path)
            tree.setdefault("files", []).append(rel_path)
            timestamps.append(os.path.getmtime(full_path))

    return tree


def generate_html(tree_dict, output_path, last_modified):
    timestamp_str = datetime.fromtimestamp(last_modified).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Count total files
    def count_files(node):
        total = len(node.get("files", []))
        for k, v in node.items():
            if k != "files" and isinstance(v, dict):
                total += count_files(v)
        return total

    total_plots = count_files(tree_dict)
    total_folders = sum(1 for k in tree_dict if k != "files")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plot Viewer — Physics Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* ── Design tokens ── */
:root {{
  --bg:         #f5f6f8;
  --surface:    #ffffff;
  --surface2:   #f0f1f4;
  --surface3:   #e8eaef;
  --border:     #dde0e7;
  --border2:    #c8cdd8;
  --accent:     #4f6ef7;
  --accent2:    #3a56e0;
  --accent-dim: #4f6ef712;
  --gold:       #e09c20;
  --green:      #22a06b;
  --red:        #e5484d;
  --text:       #1a1d23;
  --text-muted: #5a6070;
  --text-dim:   #9aa0ad;
  --mono:       'IBM Plex Mono', monospace;
  --sans:       'IBM Plex Sans', sans-serif;
  --radius:     6px;
  --radius-lg:  10px;
}}

body.dark {{
  --bg:         #12151c;
  --surface:    #1a1e28;
  --surface2:   #1f2433;
  --surface3:   #252b3b;
  --border:     #2a3248;
  --border2:    #334060;
  --accent-dim: #4f6ef718;
  --text:       #e8ecf4;
  --text-muted: #8090a8;
  --text-dim:   #4a5870;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{ scroll-behavior: smooth; }}

body {{
  font-family: var(--sans);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  transition: background 0.25s, color 0.25s;
  /* Very subtle dot grid */
  background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
  background-size: 28px 28px;
  background-attachment: fixed;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent2); }}

/* ── HEADER ── */
.header {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 56px;
}}

.header-left {{
  display: flex;
  align-items: center;
  gap: 16px;
}}

.logo-mark {{
  width: 36px;
  height: 36px;
  border: 2px solid var(--accent);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}}
.logo-mark::after {{
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent-dim);
}}
.logo-mark svg {{ position: relative; z-index: 1; }}

.header-title {{
  font-family: var(--mono);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.02em;
}}
.header-subtitle {{
  font-size: 0.7rem;
  color: var(--text-muted);
  font-family: var(--mono);
  margin-top: 1px;
}}

.header-right {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}}

/* ── STATS BAR ── */
.stats-bar {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}}

.stat {{
  display: flex;
  align-items: baseline;
  gap: 6px;
}}
.stat-value {{
  font-family: var(--mono);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--accent);
}}
.stat-label {{
  font-size: 0.7rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}

.stats-divider {{
  width: 1px;
  height: 20px;
  background: var(--border);
}}

.timestamp {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.ts-dot {{
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--green);
  animation: pulse-dot 2s ease-in-out infinite;
}}
@keyframes pulse-dot {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50% {{ opacity: 0.5; transform: scale(0.8); }}
}}

/* ── CONTROLS ── */
.controls {{
  padding: 8px 16px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}}

.btn {{
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: var(--radius);
  border: 1px solid var(--border2);
  background: var(--surface3);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  letter-spacing: 0.02em;
}}
.btn:hover {{
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-dim);
}}
.btn.accent {{
  border-color: var(--accent2);
  color: var(--accent);
  background: var(--accent-dim);
}}
.btn.accent:hover {{
  background: rgba(0,200,255,0.12);
}}
.btn svg {{ width: 12px; height: 12px; flex-shrink: 0; }}

.search-wrap {{
  position: relative;
  margin-left: auto;
}}
.search-wrap svg {{
  position: absolute;
  left: 10px; top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  width: 13px; height: 13px;
  pointer-events: none;
}}
.search-input {{
  font-family: var(--mono);
  font-size: 0.75rem;
  padding: 6px 12px 6px 30px;
  width: 220px;
  background: var(--surface3);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  color: var(--text);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}}
.search-input::placeholder {{ color: var(--text-dim); }}
.search-input:focus {{
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-dim);
}}

/* ── GRID SIZE TOGGLE ── */
.grid-toggle {{
  display: flex;
  gap: 2px;
  padding: 3px;
  background: var(--surface3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}}
.gtb {{
  padding: 4px 8px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.7rem;
  font-family: var(--mono);
  transition: all 0.12s;
}}
.gtb.active, .gtb:hover {{
  background: var(--surface);
  color: var(--accent);
}}

/* ── MAIN CONTAINER ── */
.container {{
  padding: 14px 16px;
  max-width: 100%;
  margin: 0 auto;
}}

/* ── FOLDER CARD ── */
.folder {{
  margin-bottom: 10px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color 0.2s;
  animation: fade-in 0.3s ease both;
}}
.folder:hover {{ border-color: var(--border2); }}
@keyframes fade-in {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.folder-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 13px 18px;
  cursor: pointer;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
  user-select: none;
}}
.folder-header:hover {{ background: var(--surface3); }}

.folder-title {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.folder-icon {{
  width: 28px; height: 28px;
  border-radius: 6px;
  background: var(--accent-dim);
  border: 1px solid var(--accent2);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}}
.folder-icon svg {{ color: var(--accent); width: 14px; height: 14px; }}

.folder-name {{
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text);
  letter-spacing: 0.01em;
}}
.folder-count {{
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--text-muted);
  background: var(--surface3);
  border: 1px solid var(--border);
  padding: 1px 7px;
  border-radius: 10px;
}}

.folder-meta {{
  display: flex;
  align-items: center;
  gap: 8px;
}}
.folder-toggle {{
  width: 22px; height: 22px;
  border-radius: 4px;
  border: 1px solid var(--border2);
  background: var(--surface3);
  color: var(--text-muted);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.6rem;
}}
.folder-toggle:hover {{ border-color: var(--accent); color: var(--accent); }}

/* ── NESTED FOLDER ── */
.folder-body {{ padding: 10px; }}
.folder .folder {{
  border-color: var(--border);
  background: var(--surface2);
}}
.folder .folder .folder-header {{ background: var(--surface3); }}
.folder .folder .folder-body {{ background: var(--surface2); }}

/* ── IMAGE GRID ── */
.grid {{
  display: grid;
  grid-template-columns: repeat(var(--cols, 4), 1fr);
  gap: 8px;
  margin-bottom: 8px;
}}
.grid-item {{
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--surface3);
  border: 1px solid var(--border);
  aspect-ratio: 4/3;
  cursor: pointer;
  transition: all 0.2s;
  group: '';
}}
.grid-item:hover {{
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent), 0 8px 24px rgba(0,200,255,0.12);
  transform: translateY(-2px);
}}
.grid-item img {{
  width: 100%; height: 100%;
  object-fit: contain;
  display: block;
  padding: 4px;
}}
.grid-item-label {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 6px 8px 5px;
  background: linear-gradient(transparent, rgba(0,0,0,0.55));
  font-family: var(--mono);
  font-size: 0.6rem;
  color: rgba(255,255,255,0.92);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0;
  transition: opacity 0.2s;
}}
.grid-item:hover .grid-item-label {{ opacity: 1; }}

/* Expand corner icon */
.grid-item-expand {{
  position: absolute;
  top: 6px; right: 6px;
  width: 22px; height: 22px;
  border-radius: 4px;
  background: rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  color: white;
}}
.grid-item:hover .grid-item-expand {{ opacity: 1; }}

/* ── HIDDEN ── */
.hidden {{ display: none !important; }}

/* ── LIGHTBOX MODAL ── */
.modal {{
  display: none;
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(5, 10, 20, 0.92);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  animation: modal-in 0.18s ease;
}}
@keyframes modal-in {{
  from {{ opacity: 0; }}
  to   {{ opacity: 1; }}
}}
.modal-inner {{
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}}
.modal img {{
  max-width: 90vw;
  max-height: 80vh;
  object-fit: contain;
  border-radius: var(--radius);
  border: 1px solid var(--border2);
  box-shadow: 0 24px 80px rgba(0,0,0,0.7);
  animation: img-pop 0.2s cubic-bezier(.2,.8,.3,1.1);
}}
@keyframes img-pop {{
  from {{ transform: scale(0.93); opacity: 0; }}
  to   {{ transform: scale(1); opacity: 1; }}
}}
.modal-caption {{
  margin-top: 14px;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: center;
  max-width: 600px;
}}
.modal-close {{
  position: absolute;
  top: 18px; right: 22px;
  width: 34px; height: 34px;
  border-radius: 50%;
  border: 1px solid var(--border2);
  background: var(--surface2);
  color: var(--text-muted);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
  transition: all 0.15s;
  z-index: 10;
}}
.modal-close:hover {{ border-color: var(--red); color: var(--red); background: rgba(255,95,109,0.1); }}
.modal-nav {{
  position: absolute;
  top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px;
  border-radius: 50%;
  border: 1px solid var(--border2);
  background: var(--surface2);
  color: var(--text-muted);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  transition: all 0.15s;
}}
.modal-nav:hover {{ border-color: var(--accent); color: var(--accent); background: var(--accent-dim); }}
.modal-nav.prev {{ left: 18px; }}
.modal-nav.next {{ right: 18px; }}
.modal-counter {{
  position: absolute;
  bottom: 18px;
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--text-dim);
  letter-spacing: 0.1em;
}}

/* ── FOOTER ── */
footer {{
  margin-top: 40px;
  border-top: 1px solid var(--border);
  background: var(--surface);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}}
.footer-brand {{
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--text-muted);
}}
.footer-brand strong {{ color: var(--accent); }}
.footer-meta {{
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--text-dim);
}}

/* ── NO RESULTS ── */
.no-results {{
  text-align: center;
  padding: 60px 20px;
  color: var(--text-dim);
  font-family: var(--mono);
  font-size: 0.8rem;
}}
.no-results svg {{ width: 40px; height: 40px; margin-bottom: 12px; color: var(--text-dim); }}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {{
  .header {{ padding: 0 10px; height: auto; padding-top: 10px; padding-bottom: 10px; }}
  .stats-bar, .controls, .container {{ padding-left: 10px; padding-right: 10px; }}
  .grid {{ --cols: 2 !important; }}
  .search-input {{ width: 140px; }}
  .timestamp {{ display: none; }}
  footer {{ flex-direction: column; text-align: center; padding: 12px 10px; }}
}}
</style>
</head>
<body>

<!-- HEADER -->
<header class="header">
  <div class="header-left">
    <div class="logo-mark">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--accent)">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
      </svg>
    </div>
    <div>
      <div class="header-title">Plot Viewer</div>
      <div class="header-subtitle">Physics Dashboard</div>
    </div>
  </div>
  <div class="header-right">
    <div class="grid-toggle">
      <button class="gtb" onclick="setGrid(3)" title="3 columns">▦ 3</button>
      <button class="gtb active" onclick="setGrid(4)" title="4 columns">▦ 4</button>
      <button class="gtb" onclick="setGrid(6)" title="6 columns">▦ 6</button>
    </div>
  </div>
</header>

<!-- STATS BAR -->
<div class="stats-bar">
  <div class="stat">
    <span class="stat-value" id="stat-plots">{total_plots}</span>
    <span class="stat-label">Plots</span>
  </div>
  <div class="stats-divider"></div>
  <div class="stat">
    <span class="stat-value" id="stat-folders">{total_folders}</span>
    <span class="stat-label">Folders</span>
  </div>
  <div class="stats-divider"></div>
  <div class="stat">
    <span class="stat-value" id="stat-visible">—</span>
    <span class="stat-label">Visible</span>
  </div>
  <div class="timestamp">
    <div class="ts-dot"></div>
    Last updated: <span style="color:var(--text)">{timestamp_str}</span>
  </div>
</div>

<!-- CONTROLS -->
<div class="controls">
  <button class="btn accent" onclick="expandAll()">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>
    Expand All
  </button>
  <button class="btn" onclick="collapseAll()">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 11 12 6 17 11"/><polyline points="7 18 12 13 17 18"/></svg>
    Collapse All
  </button>
  <button class="btn" onclick="toggleTheme()">
    <svg id="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
    <span id="theme-label">Dark Mode</span>
  </button>
  <button class="btn" onclick="location.reload()">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
    Refresh
  </button>
  <div class="search-wrap">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <input class="search-input" type="text" id="searchBox" placeholder="Search plots…" oninput="searchPlots()" autocomplete="off" spellcheck="false">
  </div>
</div>

<!-- MAIN CONTENT -->
<div class="container" id="viewer"></div>

<!-- LIGHTBOX -->
<div class="modal" id="modal">
  <div class="modal-inner">
    <button class="modal-close" onclick="closeModal()" title="Close (Esc)">✕</button>
    <button class="modal-nav prev" onclick="navModal(-1)" title="Previous">‹</button>
    <button class="modal-nav next" onclick="navModal(1)" title="Next">›</button>
    <img id="modal-img" src="" alt="">
    <div class="modal-caption" id="modal-caption"></div>
    <div class="modal-counter" id="modal-counter"></div>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <div class="footer-brand">
    <strong>Plot Viewer</strong> — Physics Dashboard &nbsp;·&nbsp; Arnab Laha & Claude
  </div>
  <div class="footer-meta">Generated {timestamp_str} &nbsp;·&nbsp; {total_plots} plots across {total_folders} folders</div>
</footer>

<script>
const data = {json.dumps(tree_dict, indent=2)};

/* ── State ── */
let gridCols   = 4;
let allImages  = [];   // {{ src, name, folderName }} for lightbox
let modalIdx   = 0;
let isDark     = false;

/* ── Build DOM ── */
function createFolder(name, content, depth) {{
  depth = depth || 0;

  const files    = content.files || [];
  const pngFiles = files.filter(f => f.toLowerCase().endsWith('.png'));
  const subKeys  = Object.keys(content).filter(k => k !== 'files');
  const total    = pngFiles.length;

  const card = document.createElement('div');
  card.className = 'folder';
  card.style.animationDelay = (depth * 0.04) + 's';

  /* Header */
  const hdr = document.createElement('div');
  hdr.className = 'folder-header';

  const titleWrap = document.createElement('div');
  titleWrap.className = 'folder-title';
  titleWrap.innerHTML = `
    <div class="folder-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
      </svg>
    </div>
    <span class="folder-name">${{name}}</span>
    <span class="folder-count">${{total}} file${{total !== 1 ? 's' : ''}}</span>
  `;

  const metaWrap = document.createElement('div');
  metaWrap.className = 'folder-meta';

  const toggleBtn = document.createElement('div');
  toggleBtn.className = 'folder-toggle';
  toggleBtn.innerHTML = '▸';
  metaWrap.appendChild(toggleBtn);

  hdr.appendChild(titleWrap);
  hdr.appendChild(metaWrap);
  card.appendChild(hdr);

  /* Body */
  const body = document.createElement('div');
  body.className = 'folder-body hidden';
  card.appendChild(body);

  /* Toggle */
  hdr.onclick = () => {{
    const open = body.classList.toggle('hidden');
    toggleBtn.innerHTML = body.classList.contains('hidden') ? '▸' : '▾';
    // icon rotation handled via innerHTML
  }};

  /* PNG Grid */
  if (pngFiles.length > 0) {{
    const grid = document.createElement('div');
    grid.className = 'grid';
    grid.style.setProperty('--cols', gridCols);

    pngFiles.forEach(f => {{
      const fname = f.split('/').pop();
      const startIdx = allImages.length;
      allImages.push({{ src: f, name: fname, folder: name }});

      const item = document.createElement('div');
      item.className = 'grid-item';
      item.dataset.name = f.toLowerCase();
      item.dataset.imgidx = startIdx;

      item.innerHTML = `
        <img src="${{f}}" alt="${{fname}}" loading="lazy">
        <div class="grid-item-label">${{fname}}</div>
        <div class="grid-item-expand">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
        </div>
      `;
      item.onclick = () => openModal(startIdx);
      grid.appendChild(item);
    }});

    body.appendChild(grid);
  }}

  /* Subfolders */
  subKeys.forEach(k => {{
    body.appendChild(createFolder(k, content[k], depth + 1));
  }});

  return card;
}}

/* ── Populate viewer ── */
const viewer = document.getElementById('viewer');
for (const k in data) {{
  viewer.appendChild(createFolder(k, data[k], 0));
}}
updateVisibleCount();

/* ── Grid size ── */
function setGrid(n) {{
  gridCols = n;
  document.querySelectorAll('.grid').forEach(g => g.style.setProperty('--cols', n));
  document.querySelectorAll('.gtb').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}}

/* ── Expand / Collapse ── */
function expandAll() {{
  document.querySelectorAll('.folder-body').forEach(b => {{
    b.classList.remove('hidden');
  }});
  document.querySelectorAll('.folder-toggle').forEach(t => t.innerHTML = '▾');
  updateVisibleCount();
}}
function collapseAll() {{
  document.querySelectorAll('.folder-body').forEach(b => b.classList.add('hidden'));
  document.querySelectorAll('.folder-toggle').forEach(t => t.innerHTML = '▸');
  updateVisibleCount();
}}
/* ── Theme ── */
function toggleTheme() {{
  isDark = !isDark;
  document.body.classList.toggle('dark', isDark);
  document.getElementById('theme-label').textContent = isDark ? 'Light Mode' : 'Dark Mode';
  const icon = document.getElementById('theme-icon');
  icon.innerHTML = isDark
    ? '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>'
    : '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
}}

/* ── Search ── */
function searchPlots() {{
  const q = document.getElementById('searchBox').value.toLowerCase();
  document.querySelectorAll('.grid-item').forEach(item => {{
    const match = !q || item.dataset.name.includes(q);
    item.style.display = match ? '' : 'none';
  }});
  if (q) expandAll();
  updateVisibleCount();
}}

function updateVisibleCount() {{
  const visible = document.querySelectorAll('.grid-item:not([style*="display: none"])').length;
  document.getElementById('stat-visible').textContent = visible;
}}

/* ── Lightbox ── */
function openModal(idx) {{
  modalIdx = idx;
  showModalImage();
  document.getElementById('modal').style.display = 'block';
  document.body.style.overflow = 'hidden';
}}
function showModalImage() {{
  const item = allImages[modalIdx];
  document.getElementById('modal-img').src = item.src;
  document.getElementById('modal-caption').textContent = item.name;
  document.getElementById('modal-counter').textContent =
    (modalIdx + 1) + ' / ' + allImages.length + '  ·  ' + item.folder;
}}
function navModal(dir) {{
  modalIdx = (modalIdx + dir + allImages.length) % allImages.length;
  showModalImage();
}}
function closeModal() {{
  document.getElementById('modal').style.display = 'none';
  document.body.style.overflow = '';
}}
document.getElementById('modal').addEventListener('click', function(e) {{
  if (e.target === this || e.target === document.querySelector('.modal-inner')) closeModal();
}});

/* Keyboard navigation */
document.addEventListener('keydown', e => {{
  if (document.getElementById('modal').style.display !== 'block') return;
  if (e.key === 'Escape')      closeModal();
  if (e.key === 'ArrowRight')  navModal(1);
  if (e.key === 'ArrowLeft')   navModal(-1);
}});
</script>
</body>
</html>
"""

    with open(output_path, "w") as f:
        f.write(html)

    print(f"✓ Generated: {output_path}")
    print(f"  {total_plots} plots · {total_folders} folders")


def main():
    parser = argparse.ArgumentParser(description="Generate a physics plot dashboard")
    parser.add_argument("folder", help="Root folder containing plots")
    parser.add_argument("--name", default="index.html", help="Output filename")
    args = parser.parse_args()

    root = os.path.abspath(args.folder)
    timestamps = []

    tree = build_tree(root, root, timestamps)
    last_modified = max(timestamps) if timestamps else datetime.now().timestamp()

    output_path = os.path.join(root, args.name)
    generate_html(tree, output_path, last_modified)


if __name__ == "__main__":
    main()
