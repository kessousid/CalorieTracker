import re
import streamlit as st
import database as db


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

    # ── Page layout ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
        .auth-title  { text-align:center; font-size:2.4rem; font-weight:700;
                       color:#667eea; margin-bottom:0; }
        .auth-sub    { text-align:center; color:#888; margin-bottom:1.5rem; }
        .auth-card   { background:#fff; border-radius:16px;
                       box-shadow:0 4px 24px rgba(102,126,234,.15);
                       padding:2rem 2.5rem; }
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<p class="auth-title">🥗 Calorie Tracker</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="auth-sub">Indian Vegetarian Edition &nbsp;·&nbsp; '
            '658 foods across 20 categories</p>',
            unsafe_allow_html=True,
        )

        st.warning(
            "**Disclaimer:** This app is a personal tool for tracking calorie consumption "
            "only. It does not constitute medical, nutritional, or dietary advice of any kind. "
            "The calorie values listed are approximate. I am not a dietician or food specialist. "
            "Please consult a qualified healthcare professional for personalised dietary guidance.",
            icon="⚠️",
        )

        with st.container():
            tab_login, tab_register = st.tabs(["🔐  Sign In", "📝  Create Account"])

            # ── Login ─────────────────────────────────────────────────────────
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

            # ── Register ──────────────────────────────────────────────────────
            with tab_register:
                with st.form("register_form", clear_on_submit=False):
                    name = st.text_input("Full Name", placeholder="Priya Sharma")
                    col_u, col_e = st.columns(2)
                    username_r = col_u.text_input("Username", placeholder="priya123")
                    email_r = col_e.text_input("Email", placeholder="priya@example.com")
                    col_p, col_c = st.columns(2)
                    password_r = col_p.text_input(
                        "Password", type="password", placeholder="Min 6 chars"
                    )
                    confirm_r = col_c.text_input(
                        "Confirm Password", type="password", placeholder="Same as above"
                    )
                    target_r = st.number_input(
                        "Daily Calorie Target (kcal)",
                        min_value=500, max_value=5000, value=2000, step=50,
                        help="Recommended: 1800–2200 kcal for average adult",
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
                            name, username_r, email_r, password_r, int(target_r)
                        )
                        if ok:
                            st.success(
                                "Account created! Switch to the Sign In tab to log in."
                            )
                        else:
                            st.error(msg)

    return None


def show_sidebar_user(user: dict):
    """Render user info and logout button in the sidebar."""
    st.sidebar.markdown(f"### 👤 {user['name']}")
    st.sidebar.caption(f"@{user['username']}  ·  {user['email']}")
    st.sidebar.divider()

    # Quick target update
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

        # Change password
        st.markdown("**Change Password**")
        new_pw = st.text_input("New password", type="password", key="new_pw")
        if col2.button("Update", use_container_width=True, key="update_pw"):
            if len(new_pw) < 6:
                st.error("Min 6 characters")
            else:
                db.update_password(user["id"], new_pw)
                st.success("Password updated!")

    if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()
