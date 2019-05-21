
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from data_analysis import data_transformation
from matplotlib.lines import Line2D

def plot_scroll_annotate_bar_chart(data):
    '''
    input dataframe in pandas object that contains date, number of like, color, image
    the dataframe should be scrapped by IG_scrapper and formatted by data_analysis

    output: show a plot that have a scrollable bar chart. Upon click, it will generate the image

    '''

    # initial parameter for the graph
    num_start = 0
    num_show = 30
    buffer_at_top = 10
    num_val = 0

    # crave out the subplot section
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    
    # read the data
    num_data = len(data['date'])
    index = np.arange(num_data)
    max_y = max(data['number_of_like'])

    # set the x & y value
    x = np.arange(0, num_show)
    y = data['number_of_like'][num_start : num_show]

    # set the legend
    legend_elements = [Line2D([0], [0], color='red', lw=4, label='midnight 0:00 - 6:00', alpha=0.6),
                        Line2D([0], [0], color='green', lw=4, label='morning 6:00 - 12:00', alpha=0.6),
                        Line2D([0], [0], color='blue', lw=4, label='afternoon 12:00 - 18:00', alpha=0.6),
                        Line2D([0], [0], color='cyan', lw=4, label='night 18:00 - 24:00', alpha=0.6)]

    # format the ax of the figure
    ax_formating(ax,
                x, 
                data['date'][num_start + num_val: num_show + num_val],
                max_y + buffer_at_top, 
                "Number of Like Chart over time",
                "Date", 
                'Number of Like',
                legend_elements,
                font_size=6)


    bars = ax.bar(x, y, alpha = 0.6, color=list(data['color'][:num_show]))

    # set the slider axes in the bottom
    axcolor = 'lightgoldenrodyellow'

    # the first argument means the positin of the axes in ['left', 'bottom', 'height', width']
    axpos = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor=axcolor)
    slide_ax = Slider(axpos, 'timeindex',0, num_data-num_show, valinit=0, valstep = 1)

    # this is a event call function to update the function whenever the slider value is updated
    def update(val):
        num_val = int(slide_ax.val)
        ax.cla() # clear the axes
        bars = ax.bar(x, data['number_of_like'][num_start + num_val: num_show + num_val], color=list(data['color'][num_start + num_val: num_show + num_val]), alpha = 0.6)
        ax_formating(ax, 
                    x, 
                    data['date'][num_start + num_val: num_show + num_val],
                    max_y + buffer_at_top,  
                    "Number of Like Chart over time",
                    "Date", 
                    'Number of Like',
                    legend_elements,
                    font_size=6)

        fig.canvas.draw_idle()
        annot_and_hover(-20,20, fig, ax, bars, slide_ax, data)

    slide_ax.on_changed(update)

    # set up the annotation and hover
    annot_and_hover(-20,20, fig, ax, bars, slide_ax, data)

    plt.show()


def ax_formating(ax, x, xticklabel, top_y_lim, title, xlabel, ylabel, legend_elements, font_size):
    '''
    a function to format the ax
    '''
    ax.set_xticks(x)
    ax.set_xticklabels(xticklabel, rotation=90, fontsize = 8)
    ax.set_ylim(bottom = 0, top =  top_y_lim)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(handles=legend_elements, fontsize=font_size)

def annot_and_hover(x_pos,y_pos, fig, ax, bars, slider_val, df):
    '''
    This is a function to set up the annotation and hover so as to show the text on the top of the bar
    x_pos : x coordinate that the pointer is pointed to
    y_pos : y coordinate that the pointer is pointed to
    fig : figure of the plot
    ax : axis of the plot
    bars : bars of the plot

    '''

    img = df['image'][0]
    img_show = OffsetImage(img, zoom=0.05)
    annot = AnnotationBbox(img_show, xy=(0,0), xybox=(x_pos,y_pos),xycoords='data',
                        boxcoords="offset points",  pad=0.3,  arrowprops=dict(arrowstyle="->"))

    ax.add_artist(annot)
    annot.set_visible(False)

    # this functino work with hover func to update the annotation value and pos
    def update_annot(bar):
        x = bar.get_x()+bar.get_width()/2 # to ensure the pointer is pointed to the center
        print('{}'.format(x))
        y = bar.get_y()+bar.get_height()
        annot.xy = (x,y)
        num = int(slider_val.val + x)
        img = df['image'][num]
        img_show.set_data(img)

    # set up the hover event
    def hover(event):
        vis = annot.get_visible()
        print('slider value is{}'.format(slider_val.val))
        print('x is {}'.format(event.x))
        if event.inaxes == ax:
            for bar in bars:
                cont, ind = bar.contains(event) # it will return cont when mouse is over the container
                if cont:
                    update_annot(bar)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                    return # stop the function when mouse it's over any bar
        if vis:
            annot.set_visible(False)
            fig.canvas.draw_idle()

    # connect the event and call back hover functino with the background fig.convas
    fig.canvas.mpl_connect("button_press_event", hover)
    