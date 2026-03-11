import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

import database as db
from auth import show_auth_page, show_sidebar_user
from styles import inject_css
from food_data import (
    FOOD_DATABASE, MEAL_PERIODS, CATEGORIES,
    get_foods_by_category, get_food_info, get_all_food_names,
)

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Calorie Tracker",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Init DB ──────────────────────────────────────────────────────────────────
db.init_db()

# ─── CSS ──────────────────────────────────────────────────────────────────────
inject_css()

# ─── Auth gate ────────────────────────────────────────────────────────────────
user = show_auth_page()
if user is None:
    st.stop()

user_id: int = user["id"]

# ─── Date nav state ───────────────────────────────────────────────────────────
if "nav_date" not in st.session_state:
    st.session_state["nav_date"] = date.today()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("🥗 **Calorie Tracker**")
    st.caption("Indian Vegetarian Edition")
    st.divider()
    show_sidebar_user(user)

    # Daily target
    date_str_sidebar = st.session_state["nav_date"].strftime("%Y-%m-%d")
    current_target = db.get_daily_target(user_id, date_str_sidebar)

    new_target = st.number_input(
        "🎯 Daily Target (kcal)",
        min_value=500,
        max_value=5000,
        value=current_target,
        step=50,
        help="Recommended: 1800–2200 kcal for average adults",
    )
    if st.button("Save Target", use_container_width=True, type="primary"):
        db.set_daily_target(user_id, date_str_sidebar, int(new_target))
        st.success(f"Target set to {int(new_target)} kcal")
        st.rerun()

# ─── Fetch data for selected date ─────────────────────────────────────────────
selected_date = st.session_state["nav_date"]
date_str      = selected_date.strftime("%Y-%m-%d")

daily_target = db.get_daily_target(user_id, date_str)
daily_total  = db.get_daily_total(user_id, date_str)
remaining    = daily_target - daily_total
meal_totals  = db.get_meal_totals(user_id, date_str)
food_log     = db.get_food_log(user_id, date_str)

pct_consumed = round((daily_total / daily_target) * 100, 1) if daily_target > 0 else 0.0

# ─── Status helpers ───────────────────────────────────────────────────────────
def _status(pct: float) -> str:
    if pct >= 100:  return "red"
    if pct >= 80:   return "amber"
    return "green"

status = _status(pct_consumed)
STATUS_COLORS = {"green": "#10B981", "amber": "#F59E0B", "red": "#EF4444"}
ring_color = STATUS_COLORS[status]

# ─── 1. Header ────────────────────────────────────────────────────────────────
first_name = user["name"].split()[0]
st.markdown(f"**Welcome back, {first_name}!** &nbsp; {selected_date.strftime('%A, %d %B %Y')}")

# Date navigation — flat row, plain ASCII button labels (no Unicode arrows)
prev_c, date_c, next_c, today_c = st.columns([1, 4, 1, 1])
with prev_c:
    if st.button("Prev", use_container_width=True):
        st.session_state["nav_date"] -= timedelta(days=1)
        st.rerun()
with date_c:
    picked = st.date_input(
        "Select date",
        value=st.session_state["nav_date"],
        max_value=date.today(),
        label_visibility="collapsed",
    )
    if picked != st.session_state["nav_date"]:
        st.session_state["nav_date"] = picked
        st.rerun()
with next_c:
    if st.button("Next", use_container_width=True,
                 disabled=st.session_state["nav_date"] >= date.today()):
        st.session_state["nav_date"] += timedelta(days=1)
        st.rerun()
with today_c:
    if st.button("Today", use_container_width=True):
        st.session_state["nav_date"] = date.today()
        st.rerun()

st.divider()

# ─── 2. Hero metrics row ──────────────────────────────────────────────────────
ring_col, m1, m2, m3 = st.columns([2, 1, 1, 1])

with ring_col:
    ring_pct_display = min(pct_consumed, 100)
    fig_ring = go.Figure(go.Pie(
        values=[ring_pct_display, max(100 - ring_pct_display, 0)],
        hole=0.78,
        marker=dict(colors=[ring_color, "#E2E8F0"]),
        sort=False,
        showlegend=False,
        hoverinfo="skip",
        textinfo="none",
    ))
    fig_ring.add_annotation(
        text=f"<b>{pct_consumed:.0f}%</b><br><span style='font-size:11px;color:#64748B;'>consumed</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, color="#0F172A", family="Inter"),
        xanchor="center", yanchor="middle",
    )
    fig_ring.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar": False})

