import streamlit as st
import pandas as pd

# 页面设置，和你加州housing例子风格对齐
st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")
st.title("Global Superstore Sales Dashboard by Xinyi Chen")
st.subheader("See more filters in the sidebar:")

# 读取你的xls，工作表Orders
df = pd.read_excel("Global Superstore.xls", sheet_name="Orders")

# ========== 侧边栏筛选区 ==========
st.sidebar.header("Filters")

# 1. 地区筛选
region_options = sorted(df["Region"].unique())
select_region = st.sidebar.multiselect("Select Region", region_options, default=region_options)

# 2. 产品大类筛选
cat_options = sorted(df["Category"].unique())
select_cat = st.sidebar.multiselect("Select Category", cat_options, default=cat_options)

# 3. Sales销售额滑块（和你截图里面房价Minimal滑块一模一样）
min_sales = st.sidebar.slider(
    "Minimal Sales Value",
    min_value=float(df["Sales"].min()),
    max_value=float(df["Sales"].max()),
    value=float(df["Sales"].min())
)

# ========== 应用筛选条件 ==========
df_filter = df[
    (df["Region"].isin(select_region)) &
    (df["Category"].isin(select_cat)) &
    (df["Sales"] >= min_sales)
]

# ========== 主页面：可交互动态数据表（重点！） ==========
st.markdown("### Filtered Order Table")
# dataframe：支持点表头排序、拖动调整列宽、上下滚动，就是你要的能动的表
st.dataframe(df_filter, use_container_width=True)

# 可选加分图：销售额柱状图
st.markdown("### Total Sales by Sub-Category")
group_sales = df_filter.groupby("Sub-Category")["Sales"].sum().reset_index()
st.bar_chart(group_sales, x="Sub-Category", y="Sales")
