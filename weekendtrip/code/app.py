import streamlit as st
from streamlit_folium import st_folium
import folium
import json, pathlib
from folium.plugins import MarkerCluster
import time
from datetime import datetime
import urllib.parse, os
import pathlib, stat


st.set_page_config(page_title="Weekend Spots Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Weekend Spots — Click a pin to open the listing")

st.markdown(
    """
This map pins your saved places. Pins are approximate when exact GPS wasn't publicly listed.
Click a marker, then the link in the popup to open the listing in a new tab.
"""
)

# Paths
DATA_PATH = pathlib.Path(__file__).parent / "places.json"
PLACES_DIR = pathlib.Path(os.environ.get("PLACES_DIR", "/data/places"))
ENABLE_IMPORTS = os.environ.get("ENABLE_IMPORTS", "true").lower() == "true"
try:
    PLACES_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    import streamlit as st
    st.error(f"No write access to {PLACES_DIR}. Set PLACES_DIR to a writable PVC mount.")
# Ensure import directory exists (we will WRITE here)
PLACES_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_ICON = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png"

PREVIEW_PROVIDER = os.environ.get("PREVIEW_PROVIDER", "thumio")
PREVIEW_WIDTH = int(os.environ.get("PREVIEW_WIDTH", "500"))     # px of screenshot width
PREVIEW_CROP  = int(os.environ.get("PREVIEW_CROP", "350"))      # px crop height
ENABLE_PREVIEWS = os.environ.get("ENABLE_PREVIEWS", "true").lower() == "true"

# --- Validation and helpers ---
def validate_item(item: dict, source: str = "") -> dict:
    """
    Validate and normalize a place item.
    Required: title(str), url(str), lat(float), lon(float)
    Optional: price(str), note(str)
    Returns a cleaned dict or raises ValueError.
    """
    if not isinstance(item, dict):
        raise ValueError(f"{source}: item is not an object")

    def req(k, typ=str):
        if k not in item:
            raise ValueError(f"{source}: missing '{k}'")
        return item[k]

    title = str(req("title")).strip()
    url = str(req("url")).strip()
    if not title:
        raise ValueError(f"{source}: empty title")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError(f"{source}: url must start with http(s)://")

    try:
        lat = float(req("lat", float))
        lon = float(req("lon", float))
    except Exception:
        raise ValueError(f"{source}: lat/lon must be numbers")

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise ValueError(f"{source}: lat/lon out of range")

    cleaned = {"title": title, "url": url, "lat": lat, "lon": lon}
    # Optional fields
    if "price" in item and str(item["price"]).strip():
        cleaned["price"] = str(item["price"]).strip()
    if "note" in item and str(item["note"]).strip():
        cleaned["note"] = str(item["note"]).strip()
    return cleaned

def domain_of(url: str) -> str:
    try:
        netloc = urllib.parse.urlparse(url).netloc
        return netloc.lower()
    except Exception:
        return ""

def screenshot_preview_url(target_url: str) -> str | None:
    if not ENABLE_PREVIEWS:
        return None
    if PREVIEW_PROVIDER == "thumio":
        # Free, no-key endpoint (rate-limited, watermark). Docs: https://thumb.io / thum.io
        # Example: https://image.thum.io/get/width/500/crop/350/https://example.com
        safe = urllib.parse.quote(target_url, safe=":/?#[]@!$&'()*+,;=%")
        return f"https://image.thum.io/get/width/{PREVIEW_WIDTH}/crop/{PREVIEW_CROP}/{safe}"
    # Add other providers here (see “Other providers” below)
    return None

def favicon_for(url: str) -> str:
    # Fast, no-auth favicon service (works for most domains)
    dom = domain_of(url)
    return f"https://icons.duckduckgo.com/ip3/{dom}.ico" if dom else ""

def normalize_url(url: str, ignore_query: bool = True) -> str:
    """Return a canonical URL string for deduplication.
    - Drops fragment
    - For known listing sites always drop query (tracking/noise)
    - Otherwise drop query when ignore_query=True
    - Normalizes trailing slash in path
    """
    try:
        p = urllib.parse.urlparse(url)
        netloc = p.netloc.lower()
        path = p.path.rstrip("/") or "/"
        known_domains = ("airbnb.", "roompot.", "landal.", "hometogo.", "naartexel.nl")
        force_drop_query = any(netloc.endswith(d.strip(".")) or netloc.startswith(d) for d in known_domains)
        if force_drop_query or ignore_query:
            query = ""
        else:
            # keep query minus common tracking params
            qs = urllib.parse.parse_qsl(p.query, keep_blank_values=False)
            drop_keys = {"utm_source","utm_medium","utm_campaign","utm_content","utm_term","gclid","fbclid",
                         "source_impression_id","federated_search_id","previous_page_section_name"}
            qs = [(k,v) for k,v in qs if k not in drop_keys and not k.startswith("utm_")]
            query = urllib.parse.urlencode(qs)
        return urllib.parse.urlunparse((p.scheme, netloc, path, "", query, ""))
    except Exception:
        return url

