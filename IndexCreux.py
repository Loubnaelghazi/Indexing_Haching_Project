
from DataBaseConnection import *

class IndexCreux:
    def __init__(self):
        self.index = {}

    def add_entry(self, key, record):
        if key in self.index:
            self.index[key].append(record)
        else:
            self.index[key] = [record]
        return self.index
    
    def search(self, key):
        if key in self.index:
            return self.index[key]
        else:
            return None
    def delete(self, key):
        if key in self.index:
            del self.index[key]
        
    def display(self):
        print("Index Creux:")
        for key, records in self.index.items():
            print(f"Key: {key}, Records: {records}")
    def getDict(self):
        return self.index
    

index_creux = IndexCreux()
def filling_hash_table_creux(tree):
    index = index_creux.getDict()  
    index.clear()    
    print(index)  
    connection = database_connection()
    data = fetch_data_from_database(connection)
    
    for item in data:
        index_creux.add_entry(item[3], item)
    print(index)
    for key, value in index.items():
        tree.insert('', 'end', values=(key, value))
    tree.pack()



def search_creux(search_entry,tree):
    year = search_entry
    resualt = index_creux.search(year)
    tree.delete(*tree.get_children())
    print(resualt)
    for record in resualt:
        tree.insert('', 'end', values=(record[3], record))
    tree.pack()

# delete function 
def delete_creux(delete_entry , tree):
    year = delete_entry
    print(year)
    index_creux.delete(year)
    tree.delete(*tree.get_children())
    index = index_creux.getDict()
    for key, value in index.items():
        tree.insert('', 'end', values=(key, value))
    tree.pack()
    connection = database_connection()
    delete_book(connection, id)

def insert_item_creux(title , author,year , genre, treeHash ):
  
    connection = database_connection()
    
    insert_book(connection, title, author, year, genre)
    treeHash.delete(*treeHash.get_children())
   
    filling_hash_table_creux(treeHash)

