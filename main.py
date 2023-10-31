import tkinter as tk
from collections import deque , Counter
class Element(tk.Button):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.kind=1 #defult is 1 it can be -1
        self.container=None
        self.pre_postion=(0,0)
        
class Game :
    def __init__(self,root):
        self.root=root
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        filename = tk.PhotoImage(file = "r.png")
        background_label = tk.Label(self.root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image=filename
        self.right=deque(maxlen=6)
        self.left=deque(maxlen=6)
        self.boat=deque(maxlen=2)
        self.boat_label=tk.Label(self.root,background='Brown', width=20 ,height=3)
        self.boat_label.place(x=200,y=500)
        self.run_btn=tk.Button(self.root,text="run boat",command=self.move_boat,bg='yellow')
        self.run_btn.place(x=440,y=550)
        self.root.update_idletasks() 
        self.half_line=self.root.winfo_width()/2
        
    def build_game(self):
        #Import the image using PhotoImage function
        sheep_img= tk.PhotoImage(file='sh.png')
        wolf_img=tk.PhotoImage(file='wolf.png')
        positions_A=((20,500),(20,440),(20,380))
        positions_M=((100,500),(100,440),(100,380))
        for position in positions_M:
            my_button=Element(self.root,text="hi Im ok",image=sheep_img)
            my_button.image=sheep_img
            my_button.place(x=position[0],y=position[1])
            my_button.bind('<Button-1>',self.move_element)
            my_button.pre_postion=(position[0],position[1])
            self.left.append(my_button)
        for position in positions_A:
            my_button=Element(self.root,text="hi Im ok" ,image=wolf_img)
            my_button.kind=-1
            my_button.image=wolf_img
            my_button.place(x=position[0],y=position[1])
            my_button.bind('<Button-1>',self.move_element)
            my_button.pre_postion=(position[0],position[1])
            self.left.append(my_button)
            
    def check_status(self):
        right=Counter([item.kind for item in self.right])
        left=Counter([item.kind for item in self.left])
        return (right[-1]>right[1] and right[1]!=0) or (left[-1]>left[1] and left [1]!=0)
    
    def new_window(self):
        def close_window():
            dialog.grab_release()
            dialog.destroy()
            for w in self.root.winfo_children():
                w.destroy()
            self.__init__(self.root)
            self.build_game()
            self.run()
        dialog =tk.Toplevel(self.root)
        close =tk.Button(dialog,text="Game over",command=close_window)
        close.pack()
        dialog.grab_set()
            
    def move_element(self,e):
        btn=e.widget
        current_x=btn.winfo_x()
        current_y=btn.winfo_y()
        if btn in self.left:
            #check boat capacity 
            if len(self.boat) == 0 :
                btn.place(x=self.boat_label.winfo_x(),y=self.boat_label.winfo_y())
                self.left.remove(btn)
                self.boat.append(btn)
            elif len(self.boat) == 1 :
                if self.boat[0].winfo_x() ==self.boat_label.winfo_x():
                    btn.place(x=self.boat_label.winfo_x()+btn.winfo_width(),y=self.boat_label.winfo_y())
                else :
                    btn.place(x=self.boat_label.winfo_x(),y=self.boat_label.winfo_y())
                self.left.remove(btn)
                self.boat.append(btn)
            else :
                pass
        elif btn in self.boat:
            
            if current_x<self.half_line:
                btn.place(x=btn.pre_postion[0],y=btn.pre_postion[1])
                self.boat.remove(btn)
                self.left.append(btn)
                
            else:
                #here 
                dif=abs(self.half_line-btn.pre_postion[0]-btn.winfo_width())
                
                btn.place(x=self.half_line+dif,y=btn.pre_postion[1])
                self.boat.remove(btn)
                self.right.append(btn)
        else :
            
            #check where is boat
            if len(self.boat) == 0 :
                btn.place(x=self.boat_label.winfo_x(),y=self.boat_label.winfo_y())
                self.right.remove(btn)
                self.boat.append(btn)
            else  :
                if self.boat[0].winfo_x() ==self.boat_label.winfo_x():
                    btn.place(x=self.boat_label.winfo_x()+btn.winfo_width(),y=self.boat_label.winfo_y())
                else :
                    btn.place(x=self.boat_label.winfo_x(),y=self.boat_label.winfo_y())
                self.right.remove(btn)
                self.boat.append(btn)
            
    
    
    def move_boat(self):
        dif=self.boat_label.winfo_x()+self.boat_label.winfo_width()
        if self.boat_label.winfo_x()<self.half_line:
            
            j=0
            
            for item in self.boat:
                item.place(x=self.half_line+(self.half_line-dif)+(j*item.winfo_width()),y=500)
                j=j+1
            self.boat_label.place(x=self.half_line+(self.half_line-dif),y=500) 
        else:
            i=0
            for item in self.boat:
                item.place(x=self.half_line-(dif-self.half_line)+(i*item.winfo_width()),y=500)
                i+=1
            self.boat_label.place(x=self.half_line-(dif-self.half_line),y=500)  
        
        if self.check_status() :
            
            self.new_window()
                      
            
    def run(self):
        self.root.mainloop()
        
      
root=tk.Tk()      
game=Game(root)
game.build_game()
game.run()