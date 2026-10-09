import sqlite3
import streamlit as st

# Page Configuration for Mobile Responsiveness
st.set_page_config(
    page_title="Junkyard Harvester Pro",
    page_icon="⚡",
    layout="centered"
)

# --- AUTOMATED DATABASE SETUP & HIGH-STR SEEDING ---
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
    
    # Check if database is empty; if so, populate pre-vetted High-STR matrices
    cursor.execute("SELECT COUNT(*) FROM parts")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            # --- 2006-2011 HONDA CIVIC (TOP 10 HIGH-STR) ---
            ("honda civic", "Power Window Master Switch", "0.4 lbs", "$12", "$45", "Very High (92%)", "Takes 60 seconds with a plastic trim tool. Zero shipping hassle."),
            ("honda civic", "Mass Air Flow (MAF) Sensor", "0.3 lbs", "$10", "$40", "Very High (88%)", "Pocket-sized, highly reliable electronics seller."),
            ("honda civic", "Electronic Power Steering (EPS) Module", "1.8 lbs", "$30", "$150", "High (81%)", "Easy dash access; high failure rate in this generation."),
            ("honda civic", "Blower Motor Resistor", "0.4 lbs", "$10", "$35", "High (79%)", "Extremely common failure; lightning-fast mover online."),
            ("honda civic", "Engine Control Module (ECU/ECM)", "2.2 lbs", "$35", "$120", "High (75%)", "Always match exact numbers on the metal case casing."),
            ("honda civic", "Climate Control / HVAC Panel", "1.2 lbs", "$25", "$100", "Medium-High (68%)", "Watch out for brittle mounting tabs when popping out bezel."),
            ("honda civic", "Combination Switch (Stalk Assembly)", "0.7 lbs", "$18", "$60", "Medium-High (65%)", "Controls lights and wipers; robust seasonal demand."),
            ("honda civic", "Throttle Body Assembly (Electronic)", "3.0 lbs", "$30", "$95", "Medium-High (64%)", "Take sensors intact; do not damage connector pins."),
            ("honda civic", "Radio / Audio Head Unit", "3.2 lbs", "$35", "$100", "Medium (58%)", "Factory units sought after by owners reverting custom stereos."),
            ("honda civic", "SRS / Airbag Control Module", "1.5 lbs", "$30", "$110", "Medium (55%)", "Located under center console. Disconnect battery first!"),

            # --- 2007-2011 TOYOTA CAMRY (TOP 10 HIGH-STR) ---
            ("toyota camry", "Master Power Window Switch", "0.4 lbs", "$12", "$40", "Very High (94%)", "Universal wear item across multiple trim configurations."),
            ("toyota camry", "Fuel Injector Set (Set of 4)", "0.6 lbs", "$20", "$75", "High (86%)", "Denso units sell instantly when cleaned and flow-tested."),
            ("toyota camry", "Smart Key ECU / Immobilizer Box", "0.5 lbs", "$20", "$90", "High (82%)", "Tiny footprint, high-dollar security module replacement."),
            ("toyota camry", "Accelerator Pedal Position Sensor", "0.8 lbs", "$15", "$50", "High (78%)", "2 bolts under the dash; lightweight and ships flat-rate."),
            ("toyota camry", "ABS Control Module (Electronic Top)", "2.5 lbs", "$35", "$130", "High (74%)", "Unbolt electronic top half only to avoid brake-fluid mess."),
            ("toyota camry", "A/C Compressor Control Solenoid", "0.3 lbs", "$10", "$45", "Medium-High (70%)", "Tiny part, heavy demand during summer months."),
            ("toyota camry", "Combination Switch / Turn Stalk", "0.7 lbs", "$18", "$55", "Medium-High (66%)", "Easy steering column shroud removal."),
            ("toyota camry", "HVAC Control Module", "1.0 lbs", "$25", "$85", "Medium-High (63%)", "Direct plug-and-play dashboard swap element."),
            ("toyota camry", "Body Control Module (BCM)", "1.4 lbs", "$30", "$100", "Medium (59%)", "Controls interior body electronics and lighting architecture."),
            ("toyota camry", "Radio / Display Audio Unit", "3.0 lbs", "$30", "$110", "Medium (54%)", "Inspect screen carefully for thermal delamination lines.")
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
st.title("⚡ Yard Harvester Pro")
st.caption("Automated High-STR Vehicle Matrix")

# Quick selector chips or Search box
search_query = st.text_input("Enter Vehicle Make/Model:", placeholder="e.g., Civic, Camry...")

# Quick-filter helper buttons
st.markdown("**Quick Select Pre-Loaded Targets:**")
col_a, col_b = st.columns(2)
if col_a.button("🚗 Honda Civic"):
    search_query = "honda civic"
if col_b.button("🚙 Toyota Camry"):
    search_query = "toyota camry"

if search_query:
    query_clean = search_query.lower().strip()
    
    cursor.execute("""
        SELECT part_name, weight, yard_cost, ebay_price, str_rating, notes 
        FROM parts WHERE vehicle_key LIKE ?
    """, (f"%{query_clean}%",))
    
    results = cursor.fetchall()
    
    if results:
        st.success(database_msg := f"Top 10 Highest-STR Ranked Parts for: **{search_query.title()}**")
        for i, row in enumerate(results, 1):
            part_name, weight, yard_cost, ebay_price, str_rating, notes = row
            with st.container():
                st.markdown(f"### {i}. {part_name}")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Yard", yard_cost)
                c2.metric("eBay Est.", ebay_price)
                c3.metric("Weight", weight)
                c4.metric("Sell-Through", str_rating)
                
                st.caption(f"💡 *Field Note:* {notes}")
                st.markdown("---")
    else:
        st.warning("Vehicle model not found in the instant database yet.")
