import tkinter as tk
from tkinter import ttk
from Hachage.Chaînage_séparé import *
from Hachage.Double_Hachage import *
from Hachage.Essai_linéaire import *
from Index.IndexCreux import *
from Index.IndexDense import *
from ArbreBplus.Arbres import *
from PIL import ImageTk, Image
######################################
root = tk.Tk()
root.geometry('700x690')
root.title('BDDPROJECT')  # A changer !

# Empecher la redimension de la fenêtre
root.resizable(width=False, height=False)

##########################################################################
# 1. Notre menu :
menu = tk.Frame(root) 
menu.pack()
menu.pack_propagate(False)  # so I can change the width and height below
menu.configure(width=700, height=60)

#switch menu :

def switch(line ,page):
    for child in menu.winfo_children():    
        if isinstance(child,tk.Label):
            child['bg']='SystemButtonFace'

      
    
    line['bg']='#363062'     
    for fm in main_fm.winfo_children():
        fm.destroy() 
        root.update()
    page()
    
#home
def home_page():
    home_page=tk.Frame(main_fm)
    home_lb=tk.Label(home_page,text=' ACCEUIL ',font=('Impact',15,'bold'), bg='#363062' ,fg='#f5f5f5' ,bd=3)
    home_lb.pack(fill=tk.BOTH , pady=30)
    home_page.pack(fill=tk.BOTH, expand=True) 
    title=tk.Label(home_page ,text="Bibliothèque des livres : ",**font_label )
    title.place(x=10 , y=120)
    record_frame=tk.Frame(home_page)
    record_frame.place(x=25 ,y=160)
    record_frame.pack_propagate(False)
    record_frame.configure(width=650 ,height=220)
    record_table=ttk.Treeview(record_frame, columns=("ID", "Title", "Author","Publication Year","Genre"), show="headings")
    record_table.heading("ID", text="ID")
    record_table.heading("Title", text="Title")
    record_table.heading("Author", text="Author")
    record_table.heading("Publication Year", text="Publication Year")
    record_table.heading("Genre", text="Genre")
    record_table.column("ID", width=20)
    record_table.column("Title", width=250)
    record_table.column("Author", width=150)
    record_table.column("Publication Year", width=115)
    record_table.column("Genre", width=115)
    record_table.pack(fill=tk.X ) 

    connection = database_connection()
    data = fetch_data_from_database(connection)
    for item in record_table.get_children():
        record_table.delete(item)
    for row in data:
            record_table.insert("", "end", values=row)

    
