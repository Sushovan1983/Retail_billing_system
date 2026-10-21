
import streamlit as st

# -------------------------------
# Function to calculate discount
# -------------------------------
def manager(offer):
    return lambda total_mrp: total_mrp * (100 - offer) / 100


# -------------------------------
# Login credentials
# -------------------------------
userid_m = "manager@12"
password_m = "manager@123"

userid_cashier = "cashier@12"
password_cashier = "cashier@123"


# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Billing System",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 Store Billing System")
st.write("Manager and Cashier Billing Portal")

st.divider()


# -------------------------------
# Session state initialization
# -------------------------------
if "offer" not in st.session_state:
    st.session_state.offer = 0.0

if "manager_logged_in" not in st.session_state:
    st.session_state.manager_logged_in = False

if "cashier_logged_in" not in st.session_state:
    st.session_state.cashier_logged_in = False

if "products" not in st.session_state:
    st.session_state.products = []


# -------------------------------
# Manager Login Section
# -------------------------------
st.header("👨‍💼 Manager Login")

with st.form("manager_login_form"):
    userid_login_m = st.text_input("Enter Manager User ID")
    password_login_m = st.text_input(
        "Enter Manager Password",
        type="password"
    )

    manager_login = st.form_submit_button("Manager Login")

if manager_login:
    if (
        userid_login_m == userid_m
        and password_login_m == password_m
    ):
        st.session_state.manager_logged_in = True
        st.success("Manager login successful!")
    else:
        st.error("Incorrect manager user ID or password.")

if st.session_state.manager_logged_in:
    st.success("Manager authenticated.")

    with st.form("offer_form"):
        offer = st.number_input(
            "Enter Today's Offer (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.offer),
            step=1.0
        )

        save_offer = st.form_submit_button("Save Offer")

    if save_offer:
        st.session_state.offer = offer
        st.success(f"Today's offer set to {offer}%")

st.divider()


# -------------------------------
# Cashier Login Section
# -------------------------------
st.header("🧾 Cashier Login")

with st.form("cashier_login_form"):
    userid_login_cashier = st.text_input("Enter Cashier User ID")
    password_login_cashier = st.text_input(
        "Enter Cashier Password",
        type="password"
    )

    cashier_login = st.form_submit_button("Cashier Login")

if cashier_login:
    if (
        userid_login_cashier == userid_cashier
        and password_login_cashier == password_cashier
    ):
        st.session_state.cashier_logged_in = True
        st.success("Cashier login successful. Billing can start!")
    else:
        st.error(
            "Incorrect cashier user ID or password. "
            "Billing cannot be started."
        )


# -------------------------------
# Billing Section
# -------------------------------
if st.session_state.cashier_logged_in:

    st.divider()
    st.header("🛍️ Product Billing")

    st.info(f"Current offer: {st.session_state.offer}%")

    with st.form("product_form", clear_on_submit=True):
        price = st.number_input(
            "Enter Item Price (₹)",
            min_value=0.01,
            value=100.0,
            step=10.0
        )

        quantity = st.number_input(
            "Enter Quantity",
            min_value=1,
            value=1,
            step=1
        )

        add_product = st.form_submit_button("Add Product")

    if add_product:
        st.session_state.products.append({
            "Price (₹)": price,
            "Quantity": quantity,
            "Total (₹)": price * quantity
        })
        st.success("Product added successfully!")

    # Display product list
    if st.session_state.products:
        st.subheader("Product List")

        st.dataframe(
            st.session_state.products,
            use_container_width=True,
            hide_index=True
        )

        total_mrp = sum(
            product["Total (₹)"]
            for product in st.session_state.products
        )

        discount = total_mrp * st.session_state.offer / 100

        billing_formula = manager(st.session_state.offer)
        total_payable = billing_formula(total_mrp)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total MRP", f"₹{total_mrp:.2f}")

        with col2:
            st.metric("Discount", f"₹{discount:.2f}")

        st.success(
            f"### Total Amount Payable: ₹{total_payable:.2f}"
        )

        if st.button("Complete Billing"):
            st.session_state.last_bill = {
                "Total MRP": total_mrp,
                "Discount": discount,
                "Amount Payable": total_payable
            }
            st.session_state.products = []
            st.success("Billing completed successfully!")

    else:
        st.info("No products added yet.")

    if st.button("Clear Current Bill"):
        st.session_state.products = []
        st.rerun()
