import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Barcode BG Remover", page_icon="🏷️")

st.title("🏷️ Barcode Background Remover")
st.write("Upload your Code 128 or Barcode image, and we will remove the white background for you.")

# File uploader allowing multiple files
uploaded_files = st.file_uploader("Choose image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Open the image
        img = Image.open(uploaded_file).convert("RGBA")
        datas = img.getdata()
        new_data = []

        # Process pixels: Make white transparent
        for item in datas:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item) # Keep black

        img.putdata(new_data)

        # Save to a buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display the result and a download button
        st.image(img, caption=f"Processed: {uploaded_file.name}", use_column_width=True)
        st.download_button(
            label=f"Download {uploaded_file.name}",
            data=byte_im,
            file_name=f"Transparent_{uploaded_file.name}",
            mime="image/png"
        )
