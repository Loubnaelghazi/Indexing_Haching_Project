select_label= tk.Label(arbre_page,text="",**font_label)
    select_label.place(x=40 ,y=80)
    options = ["arbre"]
    selected_option = tk.StringVar()
    combo = ttk.Combobox(arbre_page, values=options, textvariable=selected_option , state='readonly'   )
    
    default_option = "arbre"
    default_index = options.index(default_option)
    combo.current(default_index)
    combo.place( x=40 , y=110)