#hachage 
def hachage_page():
    hachage_page=tk.Frame(main_fm)
    heading_lb=tk.Label(hachage_page,text='Algorithme: Hachage' ,font=('Impact',15,'bold'), bg='#363062' ,fg='#f5f5f5' ,bd=3)
    heading_lb.pack( fill=tk.BOTH , pady=30)

    ####
    select_label= tk.Label(hachage_page,text="Choisissez le type de l'algorithme souhaité:  ",**font_label)
    select_label.place(x=40,y=80)
    # Options à afficher dans la combobox 
    options = ["Essai lineaire", "Double hachage", "Chaînage séparé"]
    combo = ttk.Combobox(hachage_page, values=options, state='readonly')
    combo.place(x=40, y=80)

    default_option = "Essai lineaire"
    default_index = options.index(default_option)
    combo.current(default_index)
    combo.place( x=40 , y=110)
    
    def on_select(event):
        selected_value = combo.get()
        print(selected_value)
        if selected_value == "Essai lineaire":
            record_table.delete(*record_table.get_children())
            filling_hash_table_essai(record_table)
        elif selected_value == "Double hachage":
            record_table.delete(*record_table.get_children())
            filling_hash_table_double(record_table)
        elif selected_value == "Chaînage séparé":
            record_table.delete(*record_table.get_children())
            filling_hash_table_separe(record_table)
            
        def search():
            selected_value = combo.get()
            if selected_value == "Essai lineaire":
                search_essai(search_input.get(),record_table) 
                search_input.delete(0, tk.END)
            elif selected_value == "Double hachage":
                search_double_hachage(search_input.get(),record_table)  
                search_input.delete(0, tk.END)
            elif selected_value == "Chaînage séparé":
                search_chaine_separee(search_input.get(),record_table)
                search_input.delete(0, tk.END)
        
        def delete():
            selected_value = combo.get()
            if selected_value == "Essai lineaire":
                delete_essai(search_input.get(),record_table) 
                search_input.delete(0, tk.END)
            elif selected_value == "Double hachage":
                delete_double_hachage(search_input.get(),record_table)  
                search_input.delete(0, tk.END)
            elif selected_value == "Chaînage séparé":
                delete_chaine_separee(search_input.get(),record_table)  
                search_input.delete(0, tk.END)
        def add():
            selected_value = combo.get()
            title = title_input.get()
            author = author_input.get()
            year = year_user_input.get()
            genre = genre_user_input.get()
            if selected_value == "Essai lineaire":
                insert_item_essai(title , author,year , genre, record_table )
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END) 
            if selected_value == "Double hachage":
                insert_item_Double(title , author,year , genre, record_table )
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END)    
            if selected_value == "Chaînage séparé":
                insert_item_separe(title , author,year , genre, record_table )
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END)

        """def modify():
            selected_value = combo.get()
            if selected_value == "Essai lineaire":
                modify_item_essai(search_input.get(),title_input,author_input , year_user_input ,genre_user_input)""" 

        rechercher_button=tk.Button(hachage_page, font=("bold",13) ,text='Rechercher' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command=search)
        rechercher_button.place(x=290,y=370 ) 

        delete_button=tk.Button(hachage_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command=delete)
        delete_button.place(x=395,y=370 )  

        ajouter_button=tk.Button(hachage_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10' , command=add)
        ajouter_button.place(x=10 , y=310 ) 

        """modify_button=tk.Button(hachage_page, font=("bold",13) ,text='Modifier' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command = modify)
        modify_button.place(x=490,y=370 )"""
    
    combo.bind("<<ComboboxSelected>>", on_select)
    

    hachage_page.pack(fill=tk.BOTH, expand=True)  
    title=tk.Label(hachage_page ,text="Entrer le titre :",**font_label )
    title.place(x=10 , y=150)
    title_input=tk.Entry(hachage_page,font=("Bold",13))
    title_input.place(x=120, y=150)
    ###############################
    author=tk.Label(hachage_page ,text="Entrer l'auteur :",**font_label )
    author.place(x=10 , y=190)
    author_input=tk.Entry(hachage_page,font=("Bold",13))
    author_input.place(x=130, y=190)
    ####################
    year=tk.Label(hachage_page ,text="Entrer l'année de publication :",**font_label )
    year.place(x=10 , y=230)
    year_user_input=tk.Entry(hachage_page,font=("Bold",13))
    year_user_input.place(x=235, y=230)
    #############################
    genre=tk.Label(hachage_page ,text="Entrer le genre :",**font_label )
    genre.place(x=10 , y=270)
    genre_user_input=tk.Entry(hachage_page,font=("Bold",13))
    genre_user_input.place(x=135, y=270)
    
    ajouter_button=tk.Button(hachage_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10')
    ajouter_button.place(x=10 , y=310 ) 
    ###################recherchercher:
    search_frame=tk.Frame(hachage_page)
    search_frame.place(x=100 , y=350)
    search_frame.pack_propagate(False)
    search_frame.configure(width=190 ,height=50 )
    search_label=tk.Label(search_frame,text='Rechecher par ID :', **font_label)
    search_label.pack(anchor=tk.W)
    search_input=tk.Entry(search_frame, font=("Bold",13))
    search_input.pack(anchor=tk.W)
    rechercher_button=tk.Button(hachage_page, font=("bold",13) ,text='Rechercher' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command=lambda:search_essai(search_input.get()))
    rechercher_button.place(x=290,y=370 ) 
    delete_button=tk.Button(hachage_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    delete_button.place(x=395,y=370 )
    """modify_button=tk.Button(hachage_page, font=("bold",13) ,text='Modifier' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    modify_button.place(x=490,y=370 )"""
    ###ou la base de donnes va s afficher :
    record_frame=tk.Frame(hachage_page)
    record_frame.place(x=25 ,y=410)
    record_frame.pack_propagate(False)
    record_frame.configure(width=650 ,height=220)
    ####
    record_table=ttk.Treeview(record_frame, columns=("h(x)", "Item"), show="headings")
   
    record_table.heading("h(x)", text="h(x)")
    record_table.heading("Item", text="L'ELEMENT")
    
    record_table.column("h(x)", width=30 )
    record_table.column("Item", width=310)
    record_table.pack(fill=tk.X ) 

    

#arbres 
def arbre_page():
    arbre_page=tk.Frame(main_fm)
    arbre_lb=tk.Label(arbre_page,text='Algorithme : Les arbres',font=('Impact',15,'bold'),bg='#363062' ,fg='#f5f5f5' ,bd=3 )
    arbre_lb.pack(fill=tk.BOTH , pady=30)
    arbre_page.pack(fill=tk.BOTH, expand=True)  
    #########
    select_label= tk.Label(arbre_page,text="",**font_label)
    select_label.place(x=40 ,y=80)
    options = ["Arbre B+"]
    selected_option = tk.StringVar()
    combo = ttk.Combobox(arbre_page, values=options, textvariable=selected_option , state='readonly'   )
    
    default_option = "Arbre B+"
    default_index = options.index(default_option)
    combo.current(default_index)
    combo.place( x=40 , y=110)

    def display_image(image_path):
        png_image = Image.open(image_path)

        width, height = png_image.size
        aspect_ratio = width / height
        new_width = 650
        new_height = int(new_width / aspect_ratio)
        png_image = png_image.resize((new_width, new_height), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(png_image)

        for widget in record_frame.winfo_children():
            widget.destroy()

        image_label = tk.Label(record_frame, image=tk_image)
        image_label.image = tk_image
        image_label.pack(fill=tk.BOTH, expand=True)
    def on_select(event):
        selected_value = combo.get()
        print(selected_value)
        if selected_value == "Arbre B+":
            generating_arbre()
            image_path = "bplustree.png"  
            display_image(image_path)
        
        def delete():
            selected_value = combo.get()
            if selected_value == "Arbre B+":
                delete_arbre(search_input.get())
                for widget in record_frame.winfo_children():
                     widget.destroy()
                image_path = "bplustree.png"
                display_image(image_path)
            search_input.delete(0, tk.END)
            
        def add():
            selected_value = combo.get()
            title = title_input.get()
            author = author_input.get()
            year = year_user_input.get()
            genre = genre_user_input.get()
            if selected_value == "Arbre B+":
                insert_item_arbre(title , author,year , genre)
                for widget in record_frame.winfo_children():
                     widget.destroy()
                image_path = "bplustree.png"
                display_image(image_path)
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END) 
                
            
        
        delete_button=tk.Button(arbre_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command=delete)
        delete_button.place(x=290,y=370 )  

        ajouter_button=tk.Button(arbre_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10' , command=add)
        ajouter_button.place(x=10 , y=310 ) 


    combo.bind("<<ComboboxSelected>>", on_select)
    ############
    title=tk.Label(arbre_page ,text="Entrer le titre :",**font_label )
    title.place(x=10 , y=150)
    title_input=tk.Entry(arbre_page,font=("Bold",13))
    title_input.place(x=120, y=150)
    ###############################
    author=tk.Label(arbre_page ,text="Entrer l'auteur :",**font_label )
    author.place(x=10 , y=190)
    author_input=tk.Entry(arbre_page,font=("Bold",13))
    author_input.place(x=130, y=190)
    ####################
    year=tk.Label(arbre_page ,text="Entrer l'année de publication :",**font_label )
    year.place(x=10 , y=230)
    year_user_input=tk.Entry(arbre_page,font=("Bold",13))
    year_user_input.place(x=235, y=230)
    #############################
    genre=tk.Label(arbre_page ,text="Entrer le genre :",**font_label )
    genre.place(x=10 , y=270)
    genre_user_input=tk.Entry(arbre_page,font=("Bold",13))
    genre_user_input.place(x=135, y=270)

    ajouter_button=tk.Button(arbre_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10')
    ajouter_button.place(x=10 , y=310 ) 
    ###################recherchercher:
    
    search_frame=tk.Frame(arbre_page)
    search_frame.place(x=100 , y=350)
    search_frame.pack_propagate(False)
    search_frame.configure(width=190 ,height=50 )
    search_label=tk.Label(search_frame,text='Supprimer par Year :', **font_label)
    search_label.pack(anchor=tk.W)
    search_input=tk.Entry(search_frame, font=("Bold",13))
    search_input.pack(anchor=tk.W)
     
    delete_button=tk.Button(arbre_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    delete_button.place(x=290,y=370 )

    record_frame = tk.Frame(arbre_page, width=650, height=220)
    record_frame.place(x=25, y=410)
    record_frame.pack_propagate(False)

    
    


#indexage
def indexage_page():
    indexage_page=tk.Frame(main_fm)
    indexage_lb=tk.Label(indexage_page,text='Algorithme : Idexation',font=('Impact',15,'bold'),bg='#363062' ,fg='#f5f5f5' ,bd=3)
    indexage_lb.pack( fill=tk.BOTH , pady=30)
    indexage_page.pack(fill=tk.BOTH, expand=True)
    #########
    select_label= tk.Label(indexage_page,text="Choisissez le type de l'algorithme souhaité:  ",**font_label)
    select_label.place(x=40 ,y=80)
    options = ["Indexe Dense" , "Indexe Creux"]

    combo = ttk.Combobox(indexage_page, values=options, state='readonly'   )
    combo.place(x=40, y=80)
    #combo.set("Indexe Creux")  
    #combo.place(x=40 , y=110)

    default_option = "Indexe Dense"
    default_index = options.index(default_option)
    combo.current(default_index)
    combo.place( x=40 , y=110)

    def on_select(event ):
        selected_value = combo.get()
        print(selected_value)
        if selected_value == "Indexe Creux":
            record_table.delete(*record_table.get_children())
            filling_hash_table_creux(record_table)
        if selected_value == "Indexe Dense":
            record_table.delete(*record_table.get_children())
            filling_hash_table_dense(record_table)

        def search():
            selected_value = combo.get()
            if selected_value == "Indexe Creux":
                search_creux(search_input.get(),record_table) 
                search_input.delete(0, tk.END)
            if selected_value == "Indexe Dense":
                search_dense(search_input.get(),record_table) 
                search_input.delete(0, tk.END)

        def delete():
            selected_value = combo.get()
            if selected_value == "Indexe Creux":
                delete_creux(search_input.get(),record_table) 
                search_input.delete(0, tk.END)
            if selected_value == "Indexe Dense":
                delete_dense(search_input.get(),record_table) 
                search_input.delete(0, tk.END)


        def add():
            selected_value = combo.get()
            title = title_input.get()
            author = author_input.get()
            year = year_user_input.get()
            genre = genre_user_input.get()
            if selected_value == "Indexe Creux":
                insert_item_creux(title , author,year , genre, record_table )
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END) 
            if selected_value == "Indexe Dense":
                insert_item_dense(title , author,year , genre, record_table )
                title_input.delete(0, tk.END) 
                author_input.delete(0, tk.END) 
                year_user_input.delete(0, tk.END) 
                genre_user_input.delete(0, tk.END) 

        rechercher_button=tk.Button(indexage_page, font=("bold",13) ,text='Rechercher' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command=search)
        rechercher_button.place(x=290,y=370 ) 

        delete_button=tk.Button(indexage_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" , command = delete)
        delete_button.place(x=395,y=370 )  

        ajouter_button=tk.Button(indexage_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10' , command = add)
        ajouter_button.place(x=10 , y=310 ) 


    combo.bind("<<ComboboxSelected>>", on_select) 
    #les boutons :
    title=tk.Label(indexage_page ,text="Entrer le titre :",**font_label )
    title.place(x=10 , y=150)
    title_input=tk.Entry(indexage_page,font=("Bold",13))
    title_input.place(x=120, y=150)
    ###############################
    author=tk.Label(indexage_page ,text="Entrer l'auteur :",**font_label )
    author.place(x=10 , y=190)
    author_input=tk.Entry(indexage_page,font=("Bold",13))
    author_input.place(x=130, y=190)
    ####################
    year=tk.Label(indexage_page ,text="Entrer l'année de publication :",**font_label )
    year.place(x=10 , y=230)
    year_user_input=tk.Entry(indexage_page,font=("Bold",13))
    year_user_input.place(x=235, y=230)
    #############################
    genre=tk.Label(indexage_page ,text="Entrer le genre :",**font_label )
    genre.place(x=10 , y=270)
    genre_user_input=tk.Entry(indexage_page,font=("Bold",13))
    genre_user_input.place(x=135, y=270)

    ajouter_button=tk.Button(indexage_page, text='Ajouter', font=("Bold",13) ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d" ,width='10')
    ajouter_button.place(x=10 , y=310 ) 
    ###################recherchercher:
    search_frame=tk.Frame(indexage_page)
    search_frame.place(x=100 , y=350)
    search_frame.pack_propagate(False)
    search_frame.configure(width=190 ,height=50 )
    ##
    search_label=tk.Label(search_frame,text='Rechecher par Année:', **font_label)
    search_label.pack(anchor=tk.W)
    search_input=tk.Entry(search_frame, font=("Bold",13))
    search_input.pack(anchor=tk.W)
    search_button=tk.Button(indexage_page, font=("bold",13) ,text='Rechercher' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    search_button.place(x=290,y=370 )
    delete_button=tk.Button(indexage_page, font=("Bold",13) ,text='Supprimer',bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    delete_button.place(x=395,y=370 )
    """modify_button=tk.Button(indexage_page, font=("bold",13) ,text='Modifier' ,bg='#363062' ,fg="#f5f5f5" ,activebackground="#4d4c7d")
    modify_button.place(x=490,y=370 )"""
    ###ou la base de donnes va s afficher :
    record_frame=tk.Frame(indexage_page)
    record_frame.place(x=25 ,y=410)
    record_frame.pack_propagate(False)
    record_frame.configure(width=650 ,height=220)
    ####
    record_table=ttk.Treeview(record_frame, columns=("h(x)", "Item"), show="headings")
    # Define column headings
    record_table.heading("h(x)", text="Année de publication")
    record_table.heading("Item", text="L'ELEMENT")
    # Specify column widths
    record_table.column("h(x)", width=30 )
    record_table.column("Item", width=310)
    record_table.pack(fill=tk.X ) 
 
   
    
    #########################

                 





# Nos éléments de Menu :#########################################################################
btn_style = {'font': ('Impact', 15), 'bd': 0, 'fg': '#363062', 'activeforeground': '#4d4c7d'}
line_style = {'bg': '#363062'}
font_label={ 'font':("Goudy old style",13 ,'bold')}

home_btn = tk.Button(menu, text='Acceuil', **btn_style , command=lambda: switch(line=home_line ,page=home_page))
home_btn.place(x=0, y=15, width=175)
home_line = tk.Label(menu, **line_style)
home_line.place(x=22, y=50, width=130, height=2)


indexage_btn = tk.Button(menu, text='Indexation', **btn_style, command=lambda: switch(line=indexage_line ,page=indexage_page))
indexage_btn.place(x=175, y=15, width=175)
indexage_line = tk.Label(menu)
indexage_line.place(x=197, y=50, width=130, height=2)

hachage_btn = tk.Button(menu, text='Hachage', **btn_style , command=lambda: switch(line=hachage_line ,page=hachage_page))
hachage_btn.place(x=350, y=15, width=175)
hachage_line = tk.Label(menu)
hachage_line.place(x=372, y=50, width=130, height=2)

Arbres_btn = tk.Button(menu, text='Arbres', **btn_style , command=lambda: switch(line=Arbres_line ,page=arbre_page))
Arbres_btn.place(x=525, y=15, width=175)
Arbres_line = tk.Label(menu)
Arbres_line.place(x=547, y=50, width=130, height=2)
######################################################################################################


main_fm = tk.Frame(root)
main_fm.pack(fill=tk.BOTH, expand=True)
home_page()
root.mainloop()
