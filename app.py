import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Intermountain OEM Parts - Profit Calculator",
    page_icon="💰",
    layout="centered"
)

def init_db():
    conn = sqlite3.connect("junkyard_profit.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS haul_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_name TEXT,
            vehicle TEXT,
            list_price REAL,
            yard_cost REAL,
            ebay_fees REAL,
            fixed_fees REAL,
            net_profit REAL,
            roi REAL,
            status TEXT
        )
    """)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

st.title("💰 Intermountain OEM Parts - Profit Calculator")
st.markdown("Automated calculations incorporating your fixed yard admission ($1.00), handling ($0.94), shipping materials ($1.25), and eBay fees (13.25% + $0.30).")

# --- INPUT SECTION FOR NEW PART ---
with st.form("add_part_form", clear_on_submit=True):
    st.subheader("Add Part to Weekend Haul List")
    
    col1, col2 = st.columns(2)
    with col1:
        part_name = st.text_input("Part Name", placeholder="e.g. Master Window Switch")
        vehicle = st.text_input("Vehicle / Model", placeholder="e.g. 2013 Honda Odyssey")
    with col2:
        list_price = st.number_input("Expected eBay List Price ($)", min_value=0.0, format="%.2f", value=50.0)
        yard_cost = st.number_input("Junkyard Part Cost ($)", min_value=0.0, format="%.2f", value=12.0)
    
    submitted = st.form_submit_button("Calculate & Add to List", type="primary")
    if submitted:
        if part_name and vehicle:
            # Automated fixed constants
            admission_fee = 1.00
            handling_fee = 0.94
            shipping_materials = 1.25
            fixed_overhead = admission_fee + handling_fee + shipping_materials  # $3.19 total
            
            # Automated eBay fee formula (13.25% + $0.30)
            ebay_fees = (list_price * 0.1325) + 0.30
            
            total_costs = yard_cost + ebay_fees + fixed_overhead
            net_profit = list_price - total_costs
            roi = (net_profit / total_costs * 100) if total_costs > 0 else 0.0
            
            cursor.execute("""
                INSERT INTO haul_list (part_name, vehicle, list_price, yard_cost, ebay_fees, fixed_fees, net_profit, roi, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (part_name, vehicle, list_price, yard_cost, ebay_fees, fixed_overhead, net_profit, roi, "To Grab"))
            conn.commit()
            st.success(f"Added **{part_name}**! Net Profit: **${net_profit:.2f}** ({roi:.1f}% ROI)")
            st.rerun()
        else:
            st.error("Please fill in the Part Name and Vehicle fields.")

st.markdown("---")

# --- DASHBOARD & HAUL LIST ---
st.subheader("🎯 Upcoming Weekend Haul List")

# Safe schema check if upgrading from an older database version
try:
    cursor.execute("SELECT id, part_name, vehicle, list_price, yard_cost, ebay_fees, fixed_fees, net_profit, roi, status FROM haul_list")
    rows = cursor.fetchall()
except sqlite3.OperationalError:
    cursor.execute("DROP TABLE IF EXISTS haul_list")
    conn.commit()
    st.rerun()

if rows:
    total_revenue = sum(row[3] for row in rows)
    total_yard_cost = sum(row[4] for row in rows)
    total_ebay_fees = sum(row[5] for row in rows)
    total_fixed_fees = sum(row[6] for row in rows)
    total_profit = sum(row[7] for row in rows)
    total_all_costs = total_yard_cost + total_ebay_fees + total_fixed_fees
    overall_roi = (total_profit / total_all_costs * 100) if total_all_costs > 0 else 0.0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Est. Revenue", f"${total_revenue:.2f}")
    m2.metric("Total All-In Costs", f"${total_all_costs:.2f}")
    m3.metric("Total Net Profit", f"${total_profit:.2f}")
    m4.metric("Overall ROI", f"{overall_roi:.1f}%")
    
    st.markdown("### Itemized Breakdown")
    
    for row in rows:
        row_id, p_name, veh, l_price, y_cost, e_fees, f_fees, n_prof, r_val, status = row
        
        with st.container():
            col_info, col_metrics, col_action = st.columns([2, 3, 1])
            with col_info:
                st.markdown(f"**{p_name}**")
                st.caption(f"🚗 {veh}")
            with col_metrics:
                st.markdown(f"List: **${l_price:.2f}** | Yard: **${y_cost:.2f}**")
                st.markdown(f"Fees (eBay: ${e_fees:.2f} | Fixed Overhead: ${f_fees:.2f})")
                st.markdown(f"Profit: **<span style='color:green;'>${n_prof:.2f}</span>** ({r_val:.1f}% ROI)", unsafe_allow_html=True)
            with col_action:
                if st.button("Delete", key=f"del_{row_id}"):
                    cursor.execute("DELETE FROM haul_list WHERE id = ?", (row_id,))
                    conn.commit()
                    st.rerun()
            st.markdown("---")
            
    if st.button("🗑️ Clear Entire List", type="secondary"):
        cursor.execute("DELETE FROM haul_list")
        conn.commit()
        st.rerun()
else:
    st.info("Your haul list is currently empty. Use the form above to log parts during your weekday research.")
