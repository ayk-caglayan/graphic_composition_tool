#%matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton, KeyEvent
import pyperclip
#plt.ion() #matplotlib interaction on

def redraw():
    ax.clear()
    #ax.plot(plots[activated_plot_nr].keys(), plots[activated_plot_nr].values(), 'bo')
    for i in range(int(nr_of_plots)):
        ax.scatter(plots[i].keys(), plots[i].values(), marker='o', color=colors[i], label='plot ' + str(i))
    ax.set_title(colors[activated_plot_nr].capitalize()+"Plot w/ nr. "+str(activated_plot_nr)+" is active")
    plt.xlim([int(x_start), int(x_end)])
    plt.ylim([int(y_start), int(y_end)])
    plt.xticks(range(int(x_start), int(x_end),1))
    plt.yticks(range(int(y_start), int(y_end), 5))
    plt.grid()
    fig.canvas.draw()


nr_of_plots=input("Number of plots on a canvas (max. 10): ")
x_start=input("X axis starting value: ")
x_end=input("X axis ending value: ")
y_start=input("Y axis starting value: ")
y_end=input("Y axis ending value: ")

plots={} #dictionary of plots (btw. plots are dictionaries of data points)
colors={0: 'blue', 1: 'green', 2:'red', 3: 'yellow', 4:'brown', 5: 'grey', 6: 'olive', 7: 'orange', 8: 'magenta', 9: 'darkgreen'}
color_map=""
for i in range(int(nr_of_plots)):
    color_map=color_map+str(i)+". "+str(colors[i]+", ") #formats color map in use
    plots[i]={} #generates empty dic with keys as plot numbers 
    
global activated_plot_nr
activated_plot_nr=0 #this functions as a flag for activated plot to insert and export the data
    
fig, ax = plt.subplots()
fig.suptitle("Clicking LEFT adds new point, RIGHT removes it, MIDDLE or ctrl+c copies the activated plot to clipboard \n "+color_map)

def plot_select(event):
    global activated_plot_nr
    try:
        keyy=int(event.key)
        if keyy<10 and keyy<int(nr_of_plots):
            activated_plot_nr=keyy
            print('plot number ', keyy, ' selected')
            redraw()
    except:
        print("invalid input")

def copy_w_ctrl_c(event):
    if event.key=='ctrl+c':
        print("The Data of the ", colors[activated_plot_nr].capitalize(), "Plot NO:", activated_plot_nr, "Pasted To Clipboard ", str([list(plots[activated_plot_nr].keys()), list(plots[activated_plot_nr].values())]))
        pyperclip.copy(str([list(plots[activated_plot_nr].keys()), list(plots[activated_plot_nr].values())]))
        
        
def on_click(event):
    if event.button is MouseButton.LEFT:
        x, y = event.xdata, event.ydata
        plots[activated_plot_nr][int(x)]=int(y)
        redraw()
        
    if event.button is MouseButton.RIGHT:
        x, y = event.xdata, event.ydata
        plots[activated_plot_nr].pop(int(x))
        redraw()

    if event.button is MouseButton.MIDDLE:
        print("The Data of the ", colors[activated_plot_nr].capitalize(), "Plot NO:", activated_plot_nr, "Pasted To Clipboard ", str([list(plots[activated_plot_nr].keys()), list(plots[activated_plot_nr].values())]))
        pyperclip.copy(str([list(plots[activated_plot_nr].keys()), list(plots[activated_plot_nr].values())]))
        
plt.connect('key_press_event', plot_select)        
plt.connect('button_press_event', on_click)
plt.connect('key_press_event', copy_w_ctrl_c)

plt.xlim([int(x_start), int(x_end)])
plt.ylim([int(y_start), int(y_end)])
plt.xticks(range(int(x_start), int(x_end),1))
plt.yticks(range(int(y_start), int(y_end), 5))
plt.grid()        
plt.show()



    
