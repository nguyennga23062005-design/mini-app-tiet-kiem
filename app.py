import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 1. Cấu hình trang và chèn hình ảnh ở đầu App
st.set_page_config(page_title="App Tính Lãi Tiết Kiệm", layout="centered")

try:
    # Đọc và hiển thị banner ở đầu ứng dụng
    img = Image.open("banner.jpg")
    st.image(img, use_container_width=True)
except FileNotFoundError:
    st.warning("Mẹo: Thêm file 'banner.jpg' vào cùng thư mục để hiển thị banner đẹp mắt nhé!")

# 2. Tiêu đề ứng dụng
st.title("💰 Ứng Dụng Tính Lãi Suất Tiết Kiệm Ngân Hàng")
st.write("Sáng tạo bởi: Nhóm 4 Sinh Viên")

st.markdown("---")

# 3. Giao diện nhập liệu (Sidebar hoặc Giao diện chính)
st.header("📋 Nhập thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_goc = st.number_input("Số tiền gửi ban đầu (VNĐ):", min_value=0.0, value=10000000.0, step=500000.0, format="%.0f")
    lai_suat_nam = st.number_input("Lãi suất gửi (% / năm):", min_value=0.0, value=6.0, step=0.1)

with col2:
    ky_han_thang = st.number_input("Kỳ hạn gửi (tháng):", min_value=1, value=12, step=1)
    loai_lai = st.selectbox("Phương thức tính lãi:", ["Lãi kép (Tích lũy gốc)", "Lãi đơn"])

# Tỷ lệ lãi suất theo kỳ hạn (tháng)
r_thang = (lai_suat_nam / 100) / 12

# 4. Xử lý thuật toán tài chính
# Lập bảng chi tiết qua từng tháng để vẽ biểu đồ
cac_thang = np.arange(0, ky_han_thang + 1)
dong_tien = []

if loai_lai == "Lãi đơn":
    # Công thức lãi đơn theo tháng: Gốc + (Gốc * r_thang * t)
    for t in cac_thang:
        tien_thoi_diem_t = so_tien_goc + (so_tien_goc * r_thang * t)
        dong_tien.append(tien_thoi_diem_t)
    tong_tien_cuoi_ky = dong_tien[-1]
    tien_lai = tong_tien_cuoi_ky - so_tien_goc
else:
    # Công thức lãi kép theo tháng: Gốc * (1 + r_thang)^t
    for t in cac_thang:
        tien_thoi_diem_t = so_tien_goc * ((1 + r_thang) ** t)
        dong_tien.append(tien_thoi_diem_t)
    tong_tien_cuoi_ky = dong_tien[-1]
    tien_lai = tong_tien_cuoi_ky - so_tien_goc

# 5. Hiển thị kết quả ra màn hình
st.markdown("### 📊 Kết quả tính toán cuối kỳ")
c1, c2, c3 = st.columns(3)
c1.metric(label="Tiền Gốc Ban Đầu", value=f"{so_tien_goc:,.0f} VNĐ")
c2.metric(label="Tiền Lãi Nhận Được", value=f"{tien_lai:,.0f} VNĐ", delta=f"{loai_lai}")
c3.metric(label="Tổng Số Tiền Cuối Kỳ", value=f"{tong_tien_cuoi_ky:,.0f} VNĐ")

st.markdown("---")

# 6. Tính năng nâng cao: Biểu đồ tăng trưởng dòng tiền
st.subheader("📉 Biểu đồ tăng trưởng tài sản qua các tháng")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(cac_thang, dong_tien, marker='o', color='#1E88E5', linewidth=2, label="Số dư tài khoản")
ax.fill_between(cac_thang, dong_tien, so_tien_goc, color='#1E88E5', alpha=0.1)
ax.set_xlabel("Tháng")
ax.set_ylabel("Số tiền (VNĐ)")
ax.set_title("Sự thay đổi của tổng tiền (Gốc + Lãi) theo thời gian")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

st.pyplot(fig)

# 7. Tính năng nâng cao: Bảng dữ liệu chi tiết
st.subheader("📋 Bảng lịch trình tăng trưởng chi tiết")
df_chi_tiet = pd.DataFrame({
    "Tháng": cac_thang,
    "Tổng Số Tiền (VNĐ)": [f"{x:,.0f}" for x in dong_tien]
})
st.dataframe(df_chi_tiet, use_container_width=True)
