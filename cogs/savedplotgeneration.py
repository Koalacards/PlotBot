from discord.ext import commands
from discord_slash import cog_ext
import utils
import plotvars
from plotvars import guild_ids
import asyncutils
from cogs.plots.scatterplot import Scatterplot as scatterplot

class SavedPlotGeneration(commands.Cog):

    @cog_ext.cog_slash(name='plotgenerate', guild_ids=guild_ids, description="Generates a saved plot from one of yoru datasets!")
    async def plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str):
        """Generates a saved plot from a dataset.

        This method will essentially run the graph command without the user having to input a ton of information

        Args:
            dataset_name (str): name of the dataset
            saved_plot_name (str): Name of the saved plot a user generated earlier
        """

        #Get the graph data
        graph_data_dict = await asyncutils.get_graph_data_dictionary(ctx, dataset_name)
        if graph_data_dict is None:
            return

        #Get the saved plot dictionary or error if none is available
        saved_plot_dict = graph_data_dict.get(saved_plot_name, None)

        if saved_plot_dict is None:
            error_msg = f"You do not have a saved plot under the name {saved_plot_name}! Please check the name using `/viewgraphdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(error_msg))
        

        #Iterate through the different graph names to determine which type of graph to plot
        graph_name = saved_plot_dict["name"]
        if graph_name == "scatterplot":
            await self._generatescatter(ctx, dataset_name, saved_plot_dict)
        else:
            error_msg= f"An error occurred on our end when generating the plot: Incorrect plot name stored in DB. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return

    async def _generatescatter(self, ctx, dataset_name:str, saved_plot_dict):
        x_row = None
        y_row = None
        x_label = None
        y_label = None
        size_row = None
        color_row_or_one_color = None
        transparency = None
        try:
            x_row = saved_plot_dict["x_row"]
            y_row = saved_plot_dict["y_row"]
            x_label = saved_plot_dict["x_label"]
            y_label = saved_plot_dict["y_label"]
            size_row = saved_plot_dict["size_row"]
            color_row_or_one_color = saved_plot_dict["color_row_or_one_color"]
            transparency = saved_plot_dict["transparency"]
        except:
            error_msg = f"An error occured on our end when generating the scatterplot: Plot dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return
        
        await scatterplot._scatterplot(scatterplot, ctx, dataset_name, x_row, y_row, x_label, y_label, size_row, color_row_or_one_color, transparency)
        

        
    


def setup(bot):
    bot.add_cog(SavedPlotGeneration(bot))