PILL_ACCENT = {"green": "#10B981", "amber": "#F59E0B", "red": "#EF4444", "indigo": "#4F46E5"}

def _pill(label: str, value, unit: str, accent: str) -> str:
    color = PILL_ACCENT.get(accent, "#4F46E5")
    return f"""
    <div style="
        background:#FFFFFF;border-radius:14px;text-align:center;
        padding:1.1rem 0.75rem;
        border-top:4px solid {color};
        box-shadow:0 1px 4px rgba(0,0,0,0.07),0 4px 16px rgba(79,70,229,0.07);
    ">
        <p style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;color:#64748B;margin:0 0 0.2rem;">{label}</p>
        <p style="font-size:1.9rem;font-weight:800;color:#0F172A;margin:0;line-height:1;">{value}</p>
        <p style="font-size:0.68rem;color:#94A3B8;margin:0.15rem 0 0;">{unit}</p>
    </div>"""

with m1:
    st.markdown(_pill("🎯 Target", daily_target, "kcal", "indigo"), unsafe_allow_html=True)

with m2:
    st.markdown(_pill("🍽️ Consumed", daily_total, "kcal", status), unsafe_allow_html=True)

with m3:
    rem_label = "Over by" if remaining < 0 else "Remaining"
    rem_accent = "red" if remaining < 0 else ("amber" if remaining < 200 else "green")
    st.markdown(_pill(f"⚡ {rem_label}", abs(remaining), "kcal", rem_accent), unsafe_allow_html=True)

# Contextual insight
if pct_consumed < 50:
    insight = "Good start! Keep logging your meals."
elif pct_consumed < 80:
    insight = f"On track! {remaining} kcal remaining."
elif pct_consumed < 100:
    insight = f"Almost there! {remaining} kcal left — choose wisely."
else:
    insight = f"Daily target reached. {abs(remaining)} kcal over."

st.markdown(
    f'<p style="font-size:0.875rem;color:#64748B;text-align:center;'
    f'padding:0.25rem 0 0.75rem;font-style:italic;">{insight}</p>',
    unsafe_allow_html=True,
)

# ─── 3. Add Food ──────────────────────────────────────────────────────────────
_OTHERS = "Others (Custom)"

with st.expander("➕ Add Food Entry", expanded=True):
    c1, c2 = st.columns([1, 2])
    with c1:
        meal_period = st.selectbox("🕐 Meal Period", options=MEAL_PERIODS)
    with c2:
        search_mode = st.radio("Browse by", ["Category", "Search by name"], horizontal=True)

    if search_mode == "Category":
        cat_col, food_col = st.columns(2)
        with cat_col:
            selected_category = st.selectbox("📂 Category", options=[_OTHERS] + CATEGORIES)
        with food_col:
            if selected_category == _OTHERS:
                selected_food = _OTHERS
            else:
                cat_foods = get_foods_by_category(selected_category)
                selected_food = st.selectbox("🍛 Food Item", options=sorted(cat_foods.keys()))
    else:
        selected_food = st.selectbox(
            "🔍 Search Food", options=[_OTHERS] + get_all_food_names(), help="Type to filter"
        )

    # Custom food inputs when "Others" is chosen
    if selected_food == _OTHERS:
        cf1, cf2 = st.columns(2)
        custom_food_name = cf1.text_input(
            "Food Name", placeholder="e.g. Homemade Khichdi", key="custom_food_name"
        )
        custom_cal = cf2.number_input(
            "Calories per serving (kcal)", min_value=1, max_value=5000, value=200, step=5,
            key="custom_cal"
        )
        food_name_to_log = custom_food_name.strip() if custom_food_name.strip() else ""
        cal_per_unit = float(custom_cal)
        unit = "serving"
    else:
        food_info        = get_food_info(selected_food)
        cal_per_unit     = food_info.get("calories", 0)
        unit             = food_info.get("unit", "serving")
        food_name_to_log = selected_food

    qty_col, info_col, btn_col = st.columns([1, 2, 1])
    with qty_col:
        quantity = st.number_input(
            f"Quantity ({unit})",
            min_value=0.5, max_value=50.0, value=1.0, step=0.5,
        )
    with info_col:
        total_cal = round(quantity * cal_per_unit, 1)
        st.info(
            f"**{cal_per_unit} kcal** per {unit}  \n"
            f"**Total for this entry: {total_cal} kcal**"
        )
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        add_disabled = (selected_food == _OTHERS and not food_name_to_log)
        if st.button("➕ Add", type="primary", use_container_width=True, disabled=add_disabled):
            db.add_food_entry(
                user_id, date_str, meal_period,
                food_name_to_log, quantity, unit, cal_per_unit,
            )
            st.toast(f"Added {food_name_to_log} to {meal_period} — {total_cal} kcal", icon="✅")
            st.rerun()

