# Main.py by Crystal J. Hollis | crystaljhollis@gmail.com
# GitHub: https://github.com/crystaljhollis
# 08/2025
# Developed using Python 3.13.7
# 

# =======================================================================================================================================
#                                                   LIBRARIES
# =======================================================================================================================================

# Import Python Standard Libraries
import re                                                                       #regular expressions aka regex
from pathlib import Path                                                        #file system paths
from typing import List, Tuple, Set                                             #gradual typing support

# Import gradio
import gradio as gr                                                             # Documentation: https://www.gradio.app/

# =======================================================================================================================================
#                                                   FUNCTIONS
# =======================================================================================================================================

# HELPER FUNCTIONS
_SLUG_OK = re.compile(r"[^a-z0-9_]+")

def slugify(text: str) -> str:
    """lowercase, spaces->underscore, drop junk"""
    s = text.strip().lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^\w\s-]", "", s)          # keep letters/numbers/underscore/hyphen/space
    s = re.sub(r"\s+", "_", s)              # collapse spaces to _
    s = _SLUG_OK.sub("_", s)                # anything else -> _
    s = re.sub(r"_+", "_", s).strip("_")    # collapse repeats
    return s

def suggest_slugs(locked_people: List[str], locked_locs: List[str], rough_terms: List[str]) -> List[str]:
    """
    Very simple slug ideas using location + common event words.
    Swap this for an LLM later if you want.
    """
    loc = locked_locs[0] if locked_locs else ""
    base = slugify(loc) if loc else "gallery_item"

    # pick a few common event-ish tags if present
    vocab = ["opening ceremony", "ribbon cutting", "audience", "ceremony", "speeches", "panel", "performance"]
    hits = [v for v in vocab if any(v in t.lower() for t in rough_terms)]

    slugs = [f"{base}_{slugify(h)}" for h in hits[:3]] or [base]
    # add a couple safe fallbacks
    return list(dict.fromkeys(slugs + [f"{base}_event", f"{base}_scene"]))
    
def suggest_headline_title(locked_locs: List[str], rough_terms: List[str]) -> Tuple[str, str]:
    """
    Headline = longer, Title = shorter. Heuristics only.
    """
    loc = locked_locs[0] if locked_locs else "Campus"
    if any("ribbon" in t.lower() and "cut" in t.lower() for t in rough_terms):
        headline = f"{loc} Opening Ceremony and Ribbon Cutting at SMU"
        title = f"{loc} Opening Ceremony"
    else:
        headline = f"Event at {loc}, Southern Methodist University"
        title = f"{loc} Event"
    return headline, title

def suggest_description(locked_locs: List[str], rough_terms: List[str]) -> str:
    """
    Template now; replace with Gemma call later.
    """
    loc = locked_locs[0] if locked_locs else "campus venue"
    phrases = [t for t in rough_terms if len(t.split()) <= 4][:6]
    core = ", ".join(phrases) if phrases else "program footage, speeches, audience"
    return (
        f"Program footage from the {loc} event at Southern Methodist University, featuring {core} "
        f"in Dallas, Texas."
    )

def people_variants_stub(people_list: List[str]) -> str:
    """
    Placeholder until Gemma is wired. Produces generic roles.
    """
    if not people_list:
        return ""
    base = []
    # naive role guessers
    hints = ["president", "dean", "trustee", "donor", "student", "faculty"]
    base.extend({h for h in hints})
    return ", ".join(sorted(set(base)))


# SPLIT TERMS FUNCTION == accepts text and returns a cleaned list
def _split_terms(text: str) -> List[str]:
    """
    Accepts comma/newline/semicolon separated text and returns a cleaned list.
    - trims spaces
    - collapses internal whitespace
    - removes surrounding quotes
    - keeps hyphens and apostrophes (useful for names/places)
    """
    if not text:
        return []                                                               # Empty text returns empty list
    parts = re.split(r"[,\n;]+", text)                                          # regex split on commas, semicolons, or newlines
    cleaned = []                                                                # Prepare list to hold cleaned-up terms
    for p in parts:                                                             # Iterates through each text piece
        t = p.strip().strip('"').strip("'")                                     # removes trailing spaces, double/single quotes
        # collapse extra internal spaces            
        t = re.sub(r"\s+", " ", t)                                              # regex sub whitespace w/single space (\s+)
        if t:
            cleaned.append(t)                                                   # If t is not empty, append to the cleaned list
    return cleaned                                                              # Returns the cleaned list



