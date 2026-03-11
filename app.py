import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

import database as db
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

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card h3 { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    .metric-card h1 { margin: 0.2rem 0 0; font-size: 2rem; }
    .meal-header {
        background: #f0f2f6;
        border-left: 4px solid #667eea;
        padding: 0.4rem 0.8rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .stProgress > div > div { border-radius: 10px; }
    div[data-testid="stExpander"] { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/000000/salad.png",
        width=60,
    )
    st.title("🥗 Calorie Tracker")
    st.caption("Indian Vegetarian Edition")
    st.divider()

    # Date picker
    selected_date = st.date_input(
        "📅 Select Date",
        value=date.today(),
        max_value=date.today(),
    )
    date_str = selected_date.strftime("%Y-%m-%d")

    st.divider()

    # Daily calorie target
    st.subheader("🎯 Daily Calorie Target")
    current_target = db.get_daily_target(date_str)
    new_target = st.number_input(
        "Set target (kcal)",
        min_value=500,
        max_value=5000,
        value=current_target,
        step=50,
        help="Recommended: 1800–2200 kcal for average adults",
    )
    if st.button("✅ Save Target", use_container_width=True):
        db.set_daily_target(date_str, int(new_target))
        st.success(f"Target set to {new_target} kcal")
        st.rerun()

    st.divider()
    st.caption("Built with ❤️ using Streamlit")

# ─── Main Area ────────────────────────────────────────────────────────────────
st.title(f"🥗 Indian Calorie Tracker")
st.caption(f"Tracking: **{selected_date.strftime('%A, %d %B %Y')}**")

daily_target = db.get_daily_target(date_str)
daily_total = db.get_daily_total(date_str)
remaining = daily_target - daily_total
meal_totals = db.get_meal_totals(date_str)

# ─── Top Metrics ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎯 Daily Target</h3>
        <h1>{daily_target}</h1>
        <small>kcal</small>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg,#11998e,#38ef7d);">
        <h3>🍽️ Consumed</h3>
        <h1>{daily_total}</h1>
        <small>kcal</small>
    </div>""", unsafe_allow_html=True)

with col3:
    color = "#e74c3c" if remaining < 0 else "#f39c12" if remaining < 200 else "#2ecc71"
    label = "Over by" if remaining < 0 else "Remaining"
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg,{color},{color}aa);">
        <h3>⚡ {label}</h3>
        <h1>{abs(remaining)}</h1>
        <small>kcal</small>
    </div>""", unsafe_allow_html=True)

with col4:
    pct = min(int((daily_total / daily_target) * 100), 100) if daily_target > 0 else 0
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg,#fc5c7d,#6a3093);">
        <h3>📊 Progress</h3>
        <h1>{pct}%</h1>
        <small>of daily goal</small>
    </div>""", unsafe_allow_html=True)

# Progress bar
progress_val = min(daily_total / daily_target, 1.0) if daily_target > 0 else 0
bar_color = "red" if daily_total > daily_target else "green"
st.progress(progress_val, text=f"{daily_total} / {daily_target} kcal consumed")

st.divider()

# ─── Add Food Section ─────────────────────────────────────────────────────────
st.subheader("➕ Add Food Entry")

with st.container():
    c1, c2 = st.columns([1, 2])

    with c1:
        meal_period = st.selectbox(
            "🕐 Meal Period",
            options=MEAL_PERIODS,
            index=0,
        )

    with c2:
        search_mode = st.radio(
            "Browse by",
            ["Category", "Search by name"],
            horizontal=True,
        )

    if search_mode == "Category":
        cat_col, food_col = st.columns(2)
        with cat_col:
            selected_category = st.selectbox("📂 Category", options=CATEGORIES)
        with food_col:
            cat_foods = get_foods_by_category(selected_category)
            selected_food = st.selectbox("🍛 Food Item", options=sorted(cat_foods.keys()))
    else:
        all_foods = get_all_food_names()
        selected_food = st.selectbox(
            "🔍 Search Food",
            options=all_foods,
            help="Type to filter",
        )

    if selected_food:
        food_info = get_food_info(selected_food)
        cal_per_unit = food_info.get("calories", 0)
        unit = food_info.get("unit", "serving")

        qty_col, info_col, btn_col = st.columns([1, 2, 1])

        with qty_col:
            quantity = st.number_input(
                f"Quantity ({unit})",
                min_value=0.5,
                max_value=50.0,
                value=1.0,
                step=0.5,
            )

        with info_col:
            total_cal = round(quantity * cal_per_unit, 1)
            st.info(
                f"**{cal_per_unit} kcal** per {unit}  \n"
                f"**Total for this entry: {total_cal} kcal**"
            )

        with btn_col:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Add", type="primary", use_container_width=True):
                db.add_food_entry(
                    date_str, meal_period, selected_food,
                    quantity, unit, cal_per_unit
                )
                st.success(f"Added {selected_food} ({total_cal} kcal) to {meal_period}")
                st.rerun()

st.divider()

# ─── Today's Food Log ─────────────────────────────────────────────────────────
st.subheader("📋 Today's Food Log")

food_log = db.get_food_log(date_str)

if not food_log:
    st.info("No food entries yet for this day. Add your first meal above!")
else:
    for period in MEAL_PERIODS:
        period_entries = [e for e in food_log if e["meal_period"] == period]
        if not period_entries:
            continue

        period_total = meal_totals.get(period, 0)
        period_icons = {
            "Breakfast": "🌅",
            "Lunch": "☀️",
            "Dinner": "🌙",
            "Snack / Anytime": "🍎",
        }
        icon = period_icons.get(period, "🍽️")

        with st.expander(
            f"{icon} **{period}** — {period_total} kcal",
            expanded=True,
        ):
            df = pd.DataFrame(period_entries)
            df = df.rename(columns={
                "food_name": "Food",
                "quantity": "Qty",
                "unit": "Unit",
                "calories_per_unit": "Cal/Unit",
                "total_calories": "Total Cal",
            })

            # Display table with delete buttons
            for _, row in df.iterrows():
                rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([3, 1, 1.5, 1.5, 1.5, 0.8])
                rc1.write(row["Food"])
                rc2.write(f"{row['Qty']}")
                rc3.write(row["Unit"])
                rc4.write(f"{row['Cal/Unit']} kcal")
                rc5.write(f"**{row['Total Cal']} kcal**")
                entry_id = [e["id"] for e in period_entries if e["food_name"] == row["Food"]][0]
                if rc6.button("🗑️", key=f"del_{entry_id}", help="Remove this entry"):
                    db.delete_food_entry(entry_id)
                    st.rerun()

    st.divider()

# ─── Charts ───────────────────────────────────────────────────────────────────
st.subheader("📊 Visual Summary")

chart_col1, chart_col2 = st.columns(2)

# Pie chart — meal distribution
with chart_col1:
    if meal_totals:
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(meal_totals.keys()),
            values=list(meal_totals.values()),
            hole=0.4,
            marker=dict(colors=["#667eea", "#11998e", "#fc5c7d", "#f39c12"]),
        )])
        fig_pie.update_layout(
            title="Calories by Meal Period",
            showlegend=True,
            height=320,
            margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Add food entries to see the meal distribution chart.")

# Bar chart — target vs consumed
with chart_col2:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["Target", "Consumed"],
        y=[daily_target, daily_total],
        marker_color=["#667eea", "#11998e" if daily_total <= daily_target else "#e74c3c"],
        text=[f"{daily_target} kcal", f"{daily_total} kcal"],
        textposition="outside",
    ))
    fig_bar.update_layout(
        title="Target vs Consumed",
        yaxis_title="Calories (kcal)",
        height=320,
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Weekly trend chart
st.subheader("📈 Weekly Trend (Last 7 Days)")
weekly_data = db.get_weekly_summary(date_str)

if weekly_data:
    all_dates = [(selected_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    totals_map = {d["date"]: d["total"] for d in weekly_data}
    targets_map = {d: db.get_daily_target(d) for d in all_dates}

    fig_week = go.Figure()
    fig_week.add_trace(go.Scatter(
        x=all_dates,
        y=[targets_map.get(d, daily_target) for d in all_dates],
        mode="lines",
        name="Target",
        line=dict(color="#667eea", dash="dash", width=2),
    ))
    fig_week.add_trace(go.Bar(
        x=all_dates,
        y=[totals_map.get(d, 0) for d in all_dates],
        name="Consumed",
        marker_color=[
            "#11998e" if totals_map.get(d, 0) <= targets_map.get(d, daily_target) else "#e74c3c"
            for d in all_dates
        ],
        opacity=0.8,
    ))
    fig_week.update_layout(
        xaxis_title="Date",
        yaxis_title="Calories (kcal)",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=30, b=30, l=20, r=20),
    )
    st.plotly_chart(fig_week, use_container_width=True)
else:
    st.info("No data yet for the weekly trend. Start logging your meals!")

st.divider()

# ─── Food Reference Table ─────────────────────────────────────────────────────
with st.expander("📖 Food Calorie Reference Table"):
    ref_df = pd.DataFrame([
        {
            "Food Item": name,
            "Category": info["category"],
            "Calories": info["calories"],
            "Per": info["unit"],
        }
        for name, info in FOOD_DATABASE.items()
    ]).sort_values(["Category", "Food Item"])

    filter_cat = st.selectbox("Filter by category", ["All"] + CATEGORIES, key="ref_cat")
    if filter_cat != "All":
        ref_df = ref_df[ref_df["Category"] == filter_cat]

    st.dataframe(ref_df.reset_index(drop=True), use_container_width=True, height=400)
