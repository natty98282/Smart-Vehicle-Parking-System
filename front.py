from tkinter import *
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk
import cv2
import pickle
import cvzone
import numpy as np

class Smart_Parking_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Smart Parking System")

        img = Image.open(r"C:\Users\natty\Desktop\VehicleParkig\photodata\VistaTouch400.jpg")
        img = img.resize((1530, 790), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=1500, height=790)

        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(bg_img, text="Smart Vehicle Parking System", bg="white",
                          font=("times new roman", 35, "bold"), fg="darkblue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img4 = Image.open(r"C:\Users\natty\Desktop\VehicleParkig\photodata\pp.PNG")
        img4 = img4.resize((220, 220), Image.ANTIALIAS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img,command=self.parking, image=self.photoimg4,  cursor="hand2")
        b1.place(x=400, y=100, width=220, height=220)

        b1_1 = Button(bg_img,command=self.parking, text="Start_Parking_Camera",cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="darkblue", fg="gray")
        b1_1.place(x=400, y=300, width=220, height=40)

        img5 = Image.open(r"C:\Users\natty\Desktop\VehicleParkig\photodata\9.jpg")
        img5 = img5.resize((300, 130), Image.ANTIALIAS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b2 = Button(bg_img,command=self.iExit,  image=self.photoimg5, cursor="hand2")
        b2.place(x=800, y=100, width=220, height=220)

        b2_1 = Button(bg_img,  text="EXIT", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="gray")
        b2_1.place(x=800, y=300, width=220, height=40)

    def parking(self):
        cap = cv2.VideoCapture('carPark.mp4')

        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)

        width, height = 107, 48

        def checkParkingSpace(imgPro):
            spaceCounter = 0

            for pos in posList:
                x, y = pos

                imgCrop = imgPro[y:y + height, x:x + width]
                # cv2.imshow(str(x * y), imgCrop)
                count = cv2.countNonZero(imgCrop)

                if count < 900:
                    color = (0, 255, 0)
                    thickness = 5
                    spaceCounter += 1
                else:
                    color = (0, 0, 255)
                    thickness = 2

                cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
                cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                                   thickness=2, offset=0, colorR=color)

            cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (0, 50), scale=3,
                               thickness=5, offset=20, colorR=(0, 0, 0))
            if spaceCounter > 0:
                cvzone.putTextRect(img, f'There : {spaceCounter} Free lines', (390, 50), scale=4,
                                   thickness=5, offset=20, colorR=(0, 0, 0))

        while True:

            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16)
            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            checkParkingSpace(imgDilate)
            cv2.imshow("Image", img)
            cv2.waitKey(10)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
    def iExit(self):
        self.iExit=askyesno("Smart Parking System","Do you want to exit")
        if self.iExit >0:
            self.root.destroy()
        else:
            return




if __name__ == "__main__":
    root = Tk()
    obj = Smart_Parking_System(root)
    root.mainloop()