# LOAD MASTER KEYWORDS FUNCTION == user uploads txt file
def _load_master_keywords(file_obj) -> Set[str]:                                # Accepts .txt, returns lowercase keywords
    """
    Load hierarchical SMU keyword file.
    - Keeps each line as its own entry
    - Ignores bracketed category headers like [Academic Life]
    - Strips tabs/spaces

    """
    if not file_obj:
        return set()
    
    if isinstance(file_obj, bytes):
        content = file_obj.decode("utf-8", errors="ignore")                     # Decode file_obj into string with UTF-8 encoding, ignore weird characters
    else:
        content = str(file_obj) #force to string
    keywords = set()
    for line in content.splitlines():                                           # Iterates line by line 
        line = line.strip()
        if not line:
            continue                                                            # Ignores blank lines
        # skip category headers in [brackets]
        if line.startswith("[") and line.endswith("]"):
            continue                                                            # Ignores [Category] headers
        keywords.add(line.lower())                                              # Preserve keywords, matching lowercase
    return keywords                                                             # Returns the cleaned set of keywords


# COMMA+SPACE FUNCTION == simply adds comma and space for each keyword
def _to_csv_line(items: List[str]) -> str:                                      # Adds comma and space to cleaned list
    """
    Make a comma+space separated line
    for copy-paste.
    """
    return ", ".join(items)                                                     # Concatenates all elements separated by ", "

  
# KEYWORD CHECKER FUNCTION
def keyword_checker(                                                            # Takes arguments:
    job_number: str,                                                            # Job Number i.e. 26-999
    neg_number: str,                                                            # Neg Number
    rough_keywords: str,                                                        # Rough draft keywords
    people_locked: str,                                                         # Names of Persons Shown
    locations_locked: str,                                                      # Names of Locations
    names_locked: str,                                                          # Other locked terms
    master_txt                                                                  # Latest keyword txt file
):
    # [1] Parse inputs; Converts raw text into a list, calling _split_terms
    rough_list = _split_terms(rough_keywords)                    
    people_list = _split_terms(people_locked)
    locations_list = _split_terms(locations_locked)
    names_list = _split_terms(names_locked)

    # [2] Build locked sets (lowercase for matching)
    locked_map = {                                                              # Dictionary
        "PEOPLE": set(p.lower() for p in people_list),                          # lowercase so matching is case-insensitive
        "LOCATIONS": set(l.lower() for l in locations_list),
        "LOCKED": set(a.lower() for a in names_list),
    }
    locked_all = set().union(*locked_map.values())                              # Combines everything in the dictionary, keeping only unique elements

    # [3] Load master keyword list
    master_set = _load_master_keywords(master_txt) if master_txt else set()     # Load keyword txt if provided, else empty set

    # [4] Categorize
    locked_hits = {"PEOPLE": [], "LOCATIONS": [], "LOCKED": []}        # locked terms separated by category
    in_master = []                                                              # from keyword txt file
    new_terms = []                                                              # not in keyword txt file

    for kw in rough_list:
        k = kw.lower()                                                          # loop through each keywords, make it lowercase
        # Check locked first (so they can be handled specially later)
        hit_locked = False                                                      # checked if keyword is in a locked category
        for cat, s in locked_map.items():
            if k in s:
                locked_hits[cat].append(kw)                                     # If yes, add to locked_hits
                hit_locked = True
                break
        if hit_locked:                                                          # locked terms don't need to be checked against keyword txt file
            continue

        # Then check against master
        if master_set:                                                          # check if in the keyword txt file
            if k in master_set:
                in_master.append(kw)                                            # If yes, in_master
            else:
                new_terms.append(kw)                                            # If no, new_terms
        else:
            # No master list provided
            in_master.append(kw)                                                # If no keyword txt file, treat all non-locked terms as in_master

    # [5] Build human-readable outputs
    locked_block = {
        "PEOPLE": _to_csv_line(locked_hits["PEOPLE"]),
        "LOCATIONS": _to_csv_line(locked_hits["LOCATIONS"]),
        "LOCKED": _to_csv_line(locked_hits["LOCKED"]),
    }
    in_list_block = _to_csv_line(in_master)
    new_block = _to_csv_line(new_terms)
    combined_csv = _to_csv_line(locked_hits["PEOPLE"] + locked_hits["LOCATIONS"] + locked_hits["LOCKED"] + in_master + new_terms) # Combined summary output

    # [6] LLM customizable fields
    slugs = suggest_slugs(locked_hits["PEOPLE"], locked_hits["LOCATIONS"], rough_list)
    headline, title = suggest_headline_title(locked_hits["LOCATIONS"], rough_list)
    description = suggest_description(locked_hits["LOCATIONS"], rough_list)
    people_variants = people_variants_stub(locked_hits["PEOPLE"])  # replace w/ Gemma later

    # [7] Summary line
    summary = (
        f"Job {job_number or '(none)'} | "                                      # Job Number
        f"Catalog {neg_number or '(none)'} | "                                  # Neg Number
        f"Total input: {len(rough_list)} | "                                    # Total Keywords Checked
        f"Locked: {sum(len(v) for v in locked_hits.values())} | "               # Total Locked Hits Category
        f"In List: {len(in_master)} | "                                         # Total from keyword txt file
        f"New: {len(new_terms)}"                                                # Total new keywords
    )

    # [8] Return in same order as UI outputs
    return (
        job_number,                     # Job Number (echo)
        neg_number,                     # Neg Number (echo)
        "\n".join(slugs),               # Recommended filename slugs
        headline,                       # Headline
        title,                          # Title
        description,                    # Description / Alt Text
        locked_block["PEOPLE"],         # PEOPLE (Persons Shown)
        people_variants,                # PEOPLE VARIANTS (suggested / LLM)
        locked_block["LOCATIONS"],      # LOCKED: LOCATIONS
        locked_block["LOCKED"],         # LOCKED: OTHER
        in_list_block,                  # BATCH + SEO
        new_block,                      # OPTIONAL + SEO
        combined_csv,                   # All Combined CSV
        "",                             # Credit Line Field (optional inputs)
        "",                             # Creator Field (optional inputs)
        summary,                        # (optional) Summary – nice to have last
    )

