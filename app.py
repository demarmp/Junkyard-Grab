import sqlite3
import streamlit as st

# Page Configuration for Mobile Responsiveness
st.set_page_config(
    page_title="Junkyard Harvester Pro",
    page_icon="⚡",
    layout="centered"
)

# --- AUTOMATED DATABASE SETUP & MASSIVE MULTI-BRAND SEEDING ---
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
    
    # Check if database is empty; if so, populate pre-vetted High-STR matrices for requested brands
    cursor.execute("SELECT COUNT(*) FROM parts")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            # --- FORD ---
            ("ford f-150", "Master Window Switch Bezel", "0.6 lbs", "$15", "$55", "Very High (93%)", "High-touch interior wear component."),
            ("ford f-150", "Trailer Brake Control Module", "0.5 lbs", "$25", "$90", "High (85%)", "Dash integrated module; plug-and-play upgrade item."),
            ("ford explorer", "Rear Liftgate Lock Actuator", "1.1 lbs", "$20", "$75", "High (82%)", "High failure rate on SUV tailgates."),
            
            # --- CHEVY ---
            ("chevy silverado", "Instrument Cluster Stepper Motors / Assembly", "2.5 lbs", "$35", "$120", "Very High (91%)", "Gauges fail constantly across 99-06 models."),
            ("chevy tahoe", "Blower Motor Resistor & Pigtail", "0.4 lbs", "$10", "$40", "High (84%)", "Melts frequently; clip wires with pigtail intact."),
            ("chevy cruze", "Coolant Thermostat Housing / Outlet", "0.8 lbs", "$12", "$45", "High (80%)", "Plastic housing cracks under thermal stress."),

            # --- DODGE ---
            ("dodge ram", "Climate Control / HVAC Head Unit", "1.5 lbs", "$30", "$110", "Very High (88%)", "Knobs and button overlays wear out fast."),
            ("dodge charger", "Window Switch Master Assembly", "0.5 lbs", "$15", "$50", "High (83%)", "Easy door panel pull with trim tool."),

            # --- CHRYSLER ---
            ("chryser 300", "Smart Key Ignition Fobik / Module", "0.4 lbs", "$20", "$85", "High (79%)", "High-demand security integration part."),
            ("chrysler town & country", "Stow 'n Go Seat Latch Lever / Cable", "0.8 lbs", "$15", "$60", "Medium-High (72%)", "Snaps under heavy family cargo use."),

            # --- BUICK ---
            ("buick lesabre", "Series II 3.8L Ignition Control Module (ICM)", "1.8 lbs", "$25", "$80", "Very High (87%)", "Bulletproof engine module; highly sought after."),
            ("buick enclave", "Liftgate Module", "1.2 lbs", "$30", "$120", "High (75%)", "Rear electronics module prone to moisture failure."),

            # --- INTERNATIONAL ---
            ("international scout", "Mechanical Fuel Pump / Carb Linkage Parts", "1.0 lbs", "$20", "$75", "High (85%)", "Vintage restoration goldmine; grab any clean brackets."),
            ("international harvester", "Vintage Instrument Gauge Cluster", "3.5 lbs", "$45", "$180", "Very High (90%)", "Extremely rare collector find."),

            # --- OLDSMOBILE ---
            ("oldsmobile cutlass", "Tail Light Lens Assembly", "2.0 lbs", "$25", "$95", "High (82%)", "Classic restoration demand is steady."),
            ("oldsmobile alero", "Blinker / Multi-Function Switch", "0.7 lbs", "$15", "$55", "Medium-High (70%)", "Steering column stalk replacement."),

            # --- GMC ---
            ("gmc sierra", "Tailgate Handle with Backup Camera", "1.0 lbs", "$20", "$75", "Very High (89%)", "Direct swap upgrade for base models."),
            ("gmc acadia", "Headlight Control Switch", "0.4 lbs", "$12", "$45", "High (78%)", "Dash dimmer dial wears out."),

            # --- RAM ---
            ("ram 1500", "Rotary Shifter Dial Module (Electronic)", "0.8 lbs", "$35", "$140", "Very High (92%)", "Modern electronic dial upgrade/replacement."),
            ("ram 2500", "Cummins Grid Heater Solenoid", "1.2 lbs", "$25", "$90", "High (86%)", "Heavy duty diesel electrical component."),

            # --- JEEP ---
            ("jeep cherokee", "PCM / Engine Computer (XJ)", "2.5 lbs", "$35", "$125", "Very High (91%)", "Legendary straight-six dry solder joint demand."),
            ("jeep wrangler", "Tailgate Hinge & Hardware Set", "2.2 lbs", "$20", "$80", "Very High (94%)", "Off-roaders constantly replace rusted hardware."),

            # --- MAZDA ---
            ("mazda miata", "Pop-up Headlight Motor / Relay", "2.0 lbs", "$25", "$90", "Very High (93%)", "Massive cult-following restoration market."),
            ("mazda 3", "Climate Control Panel", "1.0 lbs", "$20", "$70", "High (77%)", "Dash center stack module."),

            # --- DATSUN ---
            ("datsun 240z", "Vintage Dash Switches & Knobs", "0.3 lbs", "$15", "$65", "Very High (95%)", "Extremely high collector value for restoration."),
            ("datsun 620", "Quarter Vent Window Latch Assembly", "0.2 lbs", "$10", "$50", "High (88%)", "Hard-to-find vintage truck trim piece."),

            # --- NISSAN ---
            ("nissan altima", "Transmission Control Module (TCM)", "1.5 lbs", "$40", "$150", "High (84%)", "High failure rate item; match part numbers."),
            ("nissan frontier", "Tailgate Finisher / Handle", "1.2 lbs", "$20", "$65", "Medium-High (73%)", "Sun-faded replacement part."),

            # --- KIA ---
            ("kia sorento", "Window Master Switch", "0.4 lbs", "$12", "$45", "High (81%)", "Common driver door wear item."),
            ("kia soul", "Radio / Display Head Unit", "3.0 lbs", "$30", "$100", "Medium-High (70%)", "Factory swap unit."),

            # --- SUZUKI ---
            ("suzuki samurai", "Transfer Case Lower Gears / Shifter Boot", "1.0 lbs", "$20", "$85", "Very High (90%)", "Off-road crawler aftermarket demand."),
            ("suzuki grand vitara", "4WD Switch Selector Panel", "0.3 lbs", "$15", "$55", "Medium (68%)", "Dash button cluster."),

            # --- MITSUBISHI ---
            ("mitsubishi lancer", "Evo-Style Wing / Trunk Trim", "4.0 lbs", "$40", "$150", "High (85%)", "Enthusiast cosmetic upgrade part."),
            ("mitsubishi outlander", "A/C Blower Motor", "2.2 lbs", "$20", "$70", "Medium-High (72%)", "Passenger footwell quick pull."),

            # --- SUBARU ---
            ("subaru outback", "Head Gaskets / Multi-Layer Steel Set (Used Core)", "3.0 lbs", "$15", "$50", "High (83%)", "Boxer engine rebuild core components."),
            ("subaru impreza", "Intercooler Core (Turbo Models)", "5.0 lbs", "$50", "$180", "Very High (90%)", "Wrx/STI top-mount core goldmine."),

            # --- VW ---
            ("volkswagen jetta", "Window Regulator & Motor Assembly", "3.5 lbs", "$25", "$85", "Very High (92%)", "Infamous cable snap failure point; huge seller."),
            ("volkswagen golf", "Headlight Switch with Fog Pull", "0.4 lbs", "$15", "$55", "High (84%)", "Classic euro-switch upgrade item."),

            # --- BMW ---
            ("bmw 3 series", "Final Stage Resistor (Blower Motor)", "0.5 lbs", "$20", "$75", "Very High (91%)", "E46/E90 climate control blower fix."),
            ("bmw 5 series", "ABS Hydraulic Pump Control Module", "3.0 lbs", "$50", "$200", "High (82%)", "Valuable electronic module rebuild core."),

            # --- MERCEDES BENZ ---
            ("mercedes c-class", "Window Master Switch Console", "0.5 lbs", "$25", "$95", "High (86%)", "Center console wood/plastic switch plate."),
            ("mercedes e-class", "Instrument Cluster Display Screen", "2.0 lbs", "$40", "$160", "High (80%)", "Pixel failure replacement market."),

            # --- SAAB ---
            ("saab 9-3", "SID (Trionic Information Display) Unit", "0.8 lbs", "$30", "$120", "Very High (94%)", "Pixel dropout is universal; easy dash pull."),
            ("saab 9-5", "DI (Direct Ignition) Cassette", "4.5 lbs", "$45", "$150", "Very High (92%)", "Essential roadside spare for Saab enthusiasts.")
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
st.caption("Multi-Brand High-STR Valuation Matrix")