def dedupe_places_list(places: list[dict], ignore_query: bool = True, coord_round: int | None = None) -> list[dict]:
    """Dedupe places by normalized URL, then optionally by (rounded lat, lon, title).
    Later entries take precedence (so imports can override base).
    """
    by_url: dict[tuple, dict] = {}
    for it in places:
        try:
            nurl = normalize_url(it["url"], ignore_query=ignore_query)
        except Exception:
            nurl = it.get("url", "")
        by_url[("url", nurl)] = it

    out = list(by_url.values())
    if coord_round is not None:
        seen = set()
        result = []
        for it in out:
            key = (round(it["lat"], coord_round), round(it["lon"], coord_round), it["title"].strip().lower())
            if key in seen:
                continue
            seen.add(key)
            result.append(it)
        return result
    return out

# Optional: domains you allow to be embedded inside the popup via <iframe>
IFRAME_ALLOWLIST = {
    "naartexel.nl",
    # add your own domains here if they allow iframes
}

def save_place_jsonl(item: dict, target_dir: pathlib.Path, filename_prefix="import"):
    """
    Append a single validated item to a JSONL file in target_dir.
    Returns the path written.
    """
    ts = datetime.utcnow().strftime("%Y%m%d")
    target = target_dir / f"{filename_prefix}-{ts}.jsonl"
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return target


def is_duplicate(item: dict, existing: list, key: str):
    val = item.get(key)
    if not val:
        return False
    return any(val == e.get(key) for e in existing)


def load_places(only_base: bool = False) -> list:
    """Load base places plus any imported JSONL records. Deduplicate by URL."""
    base = []
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            for i, it in enumerate(data, 1):
                try:
                    base.append(validate_item(it, f"places.json:{i}"))
                except Exception:
                    # Keep base permissive: if base has slight issues, try to include raw
                    # but skip hard failures
                    pass
    except FileNotFoundError:
        pass

    # Load any JSONL files in imports (when enabled)
    imported = []
    if ENABLE_IMPORTS and not only_base:
        for path in sorted(PLACES_DIR.glob("*.jsonl")):
            try:
                with path.open("r", encoding="utf-8") as f:
                    for ln, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            itm = json.loads(line)
                            imported.append(validate_item(itm, f"{path.name}:{ln}"))
                        except Exception:
                            # ignore invalid lines but continue
                            continue
            except Exception:
                continue

    # Deduplicate by URL (prefer later entries so imports can override)
    combined = {}
    for it in base + imported:
        combined[it["url"]] = it
    return list(combined.values())


# Provide a manual reload trigger and a data source toggle
col_top_l, col_top_r = st.columns([1, 1])
with col_top_l:
    st.subheader("➕ Import places")
with col_top_r:
    if st.button("Reload data", use_container_width=True):
        # Force a rerun to pick up any new files
        st.rerun()

# Importer UI
col1, col2 = st.columns(2)

with col1:
    with st.expander("Add a single place"):
        with st.form("add_single_place", clear_on_submit=False):
            title = st.text_input("Title *", placeholder="e.g., Airbnb — Den Burg (Noord-Holland)")
            url = st.text_input("URL *", placeholder="https://…")
            lat = st.number_input("Latitude *", format="%.6f")
            lon = st.number_input("Longitude *", format="%.6f")
            price = st.text_input("Price", placeholder="e.g., 527€")
            note = st.text_input("Note", placeholder="Optional short note")
            dedup_key = st.selectbox("Deduplicate by", ["url", "title"], index=0)
            submitted = st.form_submit_button("Add place")

            if submitted:
                new_item = {
                    "title": title.strip(),
                    "url": url.strip(),
                    "lat": float(lat),
                    "lon": float(lon),
                }
                if price.strip():
                    new_item["price"] = price.strip()
                if note.strip():
                    new_item["note"] = note.strip()
                try:
                    # Use currently loaded places for dedupe
                    current = load_places()
                    clean = validate_item(new_item, "form")
                    if is_duplicate(clean, current, dedup_key):
                        st.warning(f"Skipped: duplicate {dedup_key} already exists.")
                    else:
                        p = save_place_jsonl(clean, PLACES_DIR, filename_prefix="manual")
                        st.success(f"Added ✓ (saved to {p.name}). Click ‘Reload data’ to see it.")
                except Exception as e:
                    st.error(f"Could not add place: {e}")

