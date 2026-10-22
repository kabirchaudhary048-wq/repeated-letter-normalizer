
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from symspellpy import Verbosity

BACKEND_PATH = Path(__file__).resolve().parent.parent / "working_model"
sys.path.insert(0, str(BACKEND_PATH))

from automation import RepeatedLetterDFA
from normalizer import normalize_word
from symspell_corrector import create_symspell


st.set_page_config(
    page_title="Repeated Letter Normalizer",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding: 1.5rem clamp(0.8rem, 3vw, 2.5rem);
    }

    h1 { font-size: clamp(1.7rem, 4vw, 2.7rem); }
    h2 { font-size: clamp(1.25rem, 3vw, 1.8rem); }

    .state-card {
        border: 1px solid var(--secondary-background-color);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 8px;
    }

    .muted { color: var(--text-color); opacity: 0.75; }

    div.stButton > button {
        width: 100%;
        min-height: 44px;
        border-radius: 9px;
    }

    [data-testid="stDataFrame"] {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_resources():
    return create_symspell(), RepeatedLetterDFA()


try:
    sym_spell, detector = load_resources()
except Exception as exc:
    st.error(f"Could not load the backend: {exc}")
    st.stop()


def fallback_normalize(token, sym_spell):
    """Reduce runs of 3+ letters to two, then try dictionary correction."""
    candidate = re.sub(r"([a-z])\1{2,}", r"\1\1", token.lower())

    suggestions = sym_spell.lookup(
        candidate,
        Verbosity.CLOSEST,
        max_edit_distance=2,
    )

    if suggestions:
        return suggestions[0].term

    return candidate


def normalize_token(token, sym_spell):
    lower = token.lower()

    # Keep ordinary words such as hello and letter unchanged.
    if not re.search(r"([a-z])\1{2,}", lower):
        return token

    try:
        result = normalize_word(lower, sym_spell)
    except Exception:
        result = None

    if not result or result.lower() == lower:
        result = fallback_normalize(lower, sym_spell)

    if token.isupper():
        return result.upper()

    if token.istitle():
        return result.capitalize()

    return result


def normalize_sentence(text, sym_spell):
    # Preserve spaces, punctuation, and non-English characters.
    pieces = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[^A-Za-z]+", text)
    output = []

    for piece in pieces:
        if re.fullmatch(r"[A-Za-z]+(?:'[A-Za-z]+)?", piece):
            output.append(normalize_token(piece, sym_spell))
        else:
            output.append(piece)

    return "".join(output)


def trace_word(word):
    """Trace adjacent repeated letters through q0, qa-qz, and qF."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    rows = []
    previous = None
    state = "q0"
    found = False

    for index, char in enumerate(word, start=1):
        lower = char.lower()

        if lower not in alphabet:
            rows.append({
                "Step": index,
                "Input": char,
                "State before": state,
                "Transition": "Non-letter / reset",
                "State after": "q0",
            })
            previous = None
            state = "q0"
            continue

        before = state

        if previous == lower:
            state = "qF"
            found = True
            transition = f"Same adjacent letter '{lower}'"
        else:
            state = "q" + lower
            transition = f"Remember '{lower}'"

        rows.append({
            "Step": index,
            "Input": char,
            "State before": before,
            "Transition": transition,
            "State after": state,
        })

        previous = lower

    return rows, found


def show_state_grid():
    st.markdown("### All 28 states")
    st.caption(
        "q0 = start, qa–qz = remember the previous letter, "
        "qF = repeated adjacent letter detected."
    )

    states = ["q0"] + [f"q{letter}" for letter in "abcdefghijklmnopqrstuvwxyz"] + ["qF"]

    # Responsive Streamlit columns; fewer columns on narrow screens.
    width = st.slider(
        "States per row",
        min_value=2,
        max_value=7,
        value=4,
        help="Reduce this number for a narrower screen.",
    )

    for start in range(0, len(states), width):
        group = states[start:start + width]
        columns = st.columns(width)

        for col, state in zip(columns, group):
            if state == "qF":
                description = "Accepting"
            elif state == "q0":
                description = "Start"
            else:
                description = f"Stores '{state[-1]}'"

            with col:
                st.markdown(
                    f'<div class="state-card">'
                    f'<strong>{state}</strong><br>'
                    f'<span class="muted">{description}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


st.title("🔤 Repeated Letter Normalizer")
st.write(
    "Detect exaggerated repeated letters and normalize words "
    "while preserving punctuation and spacing."
)

with st.container(border=True):
    st.subheader("Try it")

    text = st.text_area(
        "Enter a sentence",
        value="Helloooo brooo, yessss this is sooo coool!",
        height=120,
        placeholder="Type a sentence here...",
        label_visibility="visible",
    )

    run = st.button("Normalize text", type="primary", use_container_width=True)

if run:
    normalized = normalize_sentence(text, sym_spell)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Original")
        st.write(text or "*(empty)*")

    with right:
        st.markdown("#### Normalized")
        st.write(normalized or "*(empty)*")

    if normalized == text:
        st.info("No changes were made.")
    else:
        st.success("Normalization complete.")

st.divider()

with st.expander("Automaton: 28-state model", expanded=False):
    st.markdown("""
    **Transition rules**

    - From `q0`, reading a letter `a` moves to `qa`.
    - From `qx`, reading the same letter `x` moves to `qF`.
    - From `qx`, reading a different letter `y` moves to `qy`.
    - `qF` is the accepting state for detecting an adjacent repeated letter.

    The diagram below shows the transition pattern schematically.
    """)
    st.graphviz_chart("""
    digraph DFA {
        rankdir=LR;
        graph [bgcolor="transparent", nodesep=0.55, ranksep=0.8];
        node [shape=circle, style=filled, fillcolor="#DCEAFE",
              color="#4776A8", fontcolor="#172554"];
        edge [color="#64748b", fontcolor="#64748b"];

        start [shape=point, label="", width=0.12];
        q0 [label="q0"];
        qa [label="qa ... qz"];
        qF [shape=doublecircle, label="qF",
            fillcolor="#BBF7D0", color="#15803D"];

        start -> q0;
        q0 -> qa [label="read x"];
        qa -> qa [label="read y ≠ x"];
        qa -> qF [label="read x again"];
        qF -> qF [label="any letter"];
    }
    """, use_container_width=True)

with st.expander("View every state", expanded=False):
    show_state_grid()

with st.expander("Character-by-character trace", expanded=False):
    trace_input = st.text_input(
        "Word to trace",
        value="helloooo",
        max_chars=100,
    )

    if trace_input:
        rows, detected = trace_word(trace_input)

        if detected:
            st.success("An adjacent repeated letter was detected.")
        else:
            st.info("No adjacent repeated letter was detected.")

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

st.caption(
    "Note: dictionary correction depends on the installed SymSpell dictionary. "
    "This is a preliminary implementation of the normalization pipeline."
)
