import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Junkyard Harvester Pro",
    page_icon="🚗",
    layout="centered"
)

def init_db():
    conn = sqlite3.connect("junkyard_inventory.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Drop old table to prevent persistent schema mismatches on Streamlit Cloud
    cursor.execute("DROP TABLE IF EXISTS parts")
    
    cursor.execute("""
        CREATE TABLE parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            part_name TEXT,
            location TEXT,
            weight TEXT,
            yard_cost TEXT,
            ebay_price TEXT,
            str_rating TEXT,
            notes TEXT,
            image_url TEXT
        )
    """)
    
    initial_data = [
        # --- TOYOTA ---
        ("toyota", "camry", "Master Power Window Switch", "Driver Door Panel", "0.4 lbs", "$12", "$40", "Very High (94%)", "Pop out trim bezel with plastic pry tool; disconnect wire harness.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("toyota", "camry", "Fuel Injector Set (Set of 4)", "Engine Intake Manifold", "0.6 lbs", "$20", "$75", "High (86%)", "Denso units; unbolt fuel rail carefully to avoid spilling fuel.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("toyota", "4runner", "Rear Hatch Lock Actuator", "Rear Tailgate Interior Panel", "1.2 lbs", "$25", "$90", "High (88%)", "Remove interior hatch trim panel; 3 bolts and electrical plug.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("toyota", "corolla", "Mass Air Flow (MAF) Sensor", "Air Intake Box", "0.3 lbs", "$10", "$45", "Very High (90%)", "2 small screws and electrical clip. Pocket-sized high seller.", "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400"),

        # --- HONDA ---
        ("honda", "civic", "Power Window Master Switch", "Driver Door Panel", "0.4 lbs", "$12", "$45", "Very High (92%)", "Takes 60 seconds with a plastic trim tool.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("honda", "civic", "Electronic Power Steering Module", "Under Lower Dash", "1.8 lbs", "$30", "$150", "High (81%)", "Easy dash access; high failure rate.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("honda", "accord", "Climate Control Panel", "Center Dash Console", "1.2 lbs", "$25", "$95", "High (80%)", "Watch for brittle plastic mounting tabs around bezel.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),

        # --- FORD ---
        ("ford", "f-150", "Master Window Switch Bezel", "Driver Door Armrest", "0.6 lbs", "$15", "$55", "Very High (93%)", "High-touch interior wear component. Pull straight up.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("ford", "f-150", "Trailer Brake Control Module", "Dashboard Lower Left", "0.5 lbs", "$25", "$90", "High (85%)", "Plug-and-play upgrade item sought after by truck owners.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("ford", "explorer", "HVAC Blend Door Actuator", "Behind Glove Box", "0.4 lbs", "$12", "$40", "High (78%)", "Deep dash component; requires stubby ratchet.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),

        # --- CHEVROLET ---
        ("chevrolet", "silverado", "Instrument Cluster Stepper Motors", "Dashboard Instrument Panel", "2.5 lbs", "$35", "$120", "Very High (91%)", "Gauges fail constantly across 99-06 models.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("chevrolet", "silverado", "Blower Motor Resistor & Pigtail", "Under Passenger Dash", "0.4 lbs", "$10", "$40", "High (84%)", "Melts frequently; clip wires with pigtail intact.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),

        # --- DODGE & RAM ---
        ("dodge", "ram", "Climate Control / HVAC Head Unit", "Center Dash Stack", "1.5 lbs", "$30", "$110", "Very High (88%)", "Knobs and button overlays wear out fast.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("ram", "1500", "Rotary Shifter Dial Module", "Center Console", "0.8 lbs", "$25", "$85", "High (82%)", "Pop center console trim ring.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),

        # --- JEEP ---
        ("jeep", "wrangler", "Tailgate Hinge & Hardware Set", "Rear Tailgate Exterior", "2.2 lbs", "$20", "$80", "Very High (94%)", "T20/T30 Torx bits needed; off-roaders replace rusted hinges.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("jeep", "wrangler", "Center Console Latch & Lid", "Center Armrest", "1.2 lbs", "$18", "$65", "High (87%)", "Plastic hinges break constantly under pressure.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),

        # --- BMW & MERCEDES & AUDI & PORSCHE & VW & SAAB ---
        ("bmw", "3 series", "Final Stage Blower Motor Resistor", "Passenger Footwell Under Dash", "0.5 lbs", "$20", "$75", "Very High (91%)", "E46/E90 climate control blower fix. T25 screw access.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("mercedes benz", "c-class", "Window Master Switch Console", "Driver Door Armrest", "0.5 lbs", "$20", "$75", "High (85%)", "Pry up gently from front edge.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("audi", "a4", "Headlight Switch Dial", "Dashboard Left Vent Pod", "0.4 lbs", "$15", "$50", "High (83%)", "Push in and turn right to release housing clip.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("porsche", "boxster", "Ignition Switch Electrical Basis", "Steering Column Base", "0.4 lbs", "$25", "$90", "High (82%)", "Common failure causing electrical gremlins.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("volkswagen", "jetta", "Headlight Switch with Fog Pull", "Dashboard Left Panel", "0.4 lbs", "$15", "$55", "High (84%)", "Classic euro-switch upgrade item.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("saab", "9-3", "SID Information Display Unit", "Top Center Dashboard", "1.0 lbs", "$35", "$125", "Very High (95%)", "Pixel failure makes working units highly coveted.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),

        # --- NISSAN & SUBARU & MAZDA & MITSUBISHI & HYUNDAI & ISUZU ---
        ("nissan", "altima", "Transmission Control Module (TCM)", "Engine Bay / Battery Tray Area", "1.5 lbs", "$40", "$150", "High (84%)", "Match part numbers exactly on metal casing.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("subaru", "outback", "Tailgate Hatch Release Switch", "Rear Liftgate Exterior Pad", "0.3 lbs", "$10", "$40", "Medium-High (75%)", "Rubber pad rots out; unplug from inside panel.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("mazda", "miata", "Pop-up Headlight Motor", "Front Engine Bay Corners", "2.0 lbs", "$25", "$90", "Very High (93%)", "3 mounting bolts and electrical connector.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("hyundai", "sonata", "Steering Wheel Clock Spring", "Behind Steering Wheel", "0.6 lbs", "$20", "$70", "High (81%)", "Disconnect battery 15 mins prior to airbag removal.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("isuzu", "trooper", "4WD Shift Control Unit", "Center Dash / Kick Panel", "1.0 lbs", "$20", "$75", "Medium-High (76%)", "Plug-and-play module for 4x4 engagement.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("mitsubishi", "lancer", "Blower Motor Assembly", "Passenger Under-Dash", "3.0 lbs", "$25", "$85", "High (79%)", "3 screws holding motor housing underneath glovebox.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),

        # --- LEXUS & ACURA & JAGUAR & BENTLEY & ASTON MARTIN & MG & DATSUN & CHRYSLER & GMC ---
        ("lexus", "is300", "Mark Levinson Audio Amplifier", "Trunk Left Side Panel", "4.0 lbs", "$40", "$160", "Very High (92%)", "Valuable premium audio component; check for water intrusion.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("acura", "tl", "Bluetooth Hands-Free (HFL) Unit", "Upper Passenger Roof Console", "0.5 lbs", "$20", "$80", "High (86%)", "Pry down overhead map light console.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("jaguar", "s-type", "Climate Control Display Panel", "Center Dashboard Stack", "1.2 lbs", "$30", "$100", "High (78%)", "Wood grain trim bezel pulls straight out.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("bentley", "continental gt", "Center Dash Switch Assembly", "Center Console", "1.5 lbs", "$75", "$350", "Very High (95%)", "Specialized trim removal tools required.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("aston martin", "vantage", "Center Console Switch Pack", "Center Dashboard", "1.0 lbs", "$60", "$280", "Very High (90%)", "Rare boutique switch cluster.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("mg", "mgb", "Dashboard Toggle Switches", "Center Dashboard Panel", "0.2 lbs", "$8", "$30", "High (88%)", "Classic chrome bezel retaining nuts.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400"),
        ("datsun", "240z", "Quarter Vent Window Latches", "Rear Quarter Glass Pillars", "0.4 lbs", "$15", "$65", "Very High (94%)", "Highly sought-after vintage restoration hardware.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400"),
        ("chrysler", "300", "Smart Key Ignition Fobik Module", "Steering Column Switch", "0.5 lbs", "$20", "$75", "High (82%)", "Ignition bezel module clip-in.", "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=400"),
        ("gmc", "sierra", "Tailgate Handle with Backup Camera", "Tailgate Exterior", "1.0 lbs", "$20", "$75", "Medium-High (77%)", "Torx screws from inside tailgate access panel.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400")
    ]
    
    cursor.executemany("""
        INSERT INTO parts (make, model, part_name, location, weight, yard_cost, ebay_price, str_rating, notes, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, initial_data)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

st.title("🚗 Yard Harvester Pro")
st.markdown("Enter vehicle information below to pull top-selling parts, locations, and removal tips.")

# Structured Input Fields for Year, Make, Model
col1, col2, col3 = st.columns(3)
with col1:
    year_val = st.text_input("Year", placeholder="e.g. 2010")
with col2:
    make_val = st.text_input("Make", placeholder="e.g. Toyota")
with col3:
    model_val = st.text_input("Model", placeholder="e.g. Camry")

if st.button("Search Top Parts & Locations", type="primary"):
    if make_val and model_val:
        make_clean = make_val.lower().strip()
        model_clean = model_val.lower().strip()
        
        # Query matching make and model or flexible wildcard
        cursor.execute("""
            SELECT part_name, location, weight, yard_cost, ebay_price, str_rating, notes, image_url 
            FROM parts WHERE (make LIKE ? AND model LIKE ?) OR make LIKE ?
        """, (f"%{make_clean}%", f"%{model_clean}%", f"%{make_clean}%"))
        
        results = cursor.fetchall()
        
        if results:
            vehicle_title = f"{year_val} {make_val} {model_val}".strip().title()
            st.success(f"Top High-STR Parts & Locations for: **{vehicle_title}**")
            for i, row in enumerate(results[:10], 1):
                part_name, location, weight, yard_cost, ebay_price, str_rating, notes, image_url = row
                with st.container():
                    st.markdown(f"### {i}. {part_name}")
                    
                    img_col, info_col = st.columns([1, 2])
                    with img_col:
                        if image_url:
                            st.image(image_url)
                    with info_col:
                        st.markdown(f"📍 **Location:** `{location}`")
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Yard Cost", yard_cost)
                        c2.metric("eBay Est.", ebay_price)
                        c3.metric("Weight", weight)
                        c4.metric("Sell-Through", str_rating)
                    
                    st.caption(f"🔧 *Removal & Field Notes:* {notes}")
                    st.markdown("---")
        else:
            st.warning(f"No specific records found for '{make_val} {model_val}'. Try searching makes like Toyota, Ford, Honda, BMW, Jeep, or Chevrolet.")
    else:
        st.error("Please fill in at least the Make and Model fields.")
