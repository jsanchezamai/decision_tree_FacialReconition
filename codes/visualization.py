import tkinter as tk

# visualize the tree given the root node of the tree
def visual_tree(tree):
    window = tk.Tk()
    window.title("My tree")
    window.geometry("1800x650")
    
    canvas = tk.Canvas(window, bg = "white", height = 650, width = 5000)
    
    x_width = 5 # width of area to show one node
    y_width = 10 # height of area to show one node
    y_interval = 30 # vertical interval between two nodes
    
    # if I want to put the leftmost node in the left of canvas, calculate x coordinate of root node
    left_number = count_number(tree.kids[1])[0]
    inital_x = (left_number+1) * x_width    
    
    # show the tree using recursion
    show_tree(tree, inital_x, 10, x_width, y_width, y_interval, canvas, inital_x)
    
    canvas.pack()
    window.mainloop()

def show_tree(tree, x, y, x_width, y_width, y_interval, canvas, inital_x):
    '''
        create_text is used to write the text (true or false, the result of leaf nodes)
        create_line is used to draw the edges between two nodes
        create_rectangle is used to draw the background area of nodes
    '''    
    if(tree.op == None):
        canvas.create_text(x+x_width/2,y+y_width,font="Times 15 italic bold",text=str(tree.cls), fill = "black")
        return
    canvas.create_rectangle(x,y,x + x_width,y + y_width, fill = "#FFF2DD", outline = 'white')
    canvas.create_text(x+x_width/2,y+y_width/2,font="Times 15 italic bold",text=tree.op, fill = "black")
    kids = tree.kids
    if(kids[0].op != None):
        far1 = 1 + count_number(kids[0].kids[1])[0]
    else:
        far1 = 1
    if(kids[1].op != None):
        far2 = 1 + count_number(kids[1].kids[0])[0]
    else:
        far2 = 1 
    canvas.create_line(x+x_width,y+y_width,x + far1* x_width+ x_width/2, y + y_interval  + y_width/2, fill = "black", width = "2")
    show_tree(kids[0],  x + far1 * x_width, y + y_interval, x_width, y_width, y_interval, canvas, inital_x)
    canvas.create_line(x,y+y_width,x - far2* x_width +x_width/2, y + y_interval  + y_width/2, fill = "black", width = "2")
    show_tree(kids[1],  x - far2* x_width, y + y_interval, x_width, y_width, y_interval, canvas, inital_x)
    if(x == inital_x):
        canvas.create_text(x+(3/4+far1/2)*x_width,y+3/4*y_width + y_interval/2,font="Times 15 italic bold",text="False", fill = "black")
        canvas.create_text(x+(1/4-far2/2)*x_width,y+3/4*y_width + y_interval/2,font="Times 15 italic bold",text="True", fill = "black")


# count the number of chidrens given one node
def count_number(tree):
    count = [0]
    count_rec(tree, count)
    return count

def count_rec(tree, count):
    count[0] = count[0] + 1
    if(tree.op != None):
        kids = tree.kids
        count_rec(kids[0], count)
        count_rec(kids[1], count)

