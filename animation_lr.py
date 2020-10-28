import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationLr():
    def __init__(self, data, history):
        self.anim_running = True
        self.fig, self.ax = plt.subplots()
        self.ln, = plt.plot([], [], '-', c=u'#1f77b4')
        self.anim = None
        self.data = data
        self.min_km = min(self.data, key=lambda x:x['km'])['km']
        self.max_km = max(self.data, key=lambda x:x['km'])['km']
        self.max_price = max(self.data, key=lambda x:x['price'])['price']
        self.history = history
    
    def init_animation(self):
        self.ax.clear()
        plt.axhline(0, color='grey')
        plt.axvline(0, color='grey')
        plt.xlabel('km')
        plt.ylabel('price')
        plt.title('Linear Regression evolution')
        plt.plot([],[], '-', label="price = θ₀ + km * θ₁", c=u'#1f77b4')
        self.ln.set_data([],[])
        # self.ln.set_label("")

        # On affiche les points du data set
        plt.scatter([x['km'] for x in self.data], [y['price'] for y in self.data], c='purple', label='Values of data set')
        self.ax.set_ylim(bottom=0)
        self.ax.set_xlim(left=0)
        plt.legend(loc="lower center")

        return self.ln,

    def onClick(self, event):
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim_running = False
        else:
            self.anim.event_source.start()
            self.anim_running = True

    def press(self, event):
        if event.key == 'enter':
            self.anim.frame_seq = self.anim.new_frame_seq() 
            if self.anim_running == False:
                self.anim.event_source.start()
                self.anim_running = True

    def animate(self, i): 
        x = np.linspace(self.min_km, self.max_km, 100)
        y = self.history[i][0] + self.history[i][1] * x
        self.ln.set_data(x, y)
        return self.ln,


    def start(self):
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.fig.canvas.mpl_connect('key_press_event', self.press)
        self.anim = FuncAnimation(self.fig, self.animate, frames=len(self.history), init_func=self.init_animation, blit=True, interval = 10)
        plt.show()

def animation_lr(data, history):
    ft_anim = AnimationLr(data, history)
    ft_anim.start()
