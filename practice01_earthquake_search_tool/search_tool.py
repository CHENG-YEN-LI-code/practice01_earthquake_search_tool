import pymongo
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv
load_dotenv()

mongourl=os.getenv('mongourl')
cluster=pymongo.MongoClient(mongourl)
coll=cluster['tw_earthquake_db']['tw_earthquake_coll']

root=tk.Tk()
root.geometry("800x800")
root.title('tw_earthquake_search_tool')
main_frame=tk.Frame(root,padx=10,pady=10)
main_frame.grid(row=0,column=0)

title_label=tk.Label(main_frame,text="TW Earthquake Search tool",font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, pady=10)

county_label=tk.Label(main_frame,text="CountyName：",font=("Arial", 11))
county_label.grid(row=1, column=0,pady=5)
county_var=tk.StringVar()
county_option=[
    'Taipei City',
    'New Taipei City',
    'Taoyuan City',
    'Taichung City',
    'Tainan City',
    'Kaohsiung City',
    'Changhua County',
    'Chiayi County',
    'Hsinchu County',
    'Hualien County',
    'Miaoli County',
    'Nantou County',
    'Pingtung County',
    'Taitung County',
    'Yilan County',
    'Yunlin County',
    'Penghu County',
    'Keelung City',
    'Hsinchu City',
    'Chiayi City',
    'Kinmen County',
    'Lienchiang County'
]
county_combobox=ttk.Combobox(
    main_frame,
    textvariable=county_var,
    values=county_option,
    state="readonly",
    width=30
)
county_combobox.current(0)
county_combobox.grid(row=1,column=1,pady=5)

min_label=tk.Label(main_frame,text="MagnitudeValue Min:",font=("Arial", 11))
min_label.grid(row=2,column=0,pady=5)
max_label=tk.Label(main_frame,text="MagnitudeValue Max:",font=("Arial", 11))
max_label.grid(row=3,column=0,pady=5)
min_spinbox=tk.Spinbox(
    main_frame,
    from_=-5.0,
    to=10.0,
    increment=0.5,
    width=15
)
max_spinbox=tk.Spinbox(
    main_frame,
    from_=-5.0,
    to=10.0,
    increment=0.5,
    width=15
)
min_spinbox.grid(row=2,column=1,pady=5)
max_spinbox.grid(row=3,column=1,pady=5)
max_spinbox.delete(0, "end")
max_spinbox.insert(0, "10.0")



answer_frame=tk.Frame(root,padx=10,pady=10)
answer_frame.grid(row=1,column=0)
answer_box=tk.Text(answer_frame,font=("Arial", 12),width=80,wrap="word")
answer_box.grid(row=0,column=0,sticky='ns',pady=5)
scrollbar=ttk.Scrollbar(answer_frame,command=answer_box.yview)
scrollbar.grid(row=0,column=1,sticky='ns')
answer_box.configure(yscrollcommand=scrollbar.set)

def get_data():
    try:
        county=county_var.get()
        min_=float(min_spinbox.get())
        max_=float(max_spinbox.get())
        answer=list(coll.find(
            {'CountyName':{"$regex": county},
            "MagnitudeValue": {"$gte": min_, "$lte": max_}}
        ))
        if not answer:
            answer_box.delete("1.0",tk.END)
            answer_box.insert('1.0','no data')

        else:
            all_items=[]
            for item in answer:
                oneitem=[]
                for k,v in item.items():
                    if k=='_id':
                        continue
                    oneitem.append(f'{k} = {v}')
                oneitem_text='\n\n'.join(oneitem)
                all_items.append(oneitem_text)
            last_answer='\n\n==================\n\n'.join(all_items)
            answer_box.delete('1.0',tk.END)
            answer_box.insert('1.0',last_answer)
    except Exception as err:
        answer_box.delete('1.0',tk.END)
        answer_box.insert('1.0',f'Error.{type(err).__name__}')
search_button=tk.Button(main_frame,text='search',width=10,command=get_data)
search_button.grid(row=4,column=0,pady=5)

root.mainloop()
