from tkinter import filedialog
from io import BytesIO
from PIL import Image, ImageTk
from picDesigner import PictureViewer

class PicApp(PictureViewer):
    def __init__(self, nw, nr, ns):
        super().__init__()
        self.nw = nw
        self.nr = nr
        self.ns = ns
        self.photo = None
        self.width = None
        self.height = None
        

    def lam(self):
        try:
            s = "TAKE"
            self.nw.write(s + '\n')
            self.nw.flush()

            s = self.nr.readline().strip()
            data = self.ns.read(int(s))

            img_byte_array = BytesIO(data)
            opened_image = Image.open(img_byte_array)

            desired_width = 600
            aspect_ratio = opened_image.width / opened_image.height
            desired_height = int(desired_width / aspect_ratio)
            self.width = desired_width
            self.height = desired_height
            resized_image = opened_image.resize((desired_width, desired_height), Image.ANTIALIAS)

            self.photo = ImageTk.PhotoImage(resized_image)

            self.picture.config(image=self.photo)
        except FileNotFoundError as fnf_error:
            print(fnf_error)


    def butTake_Click(self):
        self.lam()

    
    def button1_Click(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                pil_image = Image.new("RGB", (self.width, self.height))
                pil_image.paste(ImageTk.getimage(self.photo), (0, 0))
                
                pil_image.save(file_path)
            except Exception as e:
                print(e)

    def pic_closing(self):
        s = "QUIT"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.destroy()