# Search input box
search_query = st.text_input("Enter Vehicle Make/Model:", placeholder="e.g., Ford, BMW, Saab, Wrangler, Datsun...")

if search_query:
    query_clean = search_query.lower().strip()
    
    cursor.execute("""
        SELECT part_name, weight, yard_cost, ebay_price, str_rating, notes 
        FROM parts WHERE vehicle_key LIKE ?
    """, (f"%{query_clean}%",))
    
    results = cursor.fetchall()
    
    if results:
        st.success(f"Top High-STR Ranked Parts for: **{search_query.title()}**")
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
        st.warning("No pre-loaded parts found for this specific keyword. Use the admin tool below to add it instantly!")

# --- BUILT-IN ADMIN PANEL TO ADD ANY CUSTOM VEHICLE/PART ON THE FLY ---
with st.expander("➕ Add New Vehicle / Part to Database"):
    with st.form("add_custom_part"):
        c_veh = st.text_input("Vehicle Make & Model (e.g., 'saab 9-3' or 'datsun 240z')")
        c_part = st.text_input("Part Name")
        c_wt = st.text_input("Weight (e.g., '1.5 lbs')")
        c_yc = st.text_input("Yard Cost (e.g., '$20')")
        c_eb = st.text_input("eBay Est. (e.g., '$90')")
        c_str = st.selectbox("Sell-Through Rating", ["Very High", "High", "Medium-High", "Medium"])
        c_notes = st.text_area("Field Notes / Tips")
        
        submitted = st.form_submit_button("Save to Database")
        if submitted and c_veh and c_part:
            cursor.execute("""
                INSERT INTO parts (vehicle_key, part_name, weight, yard_cost, ebay_price, str_rating, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (c_veh.lower(), c_part, c_wt, c_yc, c_eb, c_str, c_notes))
            conn.commit()
            st.success(f"Successfully added {c_part} for {c_veh}! Search for it above.")
