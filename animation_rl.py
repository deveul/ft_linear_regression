import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animation_rl(data, history):
    anim_running = True
    fig, ax = plt.subplots()
    ln, = plt.plot([], [], '-')
    
    def init():
        ax.clear()
        plt.axes = ([0, max(data, key=lambda x:x['km'])['km'], \
            0, max(data, key=lambda x:x['price'])['price']])
        plt.axhline(0, color='grey')
        plt.axvline(0, color='grey')
        plt.xlabel('km')
        plt.ylabel('price')
        plt.title('Linear Regression')

        # On affiche les points du data set
        plt.scatter([x['km'] for x in data], [y['price'] for y in data], c='purple')

        ln.set_data([],[])
        return ln,
        
    def onClick(event):
        global anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    def press(event):
        global anim_running
        if event.key == 'enter':
            anim.frame_seq = anim.new_frame_seq() 
            if anim_running == False:
                anim.event_source.start()
                anim_running = True

    def animate(i): 
        x = np.linspace(min(data, key=lambda x:x['km'])['km'], max(data, key=lambda x:x['km'])['km'], 100)
        y = history[i][0] + history[i][1] * x
        ln.set_data(x, y)
        return ln,

    fig.canvas.mpl_connect('button_press_event', onClick)
    fig.canvas.mpl_connect('key_press_event', press)

    anim = FuncAnimation(fig, animate, frames=len(history), init_func=init, blit=True, interval = 10)

    plt.show()
