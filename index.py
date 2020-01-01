from tkinter import ttk
from tkinter import *
import sqlite3

class Product:
    #connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        #initialozations
        self.wind = window
        self.wind.title("aplicacion de Productos")

        # row= fila, izquiera superior, columspan son columnas vacias sin contenido para dejar espacio y el pady espaciado interno de los elementos para que no se vean juntos 



        #creating a Frame Conatiner
        frame = LabelFrame(self.wind, text= 'Registro de Nuevos Productos')
        frame.grid(row=0, column=0, columnspan = 3, pady = 20)

        #name Input
        Label(frame, text= 'Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #price input
        Label(frame, text= 'Precio: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.focus()
        self.price.grid(row=2, column=1)

        #button add Messages
        ttk.Button(frame, text= 'Guardar Producto', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        #output messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row=3, column = 0, columnspan=2,  sticky = W + E)

        #table
        self.tree = ttk.Treeview(height = 10, columns=2)
        self.tree.grid(row=4, column =0, columnspan =2)
        self.tree.heading('#0', text= "Nombre", anchor = CENTER)
        self.tree.heading('#1', text= "Precio", anchor = CENTER)

        #buttons
        ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_products()

    #function to excute consults database
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.excute(query, parameters)
            conn.commit()
        return result
    
    #get Products from database
    def get_products(self):
        #cleannig table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            #gwtting data
            query = 'SELECT * FROM product ORDER BY name DESC'
            db_rows = self.run_query(query)
            #filling data
            for row in db_rows:
                self.tree.insert('', 0, text = row[1], values= row[2])

    #user input validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'El Nombre y Precio son Requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, selecciona un producto'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, selecciona un producto'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Price:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price 
        Label(self.edit_wind, text = 'Old Price:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'New Name:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    aplications = Product(window)
    window.mainloop()