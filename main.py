import streamlit as st
from PIL import Image, ImageDraw
import os

# Load preloaded image
IMAGE_PATH = "L4-Overview-1.jpg"  # Make sure this file is in the same directory
img = Image.open(IMAGE_PATH).convert("RGB")

st.set_page_config(page_title="Sand Marker", layout="wide")
st.title("🏖️ Sand Marker Web App")
st.caption("Click each cell to toggle between S (Sand) and NS (No Sand).")

rows, cols = 10, 10
cell_w = img.width // cols
cell_h = img.height // rows

# Draw base grid
grid_img = img.copy()
draw = ImageDraw.Draw(grid_img)
for i in range(1, cols):
    draw.line((i * cell_w, 0, i * cell_w, img.height), fill="black")
for j in range(1, rows):
    draw.line((0, j * cell_h, img.width, j * cell_h), fill="black")

# Initialize session state
if "marks" not in st.session_state:
    st.session_state.marks = {}

# UI Layout
col1, col2 = st.columns([2, 1])
with col1:
    st.image(grid_img, caption="Beach Image Grid", use_column_width=True)

# Interactive grid of buttons
s_count = 0
ns_count = 0

st.subheader("Mark the Squares")
for r in range(rows):
    cols_layout = st.columns(cols)
    for c in range(cols):
        key = f"{r}-{c}"
        val = st.session_state.marks.get((r, c), "")
        btn_label = val or " "
        if cols_layout[c].button(btn_label, key=key):
            current = st.session_state.marks.get((r, c))
            if current == "S":
                st.session_state.marks[(r, c)] = "NS"
            elif current == "NS":
                st.session_state.marks.pop((r, c))
            else:
                st.session_state.marks[(r, c)] = "S"

# Count S and NS
for v in st.session_state.marks.values():
    if v == "S":
        s_count += 1
    elif v == "NS":
        ns_count += 1

st.markdown(f"**S: {s_count}** &nbsp;&nbsp;&nbsp; **NS: {ns_count}**")

# Download button
if st.button("🎯 Download Marked Image"):
    marked_img = grid_img.copy()
    draw = ImageDraw.Draw(marked_img)
    for (r, c), v in st.session_state.marks.items():
        x = c * cell_w + cell_w // 2 - 10
        y = r * cell_h + cell_h // 2 - 10
        draw.text((x, y), v, fill="red")
    marked_img.save("marked_output.png")
    with open("marked_output.png", "rb") as f:
        st.download_button("Download PNG", f, file_name="marked_output.png", mime="image/png")
