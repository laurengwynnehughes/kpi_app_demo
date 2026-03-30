import time
import streamlit as st

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="KPIs for Mobilisation and Support Work Packages through Transition",
    layout="wide"
)

st.title("KPIs for Mobilisation and Support Work Packages through Transition")
st.caption("Demo control panel to refresh KPI data (Databricks Jobs) and open role-specific dashboards (Power BI).")

# ----------------------------
# Sidebar controls (keeps main page clean)
# ----------------------------
with st.sidebar:
    st.header("Run Controls")

    quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

    site = st.selectbox(
        "Site",
        ["All Sites", "Sellafield", "SLF01", "SLF02", "SLF03", "SLF04", "SLF05", "SLF06", "SLF07", "SLF08", "SLF09"],
        index=1
    )

    end_user_view = st.radio(
        "End User View",
        ["Information Managers", "Project Managers", "Commercial Managers"],
        index=1
    )

    st.divider()

    demo_mode = st.toggle("Demo mode (no Databricks connection)", value=True)

    st.caption("Demo mode simulates job submission and completion.")


# ----------------------------
# Power BI links (replace with your real links)
# ----------------------------
POWER_BI_LINKS = {
    "Information Managers": "https://powerbi.com/groups/<group>/reports/<report>?pageName=InformationManagers",
    "Project Managers": "https://powerbi.com/groups/<group>/reports/<report>?pageName=ProjectManagers",
    "Commercial Managers": "https://powerbi.com/groups/<group>/reports/<report>?pageName=CommercialManagers",
}

# ----------------------------
# Databricks job trigger (stub for now)
# ----------------------------
def trigger_databricks_job(selected_quarter: str, selected_site: str) -> dict:
    """
    Demo stub. Replace the internals later with a real Databricks Jobs API call.

    Return structure is intentionally close to what a real submission might return.
    """
    # Simulate a job submission
    time.sleep(1.0)
    return {
        "submitted": True,
        "run_id": f"demo-{selected_site}-{selected_quarter}-{int(time.time())}",
        "message": "Job submitted (demo mode)."
    }


def poll_job_status(run_id: str) -> dict:
    """
    Demo stub job status polling.
    """
    # Simulate "Running" then "Completed"
    time.sleep(0.8)
    return {"run_id": run_id, "state": "RUNNING", "progress": 50}
    

# ----------------------------
# Main layout
# ----------------------------
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("What you are about to run")

    st.write(
        {
            "Quarter": quarter,
            "Site": site,
            "Dashboard view": end_user_view,
            "Mode": "Demo (simulated)" if demo_mode else "Live (Databricks)"
        }
    )

    st.markdown("### Actions")

    run_btn = st.button("Run KPI Refresh", type="primary")
    open_btn = st.button("Open Dashboard")

    st.markdown("---")
    st.markdown("### Job Status")

    # keep job state in session
    if "last_run" not in st.session_state:
        st.session_state.last_run = None

    if run_btn:
        st.info("Submitting KPI refresh job…")

        if demo_mode:
            result = trigger_databricks_job(quarter, site)
            st.session_state.last_run = {
                "run_id": result["run_id"],
                "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "quarter": quarter,
                "site": site,
                "state": "SUBMITTED",
            }
            st.success(f"{result['message']} (Run ID: {result['run_id']})")

            # Simulate progress
            status = poll_job_status(result["run_id"])
            st.session_state.last_run["state"] = status["state"]

            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                progress.progress(i)

            st.session_state.last_run["state"] = "COMPLETED"
            st.success("Job completed. KPI tables are updated (demo).")

        else:
            st.warning("Live mode selected — next step is wiring Databricks Jobs API credentials.")
            st.stop()

    # Render last run info if available
    if st.session_state.last_run:
        lr = st.session_state.last_run
        st.write(
            {
                "Run ID": lr["run_id"],
                "Submitted at": lr["submitted_at"],
                "Quarter": lr["quarter"],
                "Site": lr["site"],
                "State": lr["state"],
            }
        )
    else:
        st.caption("No job run yet. Click **Run KPI Refresh** to submit a run.")

with col2:
    st.subheader("Dashboard Shortcut")
    st.write("Open the Power BI view tailored to the selected end user.")

    link = POWER_BI_LINKS[end_user_view]
    st.markdown(f"**Selected view:** {end_user_view}")
    st.markdown(f"{link}")

    st.markdown("---")
    st.subheader("Demo Notes")
    st.write(
        "- This app is a *control panel* (run refresh + route users to the right dashboard).\n"
        "- KPI calculations and RAG logic live in Databricks.\n"
        "- Power BI reads curated Gold tables.\n"
    )

    if open_btn:
        st.success("Use the dashboard link above to open the role-specific view.")