# =======================================================================================================================================
#                                                   GRADIO GUI CONFIG
# =======================================================================================================================================

# Theme Object
custom = gr.themes.Base(
    primary_hue="red",                                                          # Red main accent color family
    neutral_hue="zinc",                                                         # Neutral palette
).set(                                                                          # Override CSS
    # Page text
    body_text_color="#1c1c1c",                                                # black text
    body_text_color_subdued="#666666",                                        # subdued text dark gray
    body_text_size="14px",                                                      # Font size
    body_text_weight="400",                                                     # regular weight font

    # Page & blocks
    background_fill_primary="#ffffff",                                        # white cards
    background_fill_secondary="#ffffff",                                      # dark mode, white cards
    block_background_fill="#eeeeee",                                          # light gray background
    block_border_color="#d6d6d6",                                             # light gray border
    block_title_text_color="#1c1c1c",                                         # black text block titles

    # Inputs/buttons
    input_background_fill="#ffffff",                                          # white input boxes
    input_border_color="#d6d6d6",                                             # light gray border

    button_primary_background_fill="#ce191c",                                 # red primary buttons
    button_primary_background_fill_hover="#7b2325",                           # dark red on hover
    button_primary_text_color="#ffffff",                                      # white text on red button

    button_secondary_background_fill="#343434",                               # dark mode, very dark gray
    button_secondary_background_fill_hover="#2b2b2b",                         # dark mode, darker gray on hover
    button_secondary_text_color="#ffffff",                                    # dark mode, white text

    # Links + radius/shadow
    link_text_color="#1c1c1c",                                                # link text is black
    embed_radius="8px",                                                         # all cards/blocks have slightly rounded corners
    border_color_accent="#d6d6d6",                                            # light gray accent borders
    shadow_drop="0 4px 16px rgba(0,0,0,0.08)",                                  # subtle shadow effect around cards
)

