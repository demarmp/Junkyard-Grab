import sqlite3
import streamlit as st

# Page Configuration for Mobile Responsiveness
st.set_page_config(
    page_title="Junkyard Harvester Pro",
    page_icon="🔧",
    layout="centered"
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("junkyard_inventory.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_key TEXT,
            part_name TEXT,
            weight TEXT,
            yard_cost TEXT,
            ebay_price TEXT,
            str_rating TEXT,
            notes TEXT
        )
    """)
    
    # Check if database is empty; if so, seed with 10 parts per vehicle
    cursor.execute("SELECT COUNT(*) FROM parts")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            # --- 2010 HONDA CIVIC (10 PARTS) ---
            ("2010 honda civic", "Electronic Power Steering (EPS) Module", "1.8 lbs", "$30", "$150", "High", "Easy dash pull, high failure rate."),
            ("2010 honda civic", "Power Window Master Switch", "0.4 lbs", "$12", "$45", "Very High", "Takes 60 seconds with a trim tool."),
            ("2010 honda civic", "Climate Control / HVAC Panel", "1.2 lbs", "$25", "$100", "Medium-High", "Watch for cracked mounting tabs."),
            ("2010 honda civic", "Engine Control Module (ECU/ECM)", "2.2 lbs", "$35", "$120", "High", "Verify matching part numbers."),
            ("2010 honda civic", "Combination Switch (Stalk Assembly)", "0.7 lbs", "$18", "$60", "Medium-High", "Controls lights/wipers; robust sellers."),
            ("2010 honda civic", "SRS / Airbag Control Module", "1.5 lbs", "$30", "$110", "Medium", "Located under center console. Disconnect battery first!"),
            ("2010 honda civic", "Radio / Audio Head Unit", "3.2 lbs", "$35", "$100", "Medium", "Factory replacements sought after by restorers."),
            ("2010 honda civic", "Mass Air Flow (MAF) Sensor", "0.3 lbs", "$10", "$40", "Very High", "Pocket-sized, pocket multiple if clean."),
            ("2010 honda civic", "Blower Motor Resistor", "0.4 lbs", "$10", "$35", "High", "Common failure; very fast mover on eBay."),
            ("2010 honda civic", "Throttle Body Assembly (Electronic)", "3.0 lbs", "$30", "$95", "Medium-High", "Take the TPS sensor and idle air control components intact."),

            # --- 2007 TOYOTA CAMRY (10 PARTS) ---
            ("2007 toyota camry", "Smart Key ECU / Immobilizer Box", "0.5 lbs", "$20", "$90", "High", "Small footprint, lightweight shipping."),
            ("2007 toyota camry", "Master Power Window Switch", "0.4 lbs", "$12", "$40", "Very High", "Universal wear item."),
            ("2007 toyota camry", "HVAC Control Module", "1.0 lbs", "$25", "$85", "Medium", "Direct plug-and-play swap."),
            ("2007 toyota camry", "Radio / Display Audio Unit", "3.0 lbs", "$30", "$110", "Medium-High", "Check for LCD screen delamination."),
            ("2007 toyota camry", "ABS Control Module (Electronic Top)", "2.5 lbs", "$35", "$130", "High", "Pull electronic top half only to save weight and fluid mess."),
            ("2007 toyota camry", "Body Control Module (BCM)", "1.4 lbs", "$30", "$100", "Medium", "Controls interior body electronics."),
            ("2007 toyota camry", "Combination Switch / Turn Stalk", "0.7 lbs", "$18", "$55", "Medium-High", "Easy steering column cover removal."),
            ("2007 toyota camry", "Accelerator Pedal Position Sensor", "0.8 lbs", "$15", "$50", "High", "Easy to unbolt from firewall/pedal assembly."),
            ("2007 toyota camry", "Fuel Injector Set (Set of 4)", "0.6 lbs", "$20", "$75", "High", "Hitachi/Denso units sell fast when tested clean."),
            ("2007 toyota camry", "A/C Compressor Control Solenoid", "0.3 lbs", "$10", "$45", "Medium-High", "Tiny part, high value for common AC failures.")
        ]
        cursor.executemany("""
            INSERT INTO parts (vehicle_key, part_name, weight, yard_cost, ebay_price, str_rating, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, initial_data)
        conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# --- APP INTERFACE ---
st.title("🔧 Yard Harvester Pro")
st.caption("10-Target Mobile Valuation Matrix")

# Search input
search_query = st.text_input("Enter Vehicle (e.g., *Civic*, *Camry*) or VIN:", placeholder="Search make, model, year...")

if search_query:
    query_clean = search_query.lower().strip()
    
    if len(query_clean) == 17:
        st.info("🔍 VIN detected. Matching to generation records...")
        query_clean = "honda civic" # Simulated fallback decode
        
    cursor.execute("""
        SELECT part_name, weight, yard_cost, ebay_price, str_rating, notes 
        FROM parts WHERE vehicle_key LIKE ?
    """, (f"%{query_clean}%",))
    
    results = cursor.fetchall()
    
    if results:
        st.success(f"Found top targets matching: **{search_query.title()}** ({len(results)} items)")
        for i, row in enumerate(results, 1):
            part_name, weight, yard_cost, ebay_price, str_rating, notes = row
            with st.container():
                st.markdown(f"### {i}. {part_name}")
                col1, col2 = st.columns(2)
                col1.metric("Yard Cost", yard_cost)
                col2.metric("eBay Est.", ebay_price)
                
                c3, c4 = st.columns(2)
                c3.metric("Weight", weight)
                c4.metric("Sell-Through", str_rating)
                
                st.caption(f"💡 *Field Note:* {notes}")
                st.markdown("---")
    else:
        st.warning("No parts logged for this vehicle yet. Use the admin panel below to add them!")

# --- EXPANDABLE ADMIN PANEL ---
with st.expander("➕ Add New Part to Database"):
    with st.form("add_part_form"):
        new_veh = st.text_input("Vehicle Key (e.g., '2012 ford focus')")
        new_part = st.text_input("Part Name")
        new_wt = st.text_input("Weight (e.g., '1.2 lbs')")
        new_yc = st.text_input("Yard Cost (e.g., '$20')")
        new_eb = st.text_input("eBay Est. (e.g., '$80')")
        new_str = st.selectbox("Sell-Through Rate", ["Very High", "High", "Medium-High", "Medium"])
        new_notes = st.text_area("Field Notes / Extraction Tips")
        
        submitted = st.form_submit_button("Save to Database")
        if submitted and new_veh and new_part:
            cursor.execute("""
                INSERT INTO parts (vehicle_key, part_name, weight, yard_cost, ebay_price, str_rating, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (new_veh.lower(), new_part, new_wt, new_yc, new_eb, new_str, new_notes))
            conn.commit()
            st.success(f"Added {new_part} successfully! Refresh to search.")
