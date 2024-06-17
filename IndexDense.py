
from DataBaseConnection import *

class DenseIndex:
    def __init__(self):
        self.index = []

    def add_entry(self, key, record_location):
        self.index.append((key, record_location))

    def search_all(self, key):
        return [(k, location) for k, location in self.index if k == key]

    def display(self):
        print("Dense Index:")
        for key, location in self.index:
            print(f"Key: {key}, Record Location: {location}")
        print("End of Dense Index\n")
    
    def delete(self, key):
        self.index = [(k, location) for k, location in self.index if k != key]


   
    


index_dense = DenseIndex()
def filling_hash_table_dense(tree):
    index_dense.index.clear()
    print(index_dense.index)
    connection = database_connection()
    data = fetch_data_from_database(connection)

    for item in data:
        index_dense.add_entry(item[3], item)
    print(index_dense.index)
    for key, value in index_dense.index:
        tree.insert('', 'end', values=(key, value))
    tree.pack()

# search function
def search_dense(search_entry,tree):
    year = search_entry
    resualt = index_dense.search_all(year)
    tree.delete(*tree.get_children())
    for key, value in resualt:
        tree.insert('', 'end', values=(key, value))
    tree.pack()

# delete function 
def delete_dense(delete_entry , tree):
    year = delete_entry
    print(year)
    index_dense.delete(year)
    tree.delete(*tree.get_children())
    for key, value in index_dense.index:
        tree.insert('', 'end', values=(key, value))
    tree.pack()
    connection = database_connection()
    delete_book(connection, id)

def insert_item_dense(title , author,year , genre, treeHash ):
  
    connection = database_connection()
    
    insert_book(connection, title, author, year, genre)
    treeHash.delete(*treeHash.get_children())
    filling_hash_table_dense(treeHash)
    index_dense.index.clear()
    for key, value in index_dense.index:
        treeHash.insert('', 'end', values=(key, value))
    treeHash.pack()
    