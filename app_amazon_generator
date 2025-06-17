import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import json
import requests
from jinja2 import Template
import pdfkit
import time

# Initialize Faker and set random seed
fake = Faker()
np.random.seed(42)
random.seed(42)

# FastAPI endpoint (replace with your ngrok URL or server URL)
FASTAPI_URL = "http://localhost:8000/generate_product"  # Update with ngrok or server URL

# Create directories
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Function to generate Amazon-style Order ID
def generate_order_id():
    return f"{random.randint(100, 999)}-{random.randint(1000000, 9999999)}-{random.randint(1000000, 9999999)}"

# Function to generate ASIN
def generate_asin():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

# Function to fetch product from FastAPI
def fetch_product(amount: float, category: str) -> dict:
    try:
        response = requests.post(
            FASTAPI_URL,
            json={"amount": amount, "category": category},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching product from FastAPI: {e}")
        return {"product_name": "Default Product", "description": "Placeholder product"}

# Generate products
@st.cache_data
def generate_products(num_products=5):
    product_categories = ['electronics', 'home goods', 'beauty', 'clothing', 'outdoor gear']
    product_names = []
    seen_names = set()
    start_time = time.time()
    st.write("Generating product names...")
    progress_bar = st.progress(0)
    for i in range(num_products):
        category = random.choice(product_categories)
        product = fetch_product(0.0, category)
        product_name = product['product_name']
        if product_name not in seen_names:
            seen_names.add(product_name)
            product_names.append(product_name)
        progress_bar.progress((i + 1) / num_products)
    st.write(f"Generated {len(product_names)} products in {time.time() - start_time:.2f} seconds")
    return product_names

# Generate orders (same as original)
def generate_orders(n, product_names):
    orders = []
    for _ in range(n):
        order_id = generate_order_id()
        order_date = fake.date_time_between(start_date="-1y", end_date=datetime.now())
        customer_name = fake.name()
        customer_email = fake.email()
        shipping_address = fake.address().replace("\n", ", ")
        num_items = random.randint(1, 5)
        items = []
        subtotal = 0
        for _ in range(num_items):
            product_name = random.choice(product_names)
            asin = generate_asin()
            price = round(random.uniform(5.99, 199.99), 2)
            quantity = random.randint(1, 3)
            items.append({'product_name': product_name, 'asin': asin, 'price': price, 'quantity': quantity})
            subtotal += price * quantity
        shipping_method = random.choice(["Prime 2-Day", "Standard Shipping", "Expedited Shipping"])
        shipping_cost = 0 if shipping_method == "Prime 2-Day" else round(random.uniform(3.99, 12.99), 2)
        tax = round(subtotal * random.uniform(0.05, 0.1), 2)
        total = round(subtotal + shipping_cost + tax, 2)
        status = random.choice(["Pending", "Shipped", "Delivered"])
        delivery_date = order_date + timedelta(days=random.randint(1, 7)) if status == "Delivered" else None
        orders.append({
            'order_id': order_id,
            'order_date': order_date,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'shipping_address': shipping_address,
            'items': items,
            'subtotal': subtotal,
            'shipping_method': shipping_method,
            'shipping_cost': shipping_cost,
            'tax': tax,
            'total': total,
            'status': status,
            'delivery_date': delivery_date
        })
    return orders

# Generate invoices (same as original)
def generate_invoices(orders):
    invoices = []
    for order in orders:
        invoice_id = f"INV-{order['order_id'].split('-')[1]}"
        invoice_date = order['order_date'] + timedelta(days=random.randint(0, 2))
        billing_address = order['shipping_address']
        payment_method = random.choice(["Credit Card", "Amazon Pay", "Gift Card"])
        invoices.append({
            'invoice_id': invoice_id,
            'order_id': order['order_id'],
            'invoice_date': invoice_date,
            'customer_name': order['customer_name'],
            'billing_address': billing_address,
            'items': order['items'],
            'subtotal': order['subtotal'],
            'shipping_cost': order['shipping_cost'],
            'tax': order['tax'],
            'total': order['total'],
            'payment_method': payment_method
        })
    return invoices

# Flatten data (same as original)
def flatten_data(data, data_type):
    flattened = []
    for record in data:
        for item in record['items']:
            flat_record = {
                'id': record['order_id'] if data_type == 'orders' else record['invoice_id'],
                'order_id': record['order_id'],
                'date': record['order_date'] if data_type == 'orders' else record['invoice_date'],
                'customer_name': record['customer_name'],
                'address': record['shipping_address'] if data_type == 'orders' else record['billing_address'],
                'product_name': item['product_name'],
                'asin': item['asin'],
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': record['subtotal'],
                'shipping_cost': record['shipping_cost'],
                'tax': record['tax'],
                'total': record['total'],
                'status': record.get('status') if data_type == 'orders' else record['payment_method']
            }
            flattened.append(flat_record)
    return flattened

# HTML to PDF conversion
def html_to_pdf(html_path, pdf_path):
    try:
        config = pdfkit.configuration(wkhtmltopdf=r"/usr/bin/wkhtmltopdf")  # Adjust path for Streamlit Cloud
        pdfkit.from_file(html_path, pdf_path, configuration=config)
        return True
    except Exception as e:
        st.error(f"Error converting HTML to PDF: {e}")
        return False

# Streamlit UI
st.title("Amazon Order Generator")
num_products = st.slider("Number of unique products to generate", 1, 10, 5)
num_orders = st.slider("Number of orders to generate", 1, 50, 20)

if st.button("Generate Orders"):
    # Generate products
    product_names = generate_products(num_products)
    
    # Generate orders and invoices
    orders = generate_orders(num_orders, product_names)
    invoices = generate_invoices(orders)
    
    # Flatten and create DataFrames
    orders_flat = flatten_data(orders, 'orders')
    invoices_flat = flatten_data(invoices, 'invoices')
    orders_df = pd.DataFrame(orders_flat)
    invoices_df = pd.DataFrame(invoices_flat)
    
    # Save to CSV
    orders_df.to_csv('data/orders.csv', index=False)
    invoices_df.to_csv('data/invoices.csv', index=False)
    
    # Display DataFrames
    st.subheader("Sample Orders Data")
    st.dataframe(orders_df.head())
    st.subheader("Sample Invoices Data")
    st.dataframe(invoices_df.head())
    
    # Generate HTML and PDF for first order
    order = orders_df.iloc[0]
    delivery_date = order['date'] + timedelta(days=random.randint(1, 2))
    formatted_delivery_date = f"{delivery_date.strftime('%A, %B %d, %Y')} - {delivery_date.strftime('%A, %B %d, %Y')}"
    shipping_speed = "Express"
    
    with open('amazon_order_template.html', 'r') as f:
        html_template = Template(f.read())
    html_output = html_template.render(
        order_id=order['order_id'],
        customer_name=order['customer_name'],
        delivery_date=formatted_delivery_date,
        shipping_speed=shipping_speed,
        item_subtotal=f"${order['subtotal']:.2f}",
        shipping_handling=f"${order['shipping_cost']:.2f}",
        total_before_tax=f"${order['subtotal'] + order['shipping_cost']:.2f}",
        estimated_tax=f"${order['tax']:.2f}",
        order_total=f"${order['total']:.2f}"
    )
    
    html_path = 'output/order_confirmation.html'
    pdf_path = 'output/order_confirmation.pdf'
    with open(html_path, 'w') as f:
        f.write(html_output)
    
    if html_to_pdf(html_path, pdf_path):
        st.success(f"Generated {html_path} and {pdf_path}")
        with open(pdf_path, 'rb') as f:
            st.download_button("Download Order Confirmation PDF", f, file_name="order_confirmation.pdf")
    else:
        st.error("Failed to generate PDF")