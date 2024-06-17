import tkinter as tk
from tkinter import ttk
from DataBaseConnection import *


# les hash tables 
hash_table = [None] * 60

def hash_function1(id):
    return  id  % 5

def hash_function2(id):
    return  id % 5 + 2

def filling_hash_table_double(treeHash):
    connection = database_connection()
    data = fetch_data_from_database(connection)
    for item in data:
        id_hash = hash_function1(item[0])
 
        if hash_table[id_hash] is None:
            hash_table[id_hash] = item
        else:
            current_index = hash_function2(item[0]) 

            while hash_table[current_index] is not None:
                current_index = current_index + 2
                
            hash_table[current_index] = item
            #populate_treeview()

    for i, item in enumerate(hash_table):
            if item is None:
                item_str = "Empty"
            else:
                item_str = str(item)
            treeHash.insert("", "end", values=(i, item_str))
    return(hash_table)

def search_double_hachage(search_entry,tree):
    id = int(search_entry)  
    index = hash_function1(int(id))
    item = ''
    while hash_table[index] is not None:
        if hash_table[index][0] == id:
            item = hash_table[index]
            break
        index = (index + 2) 
    
    tree.delete(*tree.get_children())
    tree.insert('', 'end', values=(item[0], item))
    tree.pack()
    

    
def delete_item(id):
    id_hash_delete = hash_function1(id) 
    def recursive_delete(i):
        for j in range(i+2, i + 15 ):
            if hash_table[j] is None:
                hash_table[i] = None
                break
            else:
                if hash_function1(hash_table[j][0]) == id_hash_delete:
                    hash_table[i] = hash_table[j]
                    recursive_delete(j)
                    break

    recursive_delete(id_hash_delete)
    connection = database_connection()
    delete_book(connection, id)
    
        



def delete_double_hachage(delete_entry , treeHash):
    id = int(delete_entry) 
    print(id)
    delete_item(id)
    treeHash.delete(*treeHash.get_children())
    print(hash_table)
    for i, item in enumerate(hash_table):
        if item is None:
             item_str = "Empty"
        else:
            item_str = str(item)
        treeHash.insert("", "end", values=(i, item_str))

def insert_item_Double(title , author,year , genre, treeHash ):
  
    connection = database_connection()
    
    insert_book(connection, title, author, year, genre)
    treeHash.delete(*treeHash.get_children())
   
    filling_hash_table_double(treeHash)  
    print(hash_table) 