# ─── 4. Food Log ──────────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-size:1rem;font-weight:700;color:#0F172A;margin:1.25rem 0 0.75rem;">📋 Today\'s Food Log</p>',
    unsafe_allow_html=True,
)

period_icons = {
    "Breakfast":      "🌅",
    "Lunch":          "☀️",
    "Dinner":         "🌙",
    "Snack / Anytime": "🍎",
}

if not food_log:
    st.markdown("""
    <div style="text-align:center;padding:2.5rem 1rem;color:#94A3B8;">
        <div style="font-size:2.5rem;margin-bottom:0.5rem;">🍽️</div>
        <p style="font-size:1rem;font-weight:600;color:#64748B;margin:0;">No entries yet for this day</p>
        <p style="font-size:0.82rem;margin:0.2rem 0 0;">Add your first meal using the form above!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for period in MEAL_PERIODS:
        period_entries = [e for e in food_log if e["meal_period"] == period]
        if not period_entries:
            continue

        period_total = meal_totals.get(period, 0)
        icon = period_icons.get(period, "🍽️")

        st.markdown(f"""
        <div style="
            display:flex;align-items:center;gap:0.5rem;padding:0.7rem 1rem;
            background:#FFFFFF;border-radius:10px;border:1px solid #E2E8F0;
            margin-bottom:0.4rem;box-shadow:0 1px 3px rgba(0,0,0,0.05);
        ">
            <span style="font-size:1.2rem;">{icon}</span>
            <span style="font-weight:700;color:#0F172A;font-size:0.95rem;flex:1;">{period}</span>
            <span style="
                background:#EEF2FF;color:#4F46E5;font-size:0.72rem;font-weight:700;
                padding:0.2rem 0.65rem;border-radius:999px;border:1px solid #C7D2FE;
            ">{period_total} kcal</span>
        </div>
        """, unsafe_allow_html=True)

        for entry in period_entries:
            row_col, del_col = st.columns([6, 1])
            with row_col:
                st.markdown(f"""
                <div style="
                    background:#F8FAFC;border-radius:8px;padding:0.55rem 0.9rem;
                    margin-bottom:0.3rem;display:flex;align-items:center;
                    justify-content:space-between;border:1px solid #E2E8F0;
                ">
                    <div>
                        <span style="font-weight:600;color:#0F172A;font-size:0.875rem;">{entry['food_name']}</span>
                        <span style="font-size:0.775rem;color:#94A3B8;margin-left:0.5rem;">· {entry['quantity']} {entry['unit']}</span>
                    </div>
                    <span style="font-weight:700;color:#4F46E5;font-size:0.875rem;white-space:nowrap;">{entry['total_calories']} kcal</span>
                </div>
                """, unsafe_allow_html=True)
            with del_col:
                st.markdown("<div style='padding-top:0.3rem'></div>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{entry['id']}", help="Remove entry"):
                    db.delete_food_entry(entry["id"], user_id)
                    st.rerun()

        st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

# ─── 5. Charts ────────────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-size:1rem;font-weight:700;color:#0F172A;margin:1.25rem 0 0.75rem;">📊 Visual Summary</p>',
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["  📊  Today's Breakdown  ", "  📈  Weekly Trend  "])

with tab1:
    ch1, ch2 = st.columns(2)

    with ch1:
        if meal_totals:
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(meal_totals.keys()),
                values=list(meal_totals.values()),
                hole=0.45,
                marker=dict(colors=["#4F46E5", "#10B981", "#F59E0B", "#EC4899"]),
                textfont=dict(family="Inter", size=12),
            )])
            fig_pie.update_layout(
                showlegend=True, height=300,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter"),
                legend=dict(font=dict(family="Inter", size=12)),
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""
            <div class="empty-state" style="padding:2rem 1rem;">
                <div class="es-icon">🍩</div>
                <p class="es-sub">Add food entries to see meal distribution</p>
            </div>
            """, unsafe_allow_html=True)

    with ch2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=["Target", "Consumed"],
            y=[daily_target, daily_total],
            marker_color=["#4F46E5", ring_color],
            text=[f"{daily_target}", f"{daily_total}"],
            textposition="outside",
            textfont=dict(family="Inter", size=13, color="#0F172A"),
        ))
        fig_bar.update_layout(
            yaxis_title="Calories (kcal)", height=300,
            margin=dict(t=20, b=20, l=20, r=20), showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
            yaxis=dict(gridcolor="#F1F5F9"),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with tab2:
    weekly_data = db.get_weekly_summary(user_id, date_str)
    all_dates   = [
        (selected_date - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(6, -1, -1)
    ]
    totals_map  = {d["date"]: d["total"] for d in weekly_data}
    targets_map = {d: db.get_daily_target(user_id, d) for d in all_dates}

    bar_colors = [
        "#10B981" if totals_map.get(d, 0) <= targets_map.get(d, daily_target) else "#EF4444"
        for d in all_dates
    ]

    fig_week = go.Figure()
    fig_week.add_trace(go.Bar(
        x=all_dates,
        y=[totals_map.get(d, 0) for d in all_dates],
        name="Consumed",
        marker_color=bar_colors,
        opacity=0.85,
    ))
    fig_week.add_trace(go.Scatter(
        x=all_dates,
        y=[targets_map.get(d, daily_target) for d in all_dates],
        mode="lines+markers",
        name="Target",
        line=dict(color="#4F46E5", dash="dash", width=2),
        marker=dict(size=6, color="#4F46E5"),
    ))
    fig_week.update_layout(
        xaxis_title="Date", yaxis_title="Calories (kcal)",
        height=340,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(family="Inter")),
        margin=dict(t=30, b=30, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        yaxis=dict(gridcolor="#F1F5F9"),
    )
    st.plotly_chart(fig_week, use_container_width=True, config={"displayModeBar": False})

# ─── 6. Food Reference Table & Footer ────────────────────────────────────────
with st.expander(f"📖 Food Calorie Reference Table ({len(FOOD_DATABASE)} items)"):
    ref_df = pd.DataFrame([
        {
            "Food Item": name,
            "Category": info["category"],
            "Calories": info["calories"],
            "Per": info["unit"],
        }
        for name, info in FOOD_DATABASE.items()
    ]).sort_values(["Category", "Food Item"])

    filter_cat = st.selectbox(
        "Filter by category", ["All"] + CATEGORIES, key="ref_cat"
    )
    if filter_cat != "All":
        ref_df = ref_df[ref_df["Category"] == filter_cat]

    st.dataframe(ref_df.reset_index(drop=True), use_container_width=True, height=400)

# ─── 7. Admin Dashboard (superadmin only) ─────────────────────────────────────
if user.get("role") == "superadmin":
    st.divider()
    with st.expander("🔐 Admin Dashboard", expanded=False):
        st.markdown("**All Registered Users**")
        all_users = db.get_all_users()
        if all_users:
            users_df = pd.DataFrame(all_users)[
                ["name", "username", "email", "role", "sex", "age",
                 "weight_kg", "height_cm", "activity_level",
                 "calorie_need", "default_target", "created_at"]
            ]
            users_df.columns = [
                "Name", "Username", "Email", "Role", "Sex", "Age",
                "Weight (kg)", "Height (cm)", "Activity Level",
                "Calorie Need", "Daily Target", "Joined",
            ]
            st.dataframe(users_df, use_container_width=True, height=300)
        else:
            st.info("No users found.")

        st.markdown("**Food Log — All Users**")
        all_logs = db.get_admin_food_log(limit=1000)
        if all_logs:
            logs_df = pd.DataFrame(all_logs)[
                ["date", "name", "username", "meal_period",
                 "food_name", "quantity", "unit", "total_calories"]
            ]
            logs_df.columns = [
                "Date", "Name", "Username", "Meal",
                "Food", "Qty", "Unit", "Calories (kcal)",
            ]
            # Filter by user
            user_filter = st.selectbox(
                "Filter by user",
                ["All"] + sorted(logs_df["Username"].unique().tolist()),
                key="admin_user_filter",
            )
            if user_filter != "All":
                logs_df = logs_df[logs_df["Username"] == user_filter]
            st.dataframe(logs_df.reset_index(drop=True), use_container_width=True, height=400)

            total_entries = len(logs_df)
            total_kcal    = logs_df["Calories (kcal)"].sum()
            st.caption(f"Showing {total_entries} entries · {round(total_kcal)} kcal total")
        else:
            st.info("No food log entries yet.")

# ─── 8. Footer ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.caption(
    "⚠️ **Disclaimer:** This app is for personal calorie tracking purposes only and does not "
    "constitute medical, nutritional, or dietary advice. Calorie values are approximate. "
    "The developer is not a dietician or food specialist. "
    "Consult a qualified healthcare professional for personalised dietary guidance."
)
