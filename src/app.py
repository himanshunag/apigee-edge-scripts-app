import streamlit as st
import subprocess
import json

st.set_page_config(
    page_title="Forgecrux - Apigee Edge Management",
    layout="wide"
)

# Initialize session state for configuration and token storage
if "config" not in st.session_state:
    st.session_state.config = {
        "org_name": "financialdataexchange",
        "env_name": "dev",
        "username": "prakat@financialdataexchange.org",
        "password": ""
    }
if "show_config_form" not in st.session_state:
    st.session_state.show_config_form = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Custom CSS for Orange & Green theme
st.markdown("""
    <style>
        /* Primary theme colors */
        :root {
            --primary-orange: #FF8C00;
            --light-green: #E8F5E9;
            --dark-green: #2E7D32;
            --light-orange: #FFE0CC;
            --dark-blue: #030729;
        }
        
        /* Global text color */
        body, p, span, div, label {
            color: #030729 !important;
        }
        
        /* All text elements */
        * {
            color: #030729 !important;
        }
        
        /* Markdown text */
        [data-testid="stMarkdownContainer"] {
            color: #030729 !important;
        }
        
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div {
            color: #030729 !important;
        }
        
        /* Headers styling */
        h1, h2, h3, h4, h5, h6 {
            color: #030729 !important;
        }
        
        /* Buttons styling */
        .stButton > button {
            background-color: #FF8C00 !important;
            color: white !important;
            border-radius: 8px !important;
            border: 2px solid #FF8C00 !important;
            font-weight: bold !important;
            transition: 0.3s !important;
        }
        
        .stButton > button:hover {
            background-color: #2E7D32 !important;
            border-color: #2E7D32 !important;
        }
        
        /* Input fields styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            border: 2px solid #FF8C00 !important;
            border-radius: 6px !important;
            background: linear-gradient(135deg, #FFE0CC 0%, #E8F5E9 100%) !important;
            color: #030729 !important;
        }
        
        .stTextInput > label,
        .stTextArea > label {
            color: #030729 !important;
            font-weight: bold !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] button {
            color: #030729 !important;
            border-bottom: 3px solid transparent !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px !important;
        }
        
        [data-baseweb="tab-list"] button:hover {
            color: #030729 !important;
            border-color: #FF8C00 !important;
        }
        
        [aria-selected="true"] {
            color: #030729 !important;
            border-color: #FF8C00 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(90deg, #FFC966 0%, #81C784 100%) !important;
            border-right: 3px solid #FF8C00 !important;
        }
        
        /* Radio buttons */
        .stRadio > label > div {
            color: #030729 !important;
        }
        
        .stRadio > label > div > input[type="radio"] {
            accent-color: #FF8C00 !important;
        }
        
        /* Dividers */
        hr {
            border-color: #FF8C00 !important;
        }
        
        /* Container and cards background */
        .stContainer {
            background-color: #FFFFFF !important;
        }
        
        /* Main content background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(90deg, #FFC966 0%, #81C784 100%) !important;
        }
        
        [data-testid="stMain"] {
            background: linear-gradient(90deg, #FFC966 0%, #81C784 100%) !important;
        }
        
        body {
            background: linear-gradient(90deg, #FFC966 0%, #81C784 100%) !important;
        }
        
        /* Focus styles */
        input:focus,
        textarea:focus {
            border-color: #2E7D32 !important;
            box-shadow: 0 0 5px #2E7D32 !important;
        }
        
        /* Success message styling */
        .success {
            background-color: #E8F5E9 !important;
            border-left: 5px solid #2E7D32 !important;
        }
        
        /* Hide settings button and toolbar */
        [data-testid="baseButton-secondary"] {
            display: none !important;
        }
        
        /* Hide entire toolbar */
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Hide top right menu buttons */
        .stAppHeader button {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar branding
col1, col2 = st.sidebar.columns([1, 2])
with col1:
    st.image("src/forgecruxlogo.png", width=50)
with col2:
    st.markdown("### Forgecrux Company")
st.sidebar.markdown("---")

# Configure Button
if st.sidebar.button("⚙️ Configure"):
    st.session_state.show_config_form = not st.session_state.show_config_form

# Configuration Form
if st.session_state.show_config_form:
    st.sidebar.markdown("### Configuration")
    with st.sidebar.form("config_form"):
        org_name = st.text_input(
            "Edge Organization Name",
            value=st.session_state.config["org_name"],
            placeholder="e.g., myorg",
            disabled=True
        )
        env_name = st.text_input(
            "Environment Name",
            value=st.session_state.config["env_name"],
            placeholder="e.g., prod",
            disabled=True
        )
        username = st.text_input(
            "Username",
            value=st.session_state.config["username"],
            placeholder="Your Apigee username",
            disabled=True
        )
        password = st.text_input(
            "Password",
            value=st.session_state.config["password"],
            type="password",
            placeholder="Your Apigee password"
        )
        
        if st.form_submit_button("💾 Save Configuration"):
            st.session_state.config["org_name"] = org_name
            st.session_state.config["env_name"] = env_name
            st.session_state.config["username"] = username
            st.session_state.config["password"] = password
            st.sidebar.success("✅ Configuration saved successfully!")
            # hide form after saving
            st.session_state.show_config_form = False
    
    st.sidebar.markdown("---")

# Get Access Token Button
if st.sidebar.button("🔑 Get Access Token"):
    # fetch credentials from session state configuration
    user = st.session_state.config.get("username")
    pwd = st.session_state.config.get("password")
    if not user or not pwd:
        st.sidebar.error("Please configure username and password first.")
    else:
        # run script and capture output
        result = subprocess.run(
            ["node", "src/scripts/access_token.js", user, pwd],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            try:
                token_data = json.loads(result.stdout)
                access_token = token_data.get("access_token")
                if access_token:
                    st.session_state.access_token = access_token
                    st.sidebar.success("Access token received and stored in session.")
                    st.sidebar.code(result.stdout)
                else:
                    st.sidebar.error("Token response did not contain access_token field.")
                    st.sidebar.code(result.stdout)
            except Exception as e:
                st.sidebar.error("Received output but failed to parse token.")
                st.sidebar.text(result.stdout)
        else:
            st.sidebar.error("Failed to obtain access token.")
            st.sidebar.text(result.stderr)

# Sidebar navigation
st.sidebar.markdown("### Resources")
selected_resource = st.sidebar.radio(
    "Select Resource",
    ["KVM", "Keystore", "Reference"],
    label_visibility="collapsed"
)

st.markdown("<h2 style='font-size: 40px;'>Forgecrux - Apigee Edge Resource Management</h2>", unsafe_allow_html=True)

# KVM Resource
if selected_resource == "KVM":
    st.header("Key Value Map (KVM)")
    
    tab1, tab2 = st.tabs(["Create KVM", "Add Values to KVM"])
    
    with tab1:
        st.subheader("Create Key Value Map")
        kvm_name = st.text_input("Enter KVM Name:")
        kvm_desc = st.text_input("Description (optional):")
        kvm_encrypted = st.checkbox("Encrypted", value=False)
        
        # Initialize rows for KVM creation entries
        if "kvm_create_rows" not in st.session_state:
            st.session_state.kvm_create_rows = [{"key": "", "value": ""}]

        def add_create_row():
            st.session_state.kvm_create_rows.append({"key": "", "value": ""})

        st.markdown("**Add Key-Value Pairs (optional):**")
        # render rows as two columns per row
        for i, row in enumerate(st.session_state.kvm_create_rows):
            c1, c2, c3 = st.columns([3, 3, 1])
            with c1:
                k = st.text_input(f"Key {i+1}", value=row.get("key", ""), key=f"kvm_create_key_{i}")
            with c2:
                v = st.text_input(f"Value {i+1}", value=row.get("value", ""), key=f"kvm_create_value_{i}")
            with c3:
                if st.button("Remove", key=f"remove_kvm_create_{i}"):
                    st.session_state.kvm_create_rows.pop(i)
                    st.experimental_rerun()
            # keep session_state in sync
            st.session_state.kvm_create_rows[i]["key"] = st.session_state.get(f"kvm_create_key_{i}")
            st.session_state.kvm_create_rows[i]["value"] = st.session_state.get(f"kvm_create_value_{i}")

        st.button("Add Row", on_click=add_create_row, key="add_kvm_create_row")
        
        if st.button("Create KVM"):
            org = st.session_state.config.get("org_name")
            env = st.session_state.config.get("env_name")
            token = st.session_state.get("access_token")
            if not org or not env or not token:
                st.error("Please configure org/env and fetch access token before creating a KVM.")
            else:
                # prepare entry array from rows
                entries = []
                for r in st.session_state.kvm_create_rows:
                    name = (r.get("key") or "").strip()
                    value = (r.get("value") or "").strip()
                    if name:  # only add non-empty keys
                        entries.append({"name": name, "value": value})
                
                # pass the entire array as a single JSON argument to the Node script
                entries_json = json.dumps(entries) if entries else "[]"
                # convert boolean to lowercase string for CLI
                enc_arg = "true" if kvm_encrypted else "false"
                result = subprocess.run(
                    ["node", "src/scripts/create_kvm.js", org, kvm_name, env, kvm_desc, enc_arg, entries_json, token],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    st.success("KVM created successfully. See response below:")
                    st.code(result.stdout)
                else:
                    st.error("Failed to create KVM. See error output below:")
                    st.text(result.stderr)
    
    with tab2:
        st.subheader("Add Values to KVM")
        kvm_to_update = st.text_input("Enter KVM Name to Update:")

        # initialize rows
        if "kvm_rows" not in st.session_state:
            st.session_state.kvm_rows = [{"key": "", "value": ""}]

        def add_row():
            st.session_state.kvm_rows.append({"key": "", "value": ""})

        # render rows as two columns per row
        for i, row in enumerate(st.session_state.kvm_rows):
            c1, c2, c3 = st.columns([3, 3, 1])
            with c1:
                k = st.text_input(f"Key {i+1}", value=row.get("key", ""), key=f"kvm_key_{i}")
            with c2:
                v = st.text_input(f"Value {i+1}", value=row.get("value", ""), key=f"kvm_value_{i}")
            with c3:
                if st.button("Remove", key=f"remove_kvm_{i}"):
                    st.session_state.kvm_rows.pop(i)
                    st.experimental_rerun()
            # keep session_state in sync
            st.session_state.kvm_rows[i]["key"] = st.session_state.get(f"kvm_key_{i}")
            st.session_state.kvm_rows[i]["value"] = st.session_state.get(f"kvm_value_{i}")

        st.button("Add Row", on_click=add_row)

        if st.button("Save Values to KVM"):
            org = st.session_state.config.get("org_name")
            env = st.session_state.config.get("env_name")
            token = st.session_state.get("access_token")
            if not org or not env or not token:
                st.error("Please configure org/env and fetch access token before updating a KVM.")
            else:
                # prepare values as JSON strings for CLI
                args = []
                for r in st.session_state.kvm_rows:
                    name = (r.get("key") or "").strip()
                    value = (r.get("value") or "").strip()
                    if name:
                        args.append({"name": name, "value": value})
                if not args:
                    st.error("Please provide at least one key.")
                else:
                    # pass the entire array as a single JSON argument to the Node script
                    json_arg = json.dumps(args)
                    result = subprocess.run(
                        ["node", "src/scripts/add_kvm_values.js", org, kvm_to_update, env, token, json_arg],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        st.success("Values saved to KVM. See response below:")
                        st.code(result.stdout)
                    else:
                        st.error("Failed to save values to KVM. See error output below:")
                        st.text(result.stderr)

# Keystore Resource
elif selected_resource == "Keystore":
    st.header("Keystores")
    
    st.subheader("Create Keystore")
    keystore_name = st.text_input("Enter Keystore Name:")
    if st.button("Create Keystore"):
        org = st.session_state.config.get("org_name")
        env = st.session_state.config.get("env_name")
        token = st.session_state.get("access_token")
        if not org or not env or not token:
            st.error("Please configure organization, environment, and fetch access token before creating a keystore.")
        else:
            subprocess.run(["node", "src/scripts/create_keystore.js", org, keystore_name, env, token])

# Reference Resource
elif selected_resource == "Reference":
    st.header("References")
    
    st.subheader("Create Reference")
    reference_name = st.text_input("Enter Reference Name:")
    reference_value = st.text_input("Enter Reference Value:")
    if st.button("Create Reference"):
        org = st.session_state.config.get("org_name")
        env = st.session_state.config.get("env_name")
        token = st.session_state.get("access_token")
        if not org or not env or not token:
            st.error("Please configure org/env and fetch access token before creating a reference.")
        else:
            subprocess.run(["node", "src/scripts/create_reference.js", org, env, reference_name, reference_value, token])

# Footer branding
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #FF8C00 0%, #2E7D32 100%); border-radius: 10px; margin: 20px 0;'>
        <p style='color: white; font-weight: bold; margin: 0;'> Powered by <strong>Forgecrux Company</strong></p>
        <p style='color: #FFE0CC; margin: 5px 0; font-size: 0.9em;'>Apigee X Resource Management Platform</p>
    </div>
    """, unsafe_allow_html=True)