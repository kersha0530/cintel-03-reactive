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


@reactive.calc
def dat():
    infile = Path(__file__).parent / "penguins.csv"
    return pandas.read_csv(infile)

# Get the columns for the dropdown menu
@reactive.Calc
def dropdown_columns():
    return ["island", "bill_length_mm", "bill_depth_mm", "body_mass_g", "sex", "year"]


# Define the reactive dataset function
@reactive.Calc
def filtered_data():
    data = penguins_df[
        penguins_df['species'].isin(input.selected_species_list()) &
        penguins_df['island'].isin(input.selected_island_list())
    ]
    return

from shiny.express import ui



with ui.sidebar(bg="#f8f8f8"):
    ui.input_slider("n", "N", 0, 100, 20)
    ui.input_selectize("selected_attribute", "Select attribute", ["species", "island", "bill_length_mm", "bill_depth_mm", "body_mass_g", "sex", "year"]),
    # Create a checkbox group input for penguin species
    ui.input_checkbox_group(
        "checkbox_group", 
        "Penguin Species", 
        {
            "Chinstrap": "Chinstrap",
            "Gentoo": "Gentoo",
            "Adelie": "Adelie",
        }
    )
    # Create a checkbox group input for islands
    ui.input_checkbox_group(
        "island_checkbox_group", 
        "Select Islands", 
        {
            "Biscoe": "Biscoe",
            "Dream": "Dream",
            "Torgersen": "Torgersen"
        }
    )
 


@render.text
def value():
    return ", ".join(input.checkbox_group())


"Main content"  

with ui.navset_card_underline():

    with ui.nav_panel("Data frame"):

        @render.data_frame
        def frame():
            # Give dat() to render.DataGrid to customize the grid
            return dat()

    with ui.nav_panel("Table"):

        @render.table
        def table():
            return dat()


ui.page_opts(title="Kersha Palmer Penguin Dataset Exploration", fillable=True)
with ui.layout_columns():



    @render_plotly
    def plotly_histogram():
        # Plotly histogram showing the distribution of the selected attribute for the selected species
        return px.histogram(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                          title="Flipper Length vs. Bill Length")

    @render_plotly
    def plotly_scatterplot():
        # Scatterplot of flipper length vs. bill length with species colored
        return px.scatter(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                          title="Flipper Length vs. Bill Length")


@render.plot
def seaborn_histogram():
    # Ensure the dataset is loaded
    penguins_df = dat()
    
    # Seaborn histogram showing the body mass of penguins
    fig, ax = plt.subplots()
    sns.histplot(data=penguins_df, x="body_mass_g", hue="species", multiple="stack", ax=ax)
    ax.set_title("Body Mass Distribution (Seaborn)")
    ax.set_xlabel("Mass (g)")
    ax.set_ylabel("Count")
    return fig


    @render_plotly
    def plotly_histogram():
        # Plotly histogram showing distribution of all species
        filtered_df = penguins_df[penguins_df['species'].isin(input.selected_species_list())]
        return px.histogram(filtered_df, x=input.selected_attribute(), nbins=input.plotly_bin_count())

    @render.table
    def penguins_grid():
        # Render full dataset as a data grid (basic for now, can be enhanced)
        return penguins_df

    @render.table
    def penguins_table():
        # Render full dataset as a table
        return penguins_df
