import streamlit as st
import pandas as pd

# -----------------------------
# Page config + styling
# -----------------------------
st.set_page_config(page_title="X MVP — Plates", layout="wide")

st.markdown(
    """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1150px; }

h1 { font-size: 54px !important; font-weight: 900 !important; letter-spacing: -1px; margin-bottom: 0.25rem !important; }
h2 { font-size: 42px !important; font-weight: 900 !important; letter-spacing: -0.5px; margin-top: 0.4rem !important; margin-bottom: 0.2rem !important; }
.small { font-size: 14px; opacity: 0.75; }

.hr { height: 1px; background: rgba(0,0,0,0.12); margin: 14px 0 10px 0; }

.section-header { display:flex; align-items:flex-start; justify-content:space-between; gap: 16px; margin-top: 10px; }
.step-circle {
  width: 48px; height: 48px; border-radius: 999px;
  background: #000; color:#fff; display:flex; align-items:center; justify-content:center;
  font-weight: 900; font-size: 22px; flex: 0 0 auto;
}

.menu-row { padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.10); }
.item-name { font-size: 22px; font-weight: 900; letter-spacing: -0.3px; }
.price { font-size: 22px; font-weight: 700; white-space: nowrap; }

.pills { display:flex; gap: 8px; flex-wrap: wrap; align-items:center; margin-top: 6px; }
.pill {
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding: 2px 8px;
  border-radius: 8px;
  border: 2px solid #000;
  font-size: 12px;
  font-weight: 900;
  line-height: 1.1;
}
.pill-soft { border: 2px solid rgba(0,0,0,0.25); font-weight: 800; }
.pill-yellow { background: #ffeb63; border: 0; padding: 4px 10px; border-radius: 8px; }
.pill-gray { background: rgba(0,0,0,0.08); border: 0; padding: 4px 10px; border-radius: 8px; font-weight: 800; }

.card {
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 14px 14px;
  background: rgba(255,255,255,0.02);
}

.stButton>button {
  border-radius: 10px !important;
  font-weight: 800 !important;
  padding: 0.45rem 0.65rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

def eur(x: float) -> str:
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s}€"

# -----------------------------
# Menu data
# -----------------------------
MENU = {
    "TO SHARE.": {
        "step": 1,
        "subtitle": "Choose a dish to share:",
        "items": [
            {"name": "BAKED FETA", "badges": ["VE"], "tags": ["BACK IN"], "price": 6.95},
            {"name": "CHARCOAL-GRILLED WHOLE LEEK", "badges": ["PB"], "tags": ["BACK IN"], "price": 5.95},
            {"name": "BEN’S SWEET POTATO FRIES", "badges": ["PB"], "tags": ["TOP SELLER"], "price": 4.95},
            {"name": "HUMMUS TO SHARE", "badges": ["PB"], "tags": [], "price": 4.95},
            {"name": "ARTISANAL SOURDOUGH BREAD WITH SMOKED OLIVE OIL BUTTER*", "badges": ["VE"], "tags": [], "price": 3.45,
             "note": "*You can order an extra piece of bread for 0,95€."},
        ],
    },
    "MARKET PLATES.": {
        "step": 2,
        "subtitle": "Choose between salad & bread, salad & grain salad, double salad or double bread.",
        "items": [
            {"name": "HOMEMADE FALAFEL WITH TAHINI SAUCE", "badges": ["PB"], "tags": [], "price": 8.95},
            {"name": "PIRI PIRI CHICKEN", "badges": [], "tags": ["TOP SELLER"], "price": 9.25, "icons": ["🌶️"]},
            {"name": "LEMON MUSTARD CHICKEN", "badges": [], "tags": [], "price": 9.25},
            {"name": "HERB TOFU", "badges": ["PB"], "tags": [], "price": 8.95, "icons": ["🌶️"]},
            {"name": "STEAK CHIMICHURRI", "badges": ["K"], "tags": [], "price": 9.95},
            {"name": "TUNA TATAKI WITH AJÍ AMARILLO¹", "badges": [], "tags": [], "price": 9.95, "icons": ["🌶️"]},
            {"name": "HONEST SALMON", "badges": [], "tags": [], "price": 10.45},
            {"name": "VEGGIE PLATE", "badges": [], "tags": [], "price": 8.95},
        ],
    },
    "GARDEN BOWLS.": {
        "step": 2,
        "subtitle": "Choose your salad: Bread not included.",
        "items": [
            {"name": "PISTACHIO CAESAR CRUNCH", "badges": ["VE"], "tags": ["NEW"], "price": 8.95},
            {"name": "LATIN LOVER", "badges": ["PB"], "tags": ["TOP SELLER"], "price": 8.95, "icons": ["🌶️"]},
            {"name": "SPICY FETA BOWL", "badges": ["VE"], "tags": [], "price": 8.95, "icons": ["🌶️"]},
            {"name": "WILD MEDITERRANEAN", "badges": ["PB"], "tags": [], "price": 8.95, "icons": ["🌶️"]},
            {"name": "AVOCADO SUPERGREEN", "badges": ["PB"], "tags": [], "price": 8.95},
        ],
    },
    "EXTRA PROTEIN.": {
        "step": 3,
        "subtitle": "Add more protein to your dish:",
        "items": [
            {"name": "HOMEMADE FALAFEL", "badges": ["PB"], "tags": [], "price_s": 3.95, "price_l": 6.45},
            {"name": "PIRI PIRI CHICKEN", "badges": [], "tags": ["TOP SELLER"], "price_s": 3.95, "price_l": 6.45, "icons": ["🌶️"]},
            {"name": "LEMON MUSTARD CHICKEN", "badges": [], "tags": [], "price_s": 3.95, "price_l": 6.45},
            {"name": "HERB TOFU", "badges": ["PB"], "tags": [], "price_s": 3.95, "price_l": 6.45, "icons": ["🌶️"]},
            {"name": "HOT HONEY HALLOUMI", "badges": ["VE"], "tags": [], "price_s": 3.95, "price_l": 6.45, "icons": ["🌶️"]},
            {"name": "STEAK CHIMICHURRI", "badges": ["K"], "tags": [], "price_s": 4.95, "price_l": 7.45},
            {"name": "TUNA TATAKI¹", "badges": [], "tags": [], "price_s": 4.95, "price_l": 7.45, "icons": ["🌶️"]},
            {"name": "HONEST SALMON", "badges": [], "tags": [], "price_s": None, "price_l": 7.95},
            {"name": "SPICY SALMON", "badges": [], "tags": [], "price_s": 4.95, "price_l": 7.45, "icons": ["🌶️"]},
        ],
    },
    "SIDES.": {
        "step": 4,
        "subtitle": "Complement your dish with sides:",
        "items": [
            {"name": "HOUSE HUMMUS WITH PISTACHIO", "badges": ["PB"], "tags": [], "price": 3.45},
            {"name": "SMASHED POTATOES WITH TRUFFLE MAYO", "badges": ["PB"], "tags": ["TOP SELLER"], "price": 3.45},
            {"name": "CHARCOAL-GRILLED PUMPKIN", "badges": ["VE"], "tags": ["NEW"], "price": 3.45},
            {"name": "BRUSSELS SPROUTS", "badges": ["PB"], "tags": ["NEW"], "price": 3.45},
            {"name": "GLAZED CARROTS", "badges": ["PB"], "tags": ["NEW"], "price": 3.45},
            {"name": "PLANT-BASED MUSHROOM RISOTTO", "badges": ["PB"], "tags": ["NEW"], "price": 3.45},
            {"name": "GRILLED AVOCADO NIKKEI", "badges": ["PB"], "tags": [], "price": 3.45, "icons": ["🌶️"]},
            {"name": "ROASTED SWEET POTATO WITH TAHINI", "badges": ["PB"], "tags": [], "price": 3.45},
            {"name": "SEASONAL VEGGIES", "badges": ["PB"], "tags": [], "price": 3.45},
        ],
    },
}

# -----------------------------
# State
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "saved_plates" not in st.session_state:
    st.session_state.saved_plates = []
if "orders" not in st.session_state:
    st.session_state.orders = []
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "Guest", "goal": "Feel balanced"}

GOALS = ["Build muscle", "Stay lean", "Feel balanced", "Just tastes good"]

def cart_total() -> float:
    return float(sum(x["Price"] for x in st.session_state.cart))

def add_to_cart(section: str, item: dict, size: str | None = None):
    if size == "S":
        price = item.get("price_s")
        if price is None:
            return
        label = f"{item['name']} (S)"
    elif size == "L":
        price = item.get("price_l")
        if price is None:
            return
        label = f"{item['name']} (L)"
    else:
        price = item.get("price")
        label = item["name"]

    st.session_state.cart.insert(0, {"Section": section, "Item": label, "Price": float(price)})

def pills_html(badges, icons, tags):
    # CSS-only pills; NO injected HTML spans with dynamic attributes
    parts = []
    for b in badges:
        parts.append(f"<span class='pill'>{b}</span>")
    for ic in icons:
        parts.append(f"<span class='pill pill-soft'>{ic}</span>")

    for t in tags:
        if t in ["TOP SELLER", "NEW"]:
            star = "★ " if t == "TOP SELLER" else ""
            parts.append(f"<span class='pill pill-yellow'>{star}{t}</span>")
        else:
            parts.append(f"<span class='pill pill-gray'>{t}</span>")

    if not parts:
        return ""

    return f"<div class='pills'>{''.join(parts)}</div>"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### Cart")
    if st.session_state.cart:
        st.dataframe(pd.DataFrame(st.session_state.cart), hide_index=True, use_container_width=True)
        st.markdown(f"**Total:** {eur(cart_total())}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Clear", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        with c2:
            if st.button("Checkout (demo)", use_container_width=True):
                st.session_state.orders.insert(
                    0,
                    {"type": "checkout", "customer": st.session_state.profile["name"], "items": list(st.session_state.cart), "total": cart_total()},
                )
                st.session_state.cart = []
                st.success("Checked out (demo).")
                st.rerun()
    else:
        st.caption("Add items from the menu.")

    st.divider()
    st.markdown("### Quick profile")
    st.session_state.profile["name"] = st.text_input("Name", st.session_state.profile["name"])
    st.session_state.profile["goal"] = st.selectbox("Goal", GOALS, index=GOALS.index(st.session_state.profile["goal"]))

# -----------------------------
# Main
# -----------------------------
st.title("X MVP — Plates")
st.markdown('<div class="small">Honest Greens-style menu + customization + saved plates</div>', unsafe_allow_html=True)

tabs = st.tabs(["Menu", "Customize a Plate", "Saved Plates", "Orders & Analytics"])

# -----------------------------
# TAB 1: Menu
# -----------------------------
with tabs[0]:
    for section_name, section in MENU.items():
        header = f"""
        <div class="section-header">
          <div>
            <h2>{section_name}</h2>
            <div class="small">{section.get('subtitle','')}</div>
          </div>
          <div class="step-circle">{section.get('step', '')}</div>
        </div>
        <div class="hr"></div>
        """
        st.markdown(header, unsafe_allow_html=True)

        if section_name == "EXTRA PROTEIN.":
            st.markdown(
                "<div style='display:flex; justify-content:flex-end; gap:10px; opacity:0.75; font-weight:800; margin-top:-6px;'>"
                "<span class='pill pill-soft'>S</span><span class='pill pill-soft'>L</span></div>",
                unsafe_allow_html=True,
            )

        for idx, item in enumerate(section["items"]):
            badges = item.get("badges", [])
            tags = item.get("tags", [])
            icons = item.get("icons", [])

            if section_name == "EXTRA PROTEIN.":
                p_s = item.get("price_s")
                p_l = item.get("price_l")
                right_price = f"{eur(p_s) if p_s is not None else '—'}  {eur(p_l) if p_l is not None else '—'}"
            else:
                right_price = eur(item.get("price", 0.0))

            row = st.columns([7, 2.2])

            with row[0]:
                st.markdown("<div class='menu-row'>", unsafe_allow_html=True)

                top = st.columns([6, 1])
                with top[0]:
                    st.markdown(f"<div class='item-name'>{item['name']}</div>", unsafe_allow_html=True)
                    pills = pills_html(badges, icons, tags)
                    if pills:
                        st.markdown(pills, unsafe_allow_html=True)
                with top[1]:
                    st.markdown(f"<div class='price'>{right_price}</div>", unsafe_allow_html=True)

                if item.get("note"):
                    st.markdown(f"<div class='small'>{item['note']}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with row[1]:
                if section_name == "EXTRA PROTEIN.":
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Add S", key=f"{section_name}_{idx}_S", use_container_width=True, disabled=item.get("price_s") is None):
                            add_to_cart(section_name, item, size="S")
                            st.rerun()
                    with c2:
                        if st.button("Add L", key=f"{section_name}_{idx}_L", use_container_width=True, disabled=item.get("price_l") is None):
                            add_to_cart(section_name, item, size="L")
                            st.rerun()
                else:
                    if st.button("Add", key=f"{section_name}_{idx}_add", use_container_width=True):
                        add_to_cart(section_name, item)
                        st.rerun()

# -----------------------------
# TAB 2: Customize
# -----------------------------
with tabs[1]:
    st.subheader("Build a Market Plate (MVP)")
    st.caption("This is the product: consistent portions + goal-based defaults + save/reorder.")

    colL, colR = st.columns([1.4, 1.0], gap="large")

    with colL:
        protein_options = [x["name"] for x in MENU["MARKET PLATES."]["items"]]
        protein = st.selectbox("Choose a protein", protein_options, index=1)

        base = st.radio(
            "Choose your base",
            ["Salad & bread", "Salad & grain salad", "Double salad", "Double bread"],
            horizontal=True,
        )

        mode = st.radio("Mode", ["Simple", "Advanced (precision)"], horizontal=True)

        if mode == "Simple":
            protein_level = st.radio("Protein level", ["Light", "Regular", "High", "Extra"], index=1, horizontal=True)
            carbs_level = st.radio("Carbs (bread/grains)", ["Lower", "Balanced", "Higher"], index=1, horizontal=True)
            sauce_level = st.radio("Sauce", ["Light", "Normal", "Extra"], index=1, horizontal=True)

            protein_units = {"Light": 0.85, "Regular": 1.0, "High": 1.2, "Extra": 1.4}[protein_level]
            carb_units = {"Lower": 0.8, "Balanced": 1.0, "Higher": 1.2}[carbs_level]
            sauce_units = {"Light": 0.7, "Normal": 1.0, "Extra": 1.3}[sauce_level]
        else:
            protein_units = st.slider("Protein portion (units)", 0.7, 1.6, 1.0, 0.1)
            carb_units = st.slider("Carb portion (units)", 0.6, 1.5, 1.0, 0.1)
            sauce_units = st.slider("Sauce portion (units)", 0.6, 1.5, 1.0, 0.1)

        goal = st.session_state.profile["goal"]
        if goal == "Build muscle":
            protein_units *= 1.15
        elif goal == "Stay lean":
            carb_units *= 0.9
        elif goal == "Just tastes good":
            sauce_units *= 1.1

        base_price = next(x["price"] for x in MENU["MARKET PLATES."]["items"] if x["name"] == protein)
        delta = 0.0
        delta += max(0.0, protein_units - 1.0) * 2.00
        delta += (carb_units - 1.0) * 0.80
        delta += (sauce_units - 1.0) * 0.40

        est_protein_g = 38 * protein_units
        est_calories = 620 + (carb_units - 1.0) * 120 + (sauce_units - 1.0) * 60

        name = st.text_input("Name this plate", value=f"{protein} • {base}")
        notes = st.text_input("Notes (optional)", value="")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save plate", use_container_width=True):
                st.session_state.saved_plates.insert(
                    0,
                    {
                        "name": name,
                        "protein": protein,
                        "base": base,
                        "mode": mode,
                        "protein_units": round(protein_units, 2),
                        "carb_units": round(carb_units, 2),
                        "sauce_units": round(sauce_units, 2),
                        "price": float(base_price + delta),
                        "est_protein_g": float(est_protein_g),
                        "est_calories": float(est_calories),
                        "notes": notes,
                    },
                )
                st.success("Saved.")
        with c2:
            if st.button("🛒 Add customized plate to cart", use_container_width=True):
                st.session_state.cart.insert(0, {"Section": "CUSTOM PLATE", "Item": name, "Price": float(base_price + delta)})
                st.success("Added to cart.")
                st.rerun()

    with colR:
        st.markdown('<div class="card"><b>Live summary</b></div>', unsafe_allow_html=True)
        st.metric("Est. price", eur(base_price + delta))
        m1, m2 = st.columns(2)
        m1.metric("Est. protein", f"{est_protein_g:.0f} g")
        m2.metric("Est. calories", f"{est_calories:.0f}")

        st.write("")
        st.markdown(
            "<div class='card'><b>Why this is different</b><br/>"
            "• Portion fairness without “double protein” jumps<br/>"
            "• Goal-based defaults (quietly applied)<br/>"
            "• Saved plates for 1-tap reorders</div>",
            unsafe_allow_html=True,
        )

# -----------------------------
# TAB 3: Saved
# -----------------------------
with tabs[2]:
    st.subheader("Saved Plates")

    if not st.session_state.saved_plates:
        st.info("No saved plates yet. Build one in **Customize a Plate**.")
    else:
        for i, p in enumerate(st.session_state.saved_plates[:15]):
            c1, c2, c3 = st.columns([1.6, 0.9, 0.8])
            with c1:
                st.markdown(f"**{p['name']}**")
                if p.get("notes"):
                    st.caption(p["notes"])
                st.caption(f"{p['protein']} • {p['base']} • {p['mode']}")
            with c2:
                st.metric("Price", eur(p["price"]))
            with c3:
                if st.button("Reorder", key=f"re_{i}", use_container_width=True):
                    st.session_state.cart.insert(0, {"Section": "CUSTOM PLATE", "Item": p["name"], "Price": float(p["price"])})
                    st.success("Added to cart.")
                    st.rerun()
            st.divider()

# -----------------------------
# TAB 4: Orders
# -----------------------------
with tabs[3]:
    st.subheader("Orders & Analytics (demo)")

    if not st.session_state.orders:
        st.info("No checkouts yet. Add items to cart and click Checkout (demo).")
    else:
        orders_df = pd.DataFrame(
            [
                {"Customer": o.get("customer", ""), "Total": o.get("total", 0.0), "Items": len(o.get("items", []))}
                for o in st.session_state.orders
                if o.get("type") == "checkout"
            ]
        )
        st.dataframe(orders_df, use_container_width=True, hide_index=True)
        c1, c2 = st.columns(2)
        c1.metric("Checkouts", len(orders_df))
        c2.metric("Avg total", eur(float(orders_df["Total"].mean())) if len(orders_df) else eur(0.0))

        st.divider()
        st.markdown("**Latest order (raw)**")
        st.json(st.session_state.orders[0])
