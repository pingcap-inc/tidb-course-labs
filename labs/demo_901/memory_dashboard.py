"""
mem9 Memory Dashboard - Streamlit App
Visualize, search, and manage AI agent memories.
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from mem9_client import Mem9Client

st.set_page_config(page_title="mem9 Memory Dashboard", layout="wide")

# Title
st.title("🧠 mem9 Memory Dashboard")
st.markdown("Visualize and manage persistent memory for AI agents.")

# Sidebar for API key
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input(
    "MEM9 API Key",
    type="password",
    value=os.getenv("MEM9_API_KEY", ""),
    help="Get your API key from https://mem9.ai",
)

# Initialize client
if not api_key:
    st.info("👈 Enter your mem9 API key in the sidebar to get started.")
    st.markdown("""
    ### How to get your API key
    1. Go to [mem9.ai](https://mem9.ai)
    2. Sign up for a free account
    3. Copy your API key from the dashboard
    4. Paste it in the sidebar 👈
    """)
    st.stop()

try:
    client = Mem9Client(api_key=api_key)
except ValueError as e:
    st.error(str(e))
    st.stop()

# Tab layout
tab1, tab2, tab3 = st.tabs(["📋 All Memories", "🔍 Search", "➕ Add Memory"])

# ===== Tab 1: Browse all memories =====
with tab1:
    st.subheader("All Stored Memories")

    col1, col2 = st.columns([1, 1])
    with col1:
        limit = st.slider("Memories per page", min_value=5, max_value=50, value=20)
    with col2:
        refresh = st.button("🔄 Refresh")

    with st.spinner("Fetching memories..."):
        memories = client.list_memories(limit=limit)

    if memories:
        df = pd.DataFrame(memories)
        st.dataframe(
            df,
            column_config={
                "id": st.column_config.TextColumn("ID", width="small"),
                "content": st.column_config.TextColumn("Content", width="large"),
                "tags": st.column_config.ListColumn("Tags"),
                "source": st.column_config.TextColumn("Source", width="small"),
                "created_at": st.column_config.DatetimeColumn("Created", width="small"),
            },
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"Showing {len(memories)} memories")
    else:
        st.info("No memories found. Go to the 'Add Memory' tab to create your first memory!")

# ===== Tab 2: Search =====
with tab2:
    st.subheader("🔍 Search Memories")

    query = st.text_input("Search query", placeholder="e.g., TiDB architecture, agent preferences...")
    search_limit = st.slider("Max results", 1, 20, 5)

    if st.button("Search", type="primary"):
        if query:
            with st.spinner("Searching..."):
                results = client.search_memories(query, limit=search_limit)

            if results:
                st.success(f"Found {len(results)} results")
                for i, r in enumerate(results, 1):
                    with st.expander(f"Result {i}: {r.get('content', '')[:80]}..."):
                        st.json(r)
            else:
                st.info("No matching memories found.")
        else:
            st.warning("Please enter a search query.")

# ===== Tab 3: Add memory =====
with tab3:
    st.subheader("➕ Add New Memory")

    with st.form("add_memory_form"):
        content = st.text_area(
            "Memory Content",
            placeholder="What does your agent need to remember?",
            height=150,
        )
        tags_input = st.text_input(
            "Tags (comma-separated)",
            placeholder="tidb, architecture, preference",
        )
        source = st.text_input("Source", value="dashboard", placeholder="e.g., chat, code, manual")
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("💾 Save Memory", type="primary")

    if submitted:
        if not content:
            st.warning("Please enter memory content.")
        else:
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            with st.spinner("Saving..."):
                result = client.add_memory(
                    content=content,
                    tags=tags,
                    source=source,
                )
            st.success("✅ Memory saved successfully!")
            with st.expander("View saved memory"):
                st.json(result)

# Stats footer
st.divider()
st.caption(f"Powered by mem9.ai · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
