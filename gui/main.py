import customtkinter

customtkinter.set_appearance_mode("dark");
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("500x350")


def searchPart():
  print("Test")


frame = customtkinter.CTkFrame(master=root);
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Parça Sorgulama", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="OEM NO")
entry1.pack(pady=12, padx=10)


button = customtkinter.CTkButton(master=frame, text="Parçayı Bul", command=searchPart)
button.pack(pady=12, padx=10)




root.mainloop()