with col2:
    with st.expander("Bulk import (JSON / JSONL / CSV)"):
        uploader = st.file_uploader(
            "Upload one or more files",
            type=["json", "jsonl", "ndjson", "csv"],
            accept_multiple_files=True
        )
        dedup_key_bulk = st.selectbox("Deduplicate by", ["url", "title"], index=0, key="dedup_bulk")
        if uploader:
            added, skipped, errors = 0, 0, 0
            out_path = None
            for f in uploader:
                try:
                    name = f.name.lower()
                    if name.endswith(".json"):
                        data = json.load(f)
                        if isinstance(data, dict):
                            data = [data]
                    elif name.endswith((".jsonl", ".ndjson")):
                        data = []
                        for i, line in enumerate(f, 1):
                            line = line.decode("utf-8").strip()
                            if not line:
                                continue
                            try:
                                data.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                errors += 1
                                st.error(f"{f.name} line {i}: {e}")
                    elif name.endswith(".csv"):
                        import io, csv as _csv
                        text = f.read().decode("utf-8")
                        reader = _csv.DictReader(io.StringIO(text))
                        data = []
                        for i, row in enumerate(reader, 2):
                            try:
                                row["lat"] = float(row["lat"])
                                row["lon"] = float(row["lon"])
                            except Exception:
                                errors += 1
                                st.error(f"{f.name} line {i}: invalid lat/lon")
                                continue
                            data.append({k: v for k, v in row.items() if v != ""})
                    else:
                        st.error(f"Unsupported file type: {f.name}")
                        continue

                    current = load_places()
                    for idx, item in enumerate(data, 1):
                        try:
                            clean = validate_item(item, f"{f.name}:{idx}")
                            if is_duplicate(clean, current, dedup_key_bulk):
                                skipped += 1
                                continue
                            out_path = save_place_jsonl(clean, PLACES_DIR, filename_prefix="bulk")
                            added += 1
                            current.append(clean)  # keep in-memory dedupe tight for this batch
                        except Exception as e:
                            errors += 1
                            st.error(f"{f.name} item {idx}: {e}")

                except Exception as e:
                    errors += 1
                    st.error(f"Failed to read {f.name}: {e}")

            if added or skipped or errors:
                msg = f"Imported — added: **{added}**, duplicates skipped: **{skipped}**, errors: **{errors}**."
                if out_path:
                    msg += f" Saved to **{out_path.name}**."
                st.info(msg)
                st.caption("Click ‘Reload data’ to refresh the map.")

# Sidebar: data source toggle and dedupe controls
st.sidebar.header("Data")
only_base_checkbox = st.sidebar.checkbox("Use only places.json (ignore PVC imports)", value=False)
ignore_query_checkbox = st.sidebar.checkbox("Deduplicate ignoring URL query parameters", value=True)
coord_rounding = st.sidebar.selectbox("Group duplicates by coord rounding", ["Off", 5, 6], index=0, help="Rounds lat/lon to group near-identical points.")
coord_round_val = None if coord_rounding == "Off" else int(coord_rounding)

# Now load places for the map (respect toggle) and dedupe further
PLACES = load_places(only_base=only_base_checkbox)
PLACES = dedupe_places_list(PLACES, ignore_query=ignore_query_checkbox, coord_round=coord_round_val)

# Surface a small diagnostic if there are exact duplicate coordinates in current data
_coord_counts = {}
for _p in PLACES:
    _key = (_p["lat"], _p["lon"]) 
    _coord_counts[_key] = _coord_counts.get(_key, 0) + 1
_dup_coords = [k for k, v in _coord_counts.items() if v > 1]
if _dup_coords:
    st.info(f"Note: {len(_dup_coords)} coordinate(s) have multiple places; these are combined into one marker on the map.")

# Diagnostics and PVC tools
with st.expander("Data diagnostics and PVC tools"):
    # Show import dir and files
    st.caption(f"Imports directory: {PLACES_DIR}")
    try:
        files = sorted([p.name for p in PLACES_DIR.glob("*.jsonl")])
    except Exception:
        files = []
    st.write({"jsonl_files": files, "count": len(files)})

    # Count base and imported raw entries (rough estimate)
    base_count = 0
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
            base_count = len(data) if isinstance(data, list) else 1
    except Exception:
        pass
    st.write({"base_places_json": base_count, "after_dedupe_shown": len(PLACES)})

    # Option to purge imports
    purge = st.checkbox("Confirm: delete all *.jsonl in imports directory")
    if st.button("Purge PVC imports"):
        if not purge:
            st.warning("Tick the confirmation checkbox to purge imports.")
        else:
            removed = 0
            for pth in PLACES_DIR.glob("*.jsonl"):
                try:
                    pth.unlink(missing_ok=True)
                    removed += 1
                except Exception as e:
                    st.error(f"Failed to delete {pth.name}: {e}")
            st.success(f"Removed {removed} import file(s). Click ‘Reload data’.")

