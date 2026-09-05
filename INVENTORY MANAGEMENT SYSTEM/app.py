# Import required libraries
import streamlit as st
import pandas as pd

# Configure Streamlit page title and responsive layout
st.set_page_config(
    page_title="Inventory Management App",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------------
# 1. STATE INITIALIZATION & DATA STORE
# ---------------------------------------------------------
# Initialize session state to maintain inventory records across page reloads
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"Item ID": "101", "Item Name": "Laptops", "Category": "Electronics", "Quantity": 15, "Unit Price ($)": 800},
        {"Item ID": "102", "Item Name": "Desk Chairs", "Category": "Furniture", "Quantity": 5, "Unit Price ($)": 150},
        {"Item ID": "103", "Item Name": "Wireless Mice", "Category": "Electronics", "Quantity": 40,
         "Unit Price ($)": 25},
        {"Item ID": "104", "Item Name": "Notebooks", "Category": "Stationery", "Quantity": 8, "Unit Price ($)": 5}
    ])

# Reference the active dataframe from session state
df = st.session_state.inventory

# ---------------------------------------------------------
# 2. APPLICATION HEADER
# ---------------------------------------------------------
st.title("📦 Inventory Management System")
st.caption("Track stock levels, add new items, and receive low-stock alerts.")
st.markdown("---")

# ---------------------------------------------------------
# 3. METRICS & KPI DASHBOARD
# ---------------------------------------------------------
# Compute real-time inventory summary calculations
total_items = len(df)
total_quantity = df["Quantity"].sum()
total_value = (df["Quantity"] * df["Unit Price ($)"]).sum()
low_stock_count = len(df[df["Quantity"] < 10])

# Display metrics side-by-side using Streamlit columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Unique Products", total_items)
col2.metric("Total Items in Stock", total_quantity)
col3.metric("Total Inventory Value", f"${total_value:,.2f}")
col4.metric("Low Stock Alerts (<10)", low_stock_count, delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------
# 4. SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("Manage Inventory")
action = st.sidebar.radio(
    "Select Action",
    ["View Inventory", "Add New Product", "Update Quantity"]
)

# ---------------------------------------------------------
# 5. ACTION HANDLERS
# ---------------------------------------------------------

# Option A: View Inventory and Filter by Category
if action == "View Inventory":
    st.subheader("Current Stock Table")

    # Filter dropdown configuration
    categories = ["All"] + list(df["Category"].unique())
    selected_cat = st.selectbox("Filter by Category", categories)

    # Filter dataset based on selected category
    if selected_cat != "All":
        filtered_df = df[df["Category"] == selected_cat]
    else:
        filtered_df = df

    # Render interactive data table
    st.dataframe(filtered_df, use_container_width=True)

    # Automated Alert system for stock falling below minimum threshold (10 units)
    low_stock_items = df[df["Quantity"] < 10]
    if not low_stock_items.empty:
        st.warning("⚠️ **Low Stock Warning for the following items:**")
        st.table(low_stock_items[["Item ID", "Item Name", "Quantity"]])

# Option B: Add New Product Form
elif action == "Add New Product":
    st.subheader("➕ Add Product to Inventory")

    # Form layout to handle user input efficiently
    with st.form("add_item_form", clear_on_submit=True):
        item_id = st.text_input("Item ID (e.g., 105)")
        item_name = st.text_input("Item Name")
        category = st.selectbox("Category", ["Electronics", "Furniture", "Stationery", "Other"])
        quantity = st.number_input("Initial Quantity", min_value=0, step=1)
        price = st.number_input("Unit Price ($)", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("Save Item")

        # Form validation and processing on submit button click
        if submitted:
            if item_id and item_name:
                new_row = {
                    "Item ID": item_id,
                    "Item Name": item_name,
                    "Category": category,
                    "Quantity": int(quantity),
                    "Unit Price ($)": float(price)
                }
                # Append new item row to session state dataframe
                st.session_state.inventory = pd.concat(
                    [st.session_state.inventory, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                st.success(f"Added {item_name} successfully!")
                st.rerun()
            else:
                st.error("Please fill in Item ID and Item Name.")

# Option C: Modify Existing Product Stock Level
elif action == "Update Quantity":
    st.subheader("🔄 Update Stock Levels")

    # Dropdown populated with existing item names
    selected_item = st.selectbox("Select Item", df["Item Name"].tolist())
    new_qty = st.number_input("New Quantity", min_value=0, step=1)

    # Update state upon confirmation
    if st.button("Update Stock"):
        st.session_state.inventory.loc[
            st.session_state.inventory["Item Name"] == selected_item, "Quantity"
        ] = int(new_qty)
        st.success(f"Updated quantity for {selected_item} to {new_qty}!")
        st.rerun()