#%matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton, KeyEvent
import pyperclip, pickle, sys, time
#plt.ion() #matplotlib interaction on

global activated_plot_nr
activated_plot_nr=0 #this functions as a flag for activated plot to insert and export the data
fig, ax = plt.subplots()


#file import
if len(sys.argv)>1: #if a pickle file path given, loads objects from it
    file_to_be_imported=sys.argv[1]
    print(file_to_be_imported, type(file_to_be_imported))
    #im_po=         pickle.load(open(sys.argv[1], "rb"))
    imported_stuff=pickle.load(open(sys.argv[1], "rb"))
    print(imported_stuff)
    nr_of_plots=imported_stuff['nr_of_plots']
    x_start=imported_stuff['x_start']
    x_end=imported_stuff['x_end']
    y_start=imported_stuff['y_start']
    y_end=imported_stuff['y_end']
    x_range=imported_stuff['x_range']
    y_range=imported_stuff['y_range']
    plots=imported_stuff['plots']
    
    
else: #if not, user inputs through terminal prompt
    nr_of_plots=input("Number of plots on a canvas (max. 10): ")
    x_start=input("X axis starting value: ")
    x_end=input("X axis ending value: ")
    y_start=input("Y axis starting value: ")
    y_end=input("Y axis ending value: ")
    x_range=int(x_end)-int(x_start)
    y_range=int(y_end)-int(y_start)
    plots={} #dictionary of plots (btw. plots are dictionaries of data points)
    for i in range(int(nr_of_plots)):
        plots[i]={}
   
    
if x_range<20:
    x_ticks=1
elif x_range>=20:
    x_ticks=int(x_range/20)
    
if y_range<10:
    y_ticks=1
elif y_range>=10:
    y_ticks=int(y_range/10)


colors={0: 'blue', 1: 'green', 2:'red', 3: 'yellow', 4:'brown', 5: 'grey', 6: 'olive', 7: 'orange', 8: 'magenta', 9: 'darkgreen'}
color_map=""
for i in range(int(nr_of_plots)):
    color_map=color_map+str(i)+". "+str(colors[i]+", ") #formats color map in use


fig.suptitle("LEFT click adds new point, RIGHT removes it, MIDDLE or ctrl+c copies the activated plot to clipboard \n "+"switch colors w/ number keys "+color_map)
fig.text(0,0.01, "CTRL+R writes the plot to a binary file - saved plot file can be opened on the start > python3 graphic_composition_001.py PLOT_21..plt")


def format_file_name():
    localtime=time.localtime()
    year=str(localtime[0])[2:]
    month='0'+str(localtime[1])
    day=str(localtime[2])+'_'
    hour=str(localtime[3])+'-'+str(localtime[4])
    file_name='PLOT_'+year+month+day+hour+'.plt'
    return file_name

def redraw():
    ax.clear()
    #ax.plot(plots[activated_plot_nr].keys(), plots[activated_plot_nr].values(), 'bo')
    for i in range(int(nr_of_plots)):
        ax.scatter(plots[i].keys(), plots[i].values(), marker='o', color=colors[i], label='plot ' + str(i))
    ax.set_title(colors[activated_plot_nr].capitalize()+"Plot w/ nr. "+str(activated_plot_nr)+" is active")
    plt.xlim([int(x_start), int(x_end)])
    plt.ylim([int(y_start), int(y_end)])
    plt.xticks(range(int(x_start), int(x_end),x_ticks))
    plt.yticks(range(int(y_start), int(y_end), y_ticks))
    plt.grid()
    fig.canvas.draw()

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
        sorted_active_plot_x=sorted(plots[activated_plot_nr].keys())
        sorted_active_plot_y=[plots[activated_plot_nr].get(x) for x in sorted_active_plot_x]
        print("The Data of the ", colors[activated_plot_nr].capitalize(), "Plot NO:", activated_plot_nr, "Pasted To Clipboard ", str(sorted_active_plot_x), str(sorted_active_plot_y))
        #pyperclip.copy(str(list(sorted_active_plot_x, sorted_active_plot_y)))
        pyperclip.copy(str(sorted_active_plot_x) + str(sorted_active_plot_y))
        
        
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
        sorted_active_plot_x=sorted(plots[activated_plot_nr].keys())
        sorted_active_plot_y=[plots[activated_plot_nr].get(x) for x in sorted_active_plot_x]
        print("The Data of the ", colors[activated_plot_nr].capitalize(), "Plot NO:", activated_plot_nr, "Pasted To Clipboard ", str(sorted_active_plot_x), str(sorted_active_plot_y))
        #pyperclip.copy(str([list(plots[activated_plot_nr].keys()), list(plots[activated_plot_nr].values())]))
        #pyperclip.copy(str(list(sorted_active_plot_x, sorted_active_plot_y)))
        pyperclip.copy(str(sorted_active_plot_x) + str(sorted_active_plot_y))
        
def save_plot(event):
    if event.key=='ctrl+r':
        print('saves the plot')
        fileName=format_file_name()
        dump_obj={'nr_of_plots': nr_of_plots, 'x_start': x_start, 'x_end': x_end, 'y_start': y_start, 'y_end': y_end, 'x_range': x_range, 'y_range': y_range, 'plots':plots}
        pickle.dump(dump_obj, open(fileName, 'wb'))
    
redraw()
plt.connect('key_press_event', plot_select)        
plt.connect('button_press_event', on_click)
plt.connect('key_press_event', copy_w_ctrl_c)
plt.connect('key_press_event', save_plot)

plt.xlim([int(x_start), int(x_end)])
plt.ylim([int(y_start), int(y_end)])
plt.xticks(range(int(x_start), int(x_end),x_ticks))
plt.yticks(range(int(y_start), int(y_end), y_ticks))
plt.grid()        
plt.show()



    
