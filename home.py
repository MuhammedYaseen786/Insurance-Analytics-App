import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *
import time

st.set_page_config(page_title = "Dashboard", page_icon = "🌍", layout = "wide")
st.subheader("🔔 Insurance Descriptive Analytics")
st.markdown("##")

# Fetch Data
result = view_all_data()
df = pd.DataFrame(result, columns = ["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating", "id"])

# Side Bar
st.sidebar.image("designs_logos/ins-logo.jpg", caption = "Data Analytics")

# Switcher
st.sidebar.header("Please Filter")

region = st.sidebar.multiselect(
    "Select Region",
    options = df['Region'].unique(),
    default = df['Region'].unique(),
)

location = st.sidebar.multiselect(
    "Select Location",
    options = df['Location'].unique(),
    default = df['Location'].unique(),
)

construction  = st.sidebar.multiselect(
    "Select Construction",
    options = df['Construction'].unique(),
    default = df['Construction'].unique(),
)

df_selection = df.query(
    "Region == @region & Location == @location & Construction == @construction"
)

def Home():
    with st.expander("Tabular"):
        show_data = st.multiselect('Filter: ', df_selection.columns, default = [])
        st.write(df_selection[show_data])

    # Compute top analytics
    total_investment = df_selection["Investment"].sum()
    investment_mean = float(df_selection["Investment"].mean())
    investment_mode = float(df_selection["Investment"].mode())
    investment_median = float(df_selection["Investment"].median())
    rating = float(df_selection["Rating"].sum())

    total_1, total_2, total_3, total_4, total_5 = st.columns(5, gap = 'large')
    with total_1:
        st.info('Total Investment', icon = "📌")
        st.metric(label = "sum TZS", value = f"{total_investment:,.0f}")

    with total_2:
        st.info("Highly Frequent", icon = "📈")
        st.metric(label = "mode TZS", value = f"{investment_mode:,.0f}")

    with total_3:
        st.info("Average Investment", icon = "📊")
        st.metric(label = "mean TZS", value = f"{investment_mean:,.0f}")

    with total_4:
        st.info("Central Earnings", icon = "📌")
        st.metric(label = "median TZS", value = f"{investment_median:,.0f}")

    with total_5:
        st.info("Ratings", icon = "📍")
        st.metric(label = "Rating", value = numerize(rating), help = f""" Total Rating: {rating} """)

    st.markdown("""---""")


# Graphical Representation
def graphs():
    #total_investment = int(df_selection["Investment"].sum())
    #average_rating = int(round(df_selection["Investment"].mean()), 2)

    # Simple Bar Graph
    investment_of_business_type = (
        df_selection.groupby(by = ["BusinessType"]).count()[["Investment"]].sort_values(by = "Investment")
    )

    fig_investment = px.bar(
        investment_of_business_type,
        x = "Investment",
        y = investment_of_business_type.index,
        orientation = "h",
        title = "<b> Investment by Business Type </b>",
        color = ["#0083b8"]*len(investment_of_business_type),
        template = "plotly_white"
    )

    fig_investment.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid = False))
    )

    # Simple Area Graph
    investment_by_state = df_selection.groupby(by = ["State"]).count()[["Investment"]]

    fig_state = px.area(
        investment_by_state,
        x = investment_by_state.index,
        y = "Investment",
        orientation = "v",
        title = "<b> Investment by State </b>",
        color_discrete_sequence = ["#0083b8"]*len(investment_by_state),
        template = "plotly_white"
    )

    fig_state.update_layout(
        xaxis = dict(tickmode = "linear"),
        plot_bgcolor = "rgba(0,0,0,0)",
        yaxis = (dict(showgrid = False))
    )

    left, right  = st.columns(2)
    left.plotly_chart(fig_state, use_container_width = True)
    right.plotly_chart(fig_investment, use_container_width = True)


def progress_bar():
    st.markdown(""" <style>.stProgress > div > div > div > div { background-image: linear-gradient (to right, #99ff99, #FFFF00)}</style>""", unsafe_allow_html = True)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current/target*100))
    my_bar = st.progress(0)

    if percent > 100:
        st.subheader("Target Done !")
    else:
        st.write("You have ", percent, "%", "of", (format(target, 'd')), "TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            my_bar.progress(percent_complete+1, text = " Target Percentage")


def side_bar():
    with st.sidebar:
        selected = option_menu(
            menu_title = "Main Menu",
            options = ["Home", "Progress"],
            icons = ["house", "eye"],
            menu_icon = "cast",
            default_index = 0
        )
    if selected == "Home":
        st.subheader(f"Page: {selected}")
        Home()
        graphs()

    if selected == "Progress":
        st.subheader(f"Page: {selected}")
        progress_bar()
        graphs()

side_bar()


# Theme Variations
hide_st_style = """

<style>
#MainMenu{visiblity:hidden;}
footer{visiblity:hidden;}
header{visiblity:hidden;}
</style>

"""




