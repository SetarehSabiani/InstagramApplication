from ttkbootstrap import Window, Button, Label, Entry,Treeview,SUCCESS,PRIMARY,INFO,DANGER,OUTLINE
from ttkbootstrap.dialogs import Messagebox
from jsonplaceholder_apis import get_post_list, create_post, update_post, delete_post, get_comment_list

window = Window(title="Instagram Application",themename="journal",iconphoto="insta.png")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)


def show_post_form():
    post_form = Window(title="New Post Form")

    title_label = Label(post_form, text="title",bootstyle=PRIMARY)
    title_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

    title_entry = Entry(post_form, width=50,bootstyle=PRIMARY)
    title_entry.grid(row=0, column=1, pady=10, padx=(0, 20), sticky="w")

    body_label = Label(post_form, text="Body",bootstyle=DANGER)
    body_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="e")

    body_entry = Entry(post_form, width=50,bootstyle=DANGER)
    body_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 20), sticky="w")


    def submit():
        title = title_entry.get()
        body = body_entry.get()
        user_id = 10

        result = create_post(title, body, user_id)
        if result:
            post_form.destroy()
            load_post_list()

        else:
            Messagebox.show_error(title="Error", message="Invalid request")

    submit_button = Button(post_form, text="Submit", command=submit,bootstyle=SUCCESS)
    submit_button.grid(row=2, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

    post_form.mainloop()


new_post_button = Button(window, text="New Post", command=show_post_form,bootstyle=OUTLINE+SUCCESS)
new_post_button.grid(row=0, column=0, pady=10, padx=10)


def show_update_form():
    selected_items = post_treeview.selection()
    if not selected_items:
        Messagebox.show_warning("Warning", "Please select a post to update")
        return

    post_id = selected_items[0]
    current_values = post_treeview.item(post_id)['values']

    update_form = Window(title="Update Post Form")

    title_label = Label(update_form, text="Title")
    title_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

    title_entry = Entry(update_form, width=50)
    title_entry.grid(row=0, column=1, pady=10, padx=(0, 20), sticky="w")
    title_entry.insert(0, current_values[0])  # Insert current title

    body_label = Label(update_form, text="Body")
    body_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="e")

    body_entry = Entry(update_form, width=50)
    body_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 20), sticky="w")
    body_entry.insert(0, current_values[1])  # Insert current body

    def submit_update():
        new_title = title_entry.get()
        new_body = body_entry.get()

        result = update_post(post_id, new_title, new_body)
        if result:
            update_form.destroy()
            load_post_list()
        else:
            Messagebox.show_error(title="Error", message="Update failed")

    submit_button = Button(update_form, text="Update", command=submit_update)
    submit_button.grid(row=2, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

    update_form.mainloop()


update_post_button = Button(window, text="Update Post", command=show_update_form,bootstyle=OUTLINE+DANGER)
update_post_button.grid(row=0, column=1, pady=10, padx=10)


def delete_post_button():
    post_id_list = post_treeview.selection()
    for post in post_id_list:
        result = delete_post(post)
        if not result:
            Messagebox.show_error(title="Error", message="Invalid Request")

    load_post_list()


delete_post_button = Button(window, text="Delete Post", command=delete_post_button,bootstyle=OUTLINE+PRIMARY)
delete_post_button.grid(row=0, column=2, pady=10, padx=10)


def show_comment():
    post_id = post_treeview.selection()[0]
    comment_list = get_comment_list(post_id)

    comment_form = Window(title=f"Comment list Form ({post_id})")

    row_number = 0
    for comment in comment_list:
        comment_label = Label(comment_form, text=f"{comment['id']} - {comment['body']} ({comment['email']})")
        comment_label.grid(row=row_number, column=0, pady=10, padx=10)
        row_number = row_number + 1

    comment_form.mainloop()


show_comment_button = Button(window, text="Show Comment", command=show_comment,bootstyle=OUTLINE+INFO)
show_comment_button.grid(row=0, column=3, pady=10, padx=10)

post_treeview = Treeview(window, columns=("title", "body", "user_id"),bootstyle=PRIMARY)
post_treeview.heading("#0", text="ID")
post_treeview.heading("#1", text="Title")
post_treeview.heading("#2", text="Body")
post_treeview.heading("#3", text="User ID")
window.rowconfigure(1, weight=1)

post_treeview.grid(row=1, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="nsew")

item_list = []


def load_post_list():
    post_list = get_post_list()
    for item in item_list:
        post_treeview.delete(item)
    for post in post_list:
        item = post_treeview.insert("", "end", text=post["id"],
                                    values=(post["title"], post["body"], post["title"], post["userId"]), iid=post["id"])
        item_list.append(item)


load_post_list()

window.mainloop()