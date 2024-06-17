import tkinter as tk
from tkinter import ttk
from DataBaseConnection import *
from DataBaseConnection import get_item




"""def populate_treeview():
    # Fetch data from the database
    data = fetch_data_from_database()
    # Clear existing items in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insert data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)"""

#hash tables 
hash_table = [None for _ in range(50)] 

def hash_function(id):
    return  id  % 5

def filling_hash_table_essai(treeHash):
    for i in range(len(hash_table)):
        hash_table[i] = None
    connection = database_connection()
    data = fetch_data_from_database(connection)
    #print(data)
    for item in data:
        id_hash = hash_function(item[0])
        if  hash_table[id_hash] == None:  
            hash_table[id_hash] = item
        else:
            
            for i in range(id_hash + 1, id_hash + 30):  
                if not hash_table[i]:
                    hash_table[i] = item
                    break

    for i, item in enumerate(hash_table):
        if item is None:
             item_str = "Empty"
        else:
            item_str = str(item)
        treeHash.insert("", "end", values=(i, item_str))
    return(hash_table)

def delete_item(id):
    print(hash_table)
    id_hash_delete = hash_function(id) 
    def recursive_delete(i):
        for j in range(i + 1, i + 49):
            if  hash_table[j] == None :
                hash_table[i] = None
                break
            else:
                if hash_function(hash_table[j][0]) == id_hash_delete:
                    hash_table[i] = hash_table[j]
                    recursive_delete(j)
                    break
                
    recursive_delete(id_hash_delete)
    connection = database_connection()
    delete_book(connection, id)
    

def search_essai(search_entry,tree):
    id = int(search_entry)  
    index = hash_function(int(id))

    while hash_table[index] is not None:
        if hash_table[index][0] == id:
            item = hash_table[index]
            break
        index = (index + 1) 
    tree.delete(*tree.get_children())
    tree.insert('', 'end', values=(item[0], item))
    tree.pack()
    


def delete_essai (delete_entry , treeHash):
    id = int(delete_entry) 
    print(id) 
    delete_item(id)
    treeHash.delete(*treeHash.get_children())
    
    for i, item in enumerate(hash_table):
        if item is None:
             item_str = "Empty"
        else:
            item_str = str(item)
        treeHash.insert("", "end", values=(i, item_str))
    connection = database_connection()
    delete_book(connection, id)
  
def insert_item_essai(title , author,year , genre, treeHash ):
  
    connection = database_connection()
    
    insert_book(connection, title, author, year, genre)
    treeHash.delete(*treeHash.get_children())
   
    filling_hash_table_essai(treeHash)
    
    
def modify_item_essai(id , title_input,author_input , year_user_input ,genre_user_input ):
    book_id = int(id)
    connection = database_connection()
    item = get_item(connection, book_id)
    print(item[0][1])
    ####################################
    title_input.delete(0, "end") 
    title_input.insert(0, item[0][1])     
    author_input.delete(0, "end")
    author_input.insert(0, item[0][2])  
    year_user_input.delete(0, "end")
    year_user_input.insert(0, item[0][3])  
    genre_user_input.delete(0, "end")
    genre_user_input.insert(0, item[0][4])
    ###########################################
    title = title_input.get()
    author = author_input.get()
    year = year_user_input.get()
    genre = genre_user_input.get()
    ###########################################
    print(title)


    