CSS = '''

/* ====== Palette - unused at the moment, save for later ====== */
:root{
  --smu-dark-gray: #666666;
  --smu-very-dark: #343434;
  --smu-light-gray: #d6d6d6;
  --smu-off-white: #eeeeee;
  --smu-white: #ffffff;
  --smu-black: #1c1c1c;
  --smu-red: #8e2a2c;
  --smu-salmon: #ff756d;   /* reserved for "suggested keywords" – not used yet */
}

/* ====== Hard-lock app to light mode ====== */
html, :root, body, .gradio-container{
  color-scheme: light !important;         /* browsers render controls as light */
  background: var(--smu-off-white) !important;  /* page background */
  color: var(--smu-black) !important;
}

/* ====== Global text ====== */
h1, h2, h3, label, p, .gr-markdown *{
  color: var(--smu-black) !important;
}

/* ====== Panels / cards ====== */
.gr-block{
  background: var(--smu-white) !important;
  border: 1px solid var(--smu-light-gray) !important;
  border-radius: 8px !important;
}

/* ====== Tabs / top bars (FileMaker-ish chrome) ====== */
.gr-tabs, .gr-panel{ background: var(--smu-dark-gray) !important; }
.gr-tabs *, .gr-panel *{ color: var(--smu-white) !important; }

/* ====== Inputs ====== */
.gradio-container input[type="text"],
.gradio-container textarea{
  background: var(--smu-white) !important;
  color: var(--smu-black) !important;
  border-color: var(--smu-light-gray) !important;
}
.gradio-container input[type="text"]::placeholder,
.gradio-container textarea::placeholder{
  color: var(--smu-dark-gray) !important;
  opacity: 1 !important;
}

/* ====== Buttons ====== */
button.gr-button-primary{
  background: var(--smu-red) !important; color: #fff !important;
}
button.gr-button-primary:hover{ filter: brightness(.92); }
button.gr-button-secondary{
  background: var(--smu-very-dark) !important; color: #fff !important;
}
button.gr-button-secondary:hover{ filter: brightness(1.05); }

/* ====== Copy blocks (make borders more visible) ====== */
/* Add elem_classes=["copyblock"] to those Textboxes you want highlighted */
.copyblock textarea{
  border: 2px solid var(--smu-dark-gray) !important;
  box-shadow: inset 0 1px 0 rgba(0,0,0,.03);
}

/* ====== Upload zones / dividers ====== */
#upload_panel, #upload_group{ background: var(--smu-white) !important; border-radius: 8px; }
input[type="file"], .gr-file{ border-color: var(--smu-light-gray) !important; }
hr{ border-color: var(--smu-light-gray) !important; }

/* ====== Reserved style for future "suggested keywords" (not applied yet) ====== */
/* Later you can add elem_classes=["suggested"] to a Textbox or container */
.suggested textarea, .suggested{
  /* NOT enabled yet; uncomment when wiring the feature:
  background: #ff756d1a !important;        /* subtle salmon tint */
  border-color: var(--smu-salmon) !important;
  */
}
'''

# =======================================================================================================================================
#                                                   GRADIO APP
# =======================================================================================================================================


