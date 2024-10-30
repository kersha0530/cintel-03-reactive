import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from pathlib import Path
import palmerpenguins
import pandas
import matplotlib.pyplot as plt
from shiny import reactive
from shiny.express import render, ui
import seaborn as sns


# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Optional title for the app
app_title = "Penguins Dataset Exploration"

# UI Layout for the App
ui.page_opts(title="Kersha Palmer Penguin Dataset Exploration", fillable=True)

with ui.sidebar(bg="#f8f8f8"):
    ui.input_selectize("selected_species_list", "Select Species", ["Adelie", "Gentoo", "Chinstrap"], multiple=True)
    ui.input_selectize("selected_island_list", "Select Island", ["Biscoe", "Dream", "Torgersen"], multiple=True)
    ui.input_slider("flipper_length_mm", "Flipper length (mm)", 150, 250, (150, 250))
    ui.input_slider("bill_depth_mm", "Bill depth (mm)", 13, 21, (13, 21))
    ui.input_slider("bill_length_mm", "Bill length (mm)", 30, 60, (30, 60))
    ui.input_slider("body_mass_g", "Body mass (g)", 2500, 6500, (2500, 6500))
    ui.input_selectize("sex", "Select Sex", ["Male", "Female"])
    ui.input_slider("year", "Select Year", 2007, 2009, 2008)

with ui.navset_card_underline():
    with ui.nav_panel("Filtered Table"):
        @render.table
        def filtered_table():
            return filtered_data()

    with ui.nav_panel("Histogram"):
        @render_plotly
        def plotly_histogram():
            filtered_df = filtered_data()
            return px.histogram(filtered_df, x="flipper_length_mm", color="species", 
                                 title="Flipper Length Histogram")

    with ui.nav_panel("Scatterplot"):
        @render_plotly
        def plotly_scatterplot():
            filtered_df = filtered_data()
            return px.scatter(filtered_df, x="flipper_length_mm", y="bill_length_mm", color="species",
                               title="Flipper Length vs. Bill Length")

    with ui.nav_panel("Seaborn Histogram"):
        @render.plot
        def seaborn_histogram():
            filtered_df = filtered_data()
            fig, ax = plt.subplots()
            sns.histplot(data=filtered_df, x="body_mass_g", hue="species", multiple="stack", ax=ax)
            ax.set_title("Body Mass Distribution (Seaborn)")
            ax.set_xlabel("Mass (g)")
            ax.set_ylabel("Count")
            return fig

# Reactive function to filter data
@reactive.Calc
def filtered_data():
    data = penguins_df.copy()

    # Filter by species
    selected_species = input.selected_species_list()
    if selected_species:
        data = data[data['species'].isin(selected_species)]
    
    # Filter by islands
    selected_islands = input.selected_island_list()
    if selected_islands:
        data = data[data['island'].isin(selected_islands)]

    # Filter by flipper length
    flipper_length = input.flipper_length_mm
    if isinstance(flipper_length, list) and len(flipper_length) == 2:
        data = data[(data['flipper_length_mm'] >= flipper_length[0]) & 
                    (data['flipper_length_mm'] <= flipper_length[1])]

    # Additional filtering can go here...

    return data

# Server logic
def server(input, output, session):
    @output
    @render.table
    def filtered_table():
        return filtered_data()

    @output
    @render_plotly
    def plotly_histogram():
        filtered_df = filtered_data()
        return px.histogram(filtered_df, x="flipper_length_mm", color="species", title="Flipper Length Histogram")

    @output
    @render_plotly
    def plotly_scatterplot():
        filtered_df = filtered_data()
        return px.scatter(filtered_df, x="flipper_length_mm", y="bill_length_mm", color="species", title="Flipper Length vs. Bill Length")

    @output
    @render.plot
    def seaborn_histogram():
        filtered_df = filtered_data()
        fig, ax = plt.subplots()
        sns.histplot(data=filtered_df, x="body_mass_g", hue="species", multiple="stack", ax=ax)
        ax.set_title("Body Mass Distribution (Seaborn)")
        ax.set_xlabel("Body Mass (g)")
        ax.set_ylabel("Count")
        return fig


def create_hyperlink(text, href, target="_blank"):
    return f'<a href="{href}" target="{target}">{text}</a>'

# Usage
hyperlink = create_hyperlink("Cintel-3 Interactive File", href="https://github.com/kersha0530/cintel-3-reactive", target="_blank")
print(hyperlink)