# Sidebar: quick links
st.sidebar.header("Links")
for idx, p in enumerate(PLACES, start=1):
    price = p.get('price', '—')
    st.sidebar.markdown(f"{idx}. [{p['title']}]({p['url']}) — {price}")

# Compute a reasonable map center (Netherlands-ish)
if PLACES:
    avg_lat = sum(p["lat"] for p in PLACES) / len(PLACES)
    avg_lon = sum(p["lon"] for p in PLACES) / len(PLACES)
else:
    # Default coordinates roughly Netherlands if no data
    avg_lat, avg_lon = 52.1326, 5.2913

m = folium.Map(location=[avg_lat, avg_lon], zoom_start=7, control_scale=True, tiles="OpenStreetMap")

cluster = MarkerCluster().add_to(m)

# Group exact-duplicate coordinates so only one pin is shown per identical (lat, lon)
groups = {}
for it in PLACES:
    key = (it["lat"], it["lon"])  # exact duplicates only
    groups.setdefault(key, []).append(it)

for (lat, lon), items in groups.items():
    # If single item at this coordinate, render the rich preview popup
    if len(items) == 1:
        p = items[0]
        price_txt = p.get("price", "—")
        preview = screenshot_preview_url(p["url"])  # may be None

        if preview:
            preview_img_html = (
                f"<img src='{preview}' "
                "style='width:100%;border-radius:8px;border:1px solid #e3e3e3;margin-bottom:6px;' "
                "loading='lazy' onerror=\"this.style.display='none'\">"
            )
        else:
            preview_img_html = ""

        popup_html = f"""
        <div style='min-width:260px;max-width:340px'>
          <div style="font-weight:700;margin-bottom:6px;">{p['title']}</div>
          <div style="font-size:12px;opacity:0.85;margin-bottom:6px;"><b>Price:</b> {price_txt}</div>
          {preview_img_html}
          <em>{p.get('note','')}</em><br/>
          <div style="margin-top:6px;">
            <a href="{p['url']}" target="_blank" rel="noopener">Open listing ↗</a>
          </div>
        </div>
        """

        # Use a CSS-based marker to avoid missing PNG icon assets
        marker_html = (
            "<div style=\"background:#2563eb;color:#fff;border-radius:50%;width:28px;height:28px;"
            "display:flex;align-items:center;justify-content:center;border:2px solid #fff;"
            "box-shadow:0 0 0 1px rgba(0,0,0,0.25);font-weight:700;\">"
            "•"  # simple dot for single
            "</div>"
        )
        folium.Marker(
            location=[lat, lon],
            tooltip=p["title"],
            popup=folium.Popup(popup_html, max_width=360),
            icon=folium.DivIcon(html=marker_html)
        ).add_to(cluster)
    else:
        # Multiple items share this exact coordinate: combine into one popup list
        items_sorted = sorted(items, key=lambda x: x.get("price", ""))
        list_html = "".join(
            [
                (
                    f"<li style='margin-bottom:6px;'>"
                    f"<div style='font-weight:600'>{it['title']}</div>"
                    f"<div style='font-size:12px;opacity:0.85;margin:2px 0;'><b>Price:</b> {it.get('price','—')}</div>"
                    f"<em style='font-size:12px;'>{it.get('note','')}</em><br/>"
                    f"<a href='{it['url']}' target='_blank' rel='noopener'>Open listing ↗</a>"
                    f"</li>"
                )
                for it in items_sorted
            ]
        )
        popup_html = f"""
        <div style='min-width:260px;max-width:360px'>
          <div style="font-weight:700;margin-bottom:8px;">{len(items)} places at this location</div>
          <ul style='padding-left:18px;margin:0;'>
            {list_html}
          </ul>
        </div>
        """
        # Marker with count badge
        count = len(items)
        marker_html = (
            f"<div style=\"background:#0f766e;color:#fff;border-radius:50%;width:30px;height:30px;"
            "display:flex;align-items:center;justify-content:center;border:2px solid #fff;"
            "box-shadow:0 0 0 1px rgba(0,0,0,0.25);font-weight:700;\">"
            f"{count}"
            "</div>"
        )
        folium.Marker(
            location=[lat, lon],
            tooltip=f"{count} places here",
            popup=folium.Popup(popup_html, max_width=380),
            icon=folium.DivIcon(html=marker_html)
        ).add_to(cluster)

st_data = st_folium(m, width=None, height=600)
st.caption("Tip: Ctrl/Cmd + click on a popup link to force a new tab.")