with gr.Blocks(title="Job Sheet Keyword and Metadata SEO", theme=custom) as demo:                       # css=CSS is not being used at the moment! # gr.Blocks is a container laying out multiple UI elements
    gr.Markdown(                                                                                        # gr.Markdown block to explain to the user what the app does
        "# Job Sheet Keyword and Metadata SEO \n"
        "Paste rough draft keywords, add optional **locked terms** (PEOPLE / LOCATIONS / NAMES), "
        "and upload the **latest keyword file** (.txt)."
    )

    with gr.Row():                                                                                                              # gr.Row horizontal components
        job_number = gr.Textbox(label="Job Number", placeholder="i.e. 26-999", scale=1)                          # Job Number Textbox
        neg_number = gr.Textbox(label="Catalog / Neg Number", placeholder="i.e. 12345D", scale=1)                      # Neg Number Textbox
    rough = gr.Textbox(                                                                                                         # Rough Draft Keywords Textbox
        label="Rough Draft Keywords (comma / newline / semicolon separated)",
        lines=6,
        placeholder="i.e. Owen Arts Center, Meadows School of the Arts, SMU, opening ceremony, ribbon cutting, Dallas, Texas"
    )

    with gr.Accordion("Locked Terms (will not generate SEO suggestions / synonyms)", open=False, elem_id="locked_panel"):                                                             # Dropdown Section Locked Terms
        with gr.Row():
            people = gr.Textbox(label="PEOPLE (Persons Shown)", lines=4, placeholder="i.e. R. Gerald Turner, Samuel S. Holland")                                            # Persons Shown Textbox
            locations = gr.Textbox(label="SUBLOCATION or ADDRESS / CITY / STATE / COUNTRY", lines=4, placeholder="i.e. Owen Arts Center, Dallas, Texas, United States")     # Locations Textbox
            names = gr.Textbox(label="OTHER LOCKED TERMS", lines=4, placeholder="i.e. Meadows School of the Arts, Lyle School of Engineering")                              # Locked Terms Textbox

    with gr.Row():
        credit_in = gr.Textbox(label="Credit Line (optional input)", placeholder="Southern Methodist University / John Doe", scale=1)
        creator_in = gr.Textbox(label="Creator (optional input)", placeholder="John Doe", scale=1)

    master = gr.File(label="Upload the latest keyword list (.txt Keyword file; newline or comma separated)",                    # Upload dialog
                     file_types=[".txt"], elem_id="upload_panel")

    run = gr.Button("Run Keyword Optimizer", variant="primary")                                                                 # Run Red Button
    
    # ---- OUTPUTS (order must match function returns) ----
    job_out        = gr.Textbox(label="Job Number", interactive=False, lines=1, elem_classes=["copyblock"])
    neg_out        = gr.Textbox(label="Neg Number (Job Identifier Field)", interactive=False, lines=1, elem_classes=["copyblock"])
    slugs_out      = gr.Textbox(label="Recommended filename slugs (suggested)", interactive=False, lines=4, elem_classes=["copyblock"])
    headline_out   = gr.Textbox(label="Headline", interactive=False, lines=2, elem_classes=["copyblock"])
    title_out      = gr.Textbox(label="Title", interactive=False, lines=2, elem_classes=["copyblock"])
    desc_out       = gr.Textbox(label="Description / Alt Text", interactive=False, lines=4, elem_classes=["copyblock"])

    people_out     = gr.Textbox(label="PEOPLE (Persons Shown Field)", interactive=False, lines=3, elem_classes=["copyblock"])
    peoplevar_out  = gr.Textbox(label="PEOPLE VARIANTS (suggested)", interactive=False, lines=2, elem_classes=["copyblock"])

    loc_out        = gr.Textbox(label="LOCKED: LOCATIONS (copy block)", interactive=False, lines=2, elem_classes=["copyblock"])
    locked_out     = gr.Textbox(label="LOCKED TERMS (no synonyms)", interactive=False, lines=2, elem_classes=["copyblock"])

    in_list_out    = gr.Textbox(label="BATCH + SEO (suggested)", interactive=False, lines=4, elem_classes=["copyblock"])
    new_out        = gr.Textbox(label="OPTIONAL + SEO (new)", interactive=False, lines=4, elem_classes=["copyblock"])
    csv_out        = gr.Textbox(label="All Combined (CSV)", interactive=False, lines=3, elem_classes=["copyblock"])

    credit_out     = gr.Textbox(label="Credit Line Field", interactive=False, lines=1, elem_classes=["copyblock"])
    creator_out    = gr.Textbox(label="Creator Field", interactive=False, lines=1, elem_classes=["copyblock"])

    summary_out    = gr.Textbox(label="Summary (debug)", interactive=False, lines=2)

    # Click wiring – note input list includes credit/creator, pass them into function if you want to use them
    run.click(
        fn=keyword_checker,
        inputs=[job_number, neg_number, rough, people, locations, names, master],
        outputs=[job_out, neg_out, slugs_out, headline_out, title_out, desc_out,
                 people_out, peoplevar_out, loc_out, locked_out,
                 in_list_out, new_out, csv_out, credit_out, creator_out, summary_out]
    )


#demo.launch(share=True) # launches the app, switch to false to turn off sharing

if __name__ == "__main__":
    demo.launch()  # local runs only
