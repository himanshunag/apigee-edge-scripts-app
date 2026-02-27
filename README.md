# Streamlit Apigee X Project

This project is a Streamlit application that allows users to create resources in Apigee X using Node.js scripts. The application provides an interface for managing Key Value Maps (KVMs), keystores, and references.

## Project Structure

```
streamlit-apigee-x
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   └── scripts
│       ├── create_kvm.js     # Script to create a Key Value Map (KVM)
│       ├── add_kvm_values.js  # Script to add values to an existing KVM
│       ├── create_keystore.js # Script to create a keystore
│       └── create_reference.js # Script to create a reference
├── requirements.txt           # Python dependencies for the Streamlit application
├── package.json               # Node.js configuration and dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd streamlit-apigee-x
   ```

2. **Install Python dependencies:**
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies:**
   Ensure you have Node.js installed, then run:
   ```
   npm install
   ```

## Usage

To run the Streamlit application, execute the following command in the terminal:
```
streamlit run src/app.py
```

## Available Scripts

- **Create KVM:** Use the `create_kvm.js` script to create a new Key Value Map in Apigee X.
- **Add KVM Values:** Use the `add_kvm_values.js` script to add values to an existing KVM.
- **Create Keystore:** Use the `create_keystore.js` script to create a new keystore in Apigee X.
- **Create Reference:** Use the `create_reference.js` script to create a new reference in Apigee X.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.