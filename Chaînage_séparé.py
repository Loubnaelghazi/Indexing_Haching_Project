import tkinter as tk
from tkinter import ttk
from DataBaseConnection import *

#hash tables 
hash_table = [[] for _ in range(15)]

def hash_function(id):
    return  id  % 5


def filling_hash_table_separe(tree):
    for i in range(len(hash_table)):
        hash_table[i] = []
    connection = database_connection()
    data = fetch_data_from_database(connection)
 
    for item in data:
        id_hash = hash_function(item[0])
        if not hash_table[id_hash]:
           hash_table[id_hash].append(item)
        else :
            i = len(hash_table[id_hash])
            hash_table[id_hash].insert(i, item)

    
    for i, item in enumerate(hash_table):
        item_str = str(item)
        tree.insert("", "end", values=(i, item_str))  
    return(hash_table)

def search_chaine_separee(search_entry,tree):
    id = int(search_entry) 
    item_found = '' 
    id_hash_search = hash_function(id) 
    item_serch_in_it = hash_table[id_hash_search]
    for item in item_serch_in_it:
            if item[0] == id:
                 item_found= item
                 
    tree.delete(*tree.get_children())
    tree.insert('', 'end', values=(item_found[0], item_found))
    tree.pack()
                
def delete_item(id):
    id_hash_search = hash_function(id) 
    for index, item in enumerate(hash_table[id_hash_search]):
        
        if item[0] == id:
            if index + 1 < len(hash_table[id_hash_search]) and not hash_table[id_hash_search][index + 1]:
                del hash_table[id_hash_search][index]
            else:
                del hash_table[id_hash_search][index]
    connection = database_connection()
    delete_book(connection, id)


def delete_chaine_separee(delete_entry , tree):
    id = int(delete_entry) 
    delete_item(id)
    tree.delete(*tree.get_children())
    
    for i, item in enumerate(hash_table):
        item_str = str(item)
        tree.insert("", "end", values=(i, item_str)) 

def insert_item_separe(title , author,year , genre, tree):
  
    connection = database_connection()
    
    insert_book(connection, title, author, year, genre)
    tree.delete(*tree.get_children())
    filling_hash_table_separe(tree)
    print(hash_table) 

