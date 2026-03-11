import re
import streamlit as st
import streamlit.components.v1 as components
import database as db
from food_data import FOOD_DATABASE, CATEGORIES
from styles import inject_css


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def show_auth_page() -> dict | None:
    """
    If the user is already logged in (session state), return the user dict immediately.
    Otherwise render the login / register page and return None.
    Call st.stop() after this returns None so the rest of the app doesn't run.
    """
    if st.session_state.get("user"):
        return st.session_state["user"]

    inject_css()

    # Two-column split: hero (2) | form (3)
    left_col, right_col = st.columns([2, 3], gap="small")

    # ── Left: Hero panel ──────────────────────────────────────────────────────
    with left_col:
        fs = "display:flex;align-items:center;gap:0.5rem;color:#C7D2FE;font-size:0.875rem;margin-bottom:0.6rem;"
        cs = "color:#34D399;font-weight:800;font-size:1rem;"
        hero_html = (
            '<div style="background:linear-gradient(155deg,#1E1B4B 0%,#3730A3 60%,#4338CA 100%);'
            'border-radius:16px;padding:2.5rem 2rem;min-height:480px;'
            'display:flex;flex-direction:column;justify-content:center;color:#FFFFFF;'
            'font-family:Inter,sans-serif;">'
            '<div style="font-size:3rem;margin-bottom:0.5rem;">🥗</div>'
            '<div style="font-size:1.7rem;font-weight:800;color:#FFFFFF;margin-bottom:0.25rem;line-height:1.2;">Indian Calorie Tracker</div>'
            '<p style="color:#A5B4FC;font-size:0.875rem;margin-bottom:1.5rem;line-height:1.5;">Your personal nutrition companion — eat mindfully, live better.</p>'
            f'<div style="{fs}"><span style="{cs}">✓</span> {len(FOOD_DATABASE)}+ Indian vegetarian foods</div>'
            f'<div style="{fs}"><span style="{cs}">✓</span> Track Breakfast, Lunch, Dinner &amp; Snacks</div>'
            f'<div style="{fs}"><span style="{cs}">✓</span> Weekly calorie trends &amp; visual insights</div>'
            f'<div style="{fs}"><span style="{cs}">✓</span> Secure personal profiles &amp; history</div>'
            '<div style="margin-top:2rem;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:0.75rem 1rem;color:#E0E7FF;font-size:0.82rem;">'
            f'<strong style="color:#FFFFFF;font-size:1.4rem;font-weight:800;display:block;margin-bottom:0.1rem;">{len(FOOD_DATABASE)}</strong>'
            f'foods across {len(CATEGORIES)} categories'
            '</div>'
            '</div>'
        )
        components.html(hero_html, height=500, scrolling=False)

    # ── Right: Form panel ─────────────────────────────────────────────────────
    with right_col:
        st.markdown("""
        <div style="
            background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;
            padding:0.7rem 0.9rem;margin-bottom:1rem;font-size:0.78rem;
            color:#1D4ED8;line-height:1.55;
        ">
            ℹ️ <strong>Disclaimer:</strong> This app is a personal tool for tracking calorie
            consumption only — not medical or dietary advice. Calorie values are approximate.
            Consult a healthcare professional for personalised guidance.
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔐  Sign In", "📝  Create Account"])

        # ── Login ─────────────────────────────────────────────────────────────
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="your_username")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button(
                    "Sign In", use_container_width=True, type="primary"
                )

            if submitted:
                if not username or not password:
                    st.error("Please enter your username and password.")
                else:
                    user = db.verify_user(username, password)
                    if user:
                        st.session_state["user"] = user
                        st.rerun()
                    else:
                        st.error("Incorrect username or password.")

        # ── Register ──────────────────────────────────────────────────────────
        with tab_register:
            _ACTIVITY_OPTIONS = {
                "Sedentary (little or no exercise)": 1.2,
                "Lightly active (1–3 days/week)": 1.375,
                "Moderately active (3–5 days/week)": 1.55,
                "Active (6–7 days/week)": 1.725,
            }

            # ── Health profile OUTSIDE the form so BMR updates live ──
            st.markdown("**Health Profile** *(updates calorie need live)*")
            col_sex, col_age = st.columns(2)
            sex_r      = col_sex.selectbox("Sex", ["Male", "Female"], key="reg_sex")
            age_r      = col_age.number_input("Age (years)", min_value=10, max_value=100, value=25, step=1, key="reg_age")
            col_wt, col_ht = st.columns(2)
            weight_r   = col_wt.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=65.0, step=0.5, key="reg_wt")
            height_r   = col_ht.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=165.0, step=0.5, key="reg_ht")
            activity_r = st.selectbox("Activity Level", list(_ACTIVITY_OPTIONS.keys()), key="reg_act")

            # Live BMR calculation (Mifflin-St Jeor)
            if sex_r == "Male":
                bmr = (10 * weight_r) + (6.25 * height_r) - (5 * age_r) + 5
            else:
                bmr = (10 * weight_r) + (6.25 * height_r) - (5 * age_r) - 161
            calorie_need_r = round(bmr * _ACTIVITY_OPTIONS[activity_r])

            st.info(
                f"**Estimated Calorie Need: {calorie_need_r} kcal/day**  \n"
                f"BMR = {round(bmr)} kcal \u00d7 {_ACTIVITY_OPTIONS[activity_r]} "
                f"({activity_r.split('(')[0].strip()})"
            )

            st.markdown("**Account Details**")
            with st.form("register_form", clear_on_submit=False):
                name = st.text_input("Full Name", placeholder="Priya Sharma")
                col_u, col_e = st.columns(2)
                username_r = col_u.text_input("Username", placeholder="priya123")
                email_r    = col_e.text_input("Email", placeholder="priya@example.com")
                col_p, col_c = st.columns(2)
                password_r = col_p.text_input(
                    "Password", type="password", placeholder="Min 6 chars"
                )
                confirm_r = col_c.text_input(
                    "Confirm Password", type="password", placeholder="Same as above"
                )
                target_r = st.number_input(
                    "Your Daily Calorie Target (kcal)",
                    min_value=500, max_value=5000,
                    value=calorie_need_r, step=50,
                    help="Pre-filled from your calorie need — adjust as you wish.",
                )
                submitted_r = st.form_submit_button(
                    "Create Account", use_container_width=True, type="primary"
                )

            if submitted_r:
                errors: list[str] = []
                if not all([name, username_r, email_r, password_r, confirm_r]):
                    errors.append("All fields are required.")
                if not _is_valid_email(email_r):
                    errors.append("Please enter a valid email address.")
                if len(username_r) < 3:
                    errors.append("Username must be at least 3 characters.")
                if " " in username_r:
                    errors.append("Username cannot contain spaces.")
                if len(password_r) < 6:
                    errors.append("Password must be at least 6 characters.")
                if password_r != confirm_r:
                    errors.append("Passwords do not match.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    ok, msg = db.register_user(
                        name, username_r, email_r, password_r, int(target_r),
                        age=int(age_r), weight_kg=float(weight_r),
                        height_cm=float(height_r), sex=sex_r,
                        activity_level=activity_r,
                        calorie_need=calorie_need_r,
                    )
                    if ok:
                        st.success("Account created! Switch to the Sign In tab to log in.")
                    else:
                        st.error(msg)

    return None


def show_sidebar_user(user: dict):
    """Render user info and logout button in the sidebar."""
    # Avatar with initials
    initials = "".join(w[0].upper() for w in user["name"].split()[:2])
    st.sidebar.markdown(f"""
    <div style="padding:0.5rem 0;">
        <div style="
            width:46px;height:46px;border-radius:50%;
            background:linear-gradient(135deg,#6366F1,#8B5CF6);
            display:flex;align-items:center;justify-content:center;
            font-size:1.1rem;font-weight:800;color:#FFFFFF;
            margin-bottom:0.4rem;
            box-shadow:0 2px 8px rgba(99,102,241,0.4);
        ">{initials}</div>
        <div style="font-weight:700;color:#FFFFFF;font-size:1rem;margin-bottom:2px;">
            {user['name']}
        </div>
        <div style="color:#A5B4FC;font-size:0.78rem;">@{user['username']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    # Profile settings
    with st.sidebar.expander("⚙️ Profile Settings"):
        new_target = st.number_input(
            "Default daily target (kcal)",
            min_value=500, max_value=5000,
            value=user["default_target"], step=50,
            key="profile_target",
        )
        col1, col2 = st.columns(2)
        if col1.button("Save", use_container_width=True, key="save_profile"):
            db.update_default_target(user["id"], int(new_target))
            st.session_state["user"]["default_target"] = int(new_target)
            st.success("Saved!")
            st.rerun()

        st.markdown("**Change Password**")
        new_pw = st.text_input("New password", type="password", key="new_pw")
        if col2.button("Update", use_container_width=True, key="update_pw"):
            if len(new_pw) < 6:
                st.error("Min 6 characters")
            else:
                db.update_password(user["id"], new_pw)
                st.success("Password updated!")

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()
