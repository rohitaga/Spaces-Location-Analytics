import streamlit as st

def show():
    st.title("Trust and Security")

    st.write("""
    Streamlit is a framework that turns Python scripts into interactive apps, giving data scientists the ability to quickly create data and model-based apps for the entire company.
    """)

    st.subheader('Product Security 🔐')
    st.write("""
    - SSO: All access and sign-ins to Streamlit are conducted via an SSO provider: GitHub and GSuite. We do not store customer passwords.
    - Credential Storage: We encrypt sensitive customer data (e.g. secrets, authentication tokens) at-rest with AES256 as described in Google's documentation.
    - Permissions and Role-Based Access Control: Our permission levels inherit from the permissions you have assigned in GitHub. Users with write access to a GitHub repository for a given app will be able to make changes in the Streamlit administrative console.
    """)


    st.subheader('Network and Application Security 🌐')
    st.write("""
    - Data Hosting: Our physical infrastructure is hosted and managed within Google Cloud Platform (GCP) using their secure data centers. Streamlit leverages many of the platform's built-in security, privacy, and redundancy features. GCP continually monitors its data centers for risk and undergoes assessments to ensure compliance with industry standards. GCP's data centers have numerous accreditations, including ISO-27001, SOC 1 and SOC 2.
    - Virtual Private Cloud: All of our servers are within a virtual private cloud (VPC) with firewalls and network access control lists (ACLs) to allow external access to a select few API endpoints; all other internal services are only accessible within the VPC.
    - Encryption: All Streamlit apps are served entirely over HTTPS. All data sent to or from Streamlit over the public internet is encrypted in transit using 256-bit encryption. Our API and application endpoints are TLS only (v1.2). We use only strong cipher suites and HTTP Strict Transport Security (HSTS) to ensure browsers interact with Streamlit apps over HTTPS. We also encrypt data at rest using AES-256.
    """)

    st.subheader('Ongoing Operations 🚦')
    st.write("""
    - Incident Response: We have an internal protocol for handling security events which includes escalation procedures, rapid mitigation, and documented post-mortems. We notify customers promptly and publicize security advisories at [Streamlit Advisories](https://streamlit.io/advisories).
    - Penetration Testing: Streamlit uses third-party security tools to scan for vulnerabilities on a regular basis. Our security partners conduct periodic, intensive penetration tests on the Streamlit platform. Our product development team immediately responds to any identified issues or potential vulnerabilities to ensure the quality and security of Streamlit applications.
    """)

    st.subheader('Security and Compliance Programs 📚')
    st.write("""
    - People: All Streamlit employees go through a thorough background check before hiring. We take a least-privilege approach to the access and handling of data. While we retain a minimal amount of customer data and limit internal access on a need-to-know basis, all employees are required to review related security policies and are trained on proper data handling to ensure they uphold our strict commitment to the privacy and security of your data. All employees sign a confidentiality agreement before they start at Streamlit.
    - Vulnerability Control: We keep our systems up-to-date with the latest security patches and continuously monitor for new vulnerabilities through compliance and security mailing lists. This includes automatic scanning of our code repositories for vulnerable dependencies.
    """)

    st.write("""
    Note: If you have further questions about Streamlit Trust and Security, please reach out to us on the [Streamlit Community Forum](https://discuss.streamlit.io/). 💬
    """)