# Importing the requited python libraries:

import cv2
from PyQt5.QtWidgets import QCheckBox, QMainWindow, QApplication, QLabel, QPushButton, QFileDialog, QProgressBar, QLineEdit, QToolButton, QRadioButton, QMessageBox
from PyQt5 import uic
from PyQt5 import QtGui
import sys
import math
import time
import os
import shutil
import random
from augment import augment


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()


        # Load the ui file
        uic.loadUi("Patchify.ui", self)

        # Set Main Window Title and Icon:
        self.setWindowTitle('Patchify App')
        self.setWindowIcon(QtGui.QIcon('crop_icon.png'))

        # Define the created widgets from ui file into python file.
        # (1) MainWindow;
        self.window_main = self.findChild(QMainWindow, 'PatchifyApp')


        # (2) PushButtons:
        self.btn_start = self.findChild(QPushButton, 'pushButton_1')
        self.btn_cancel = self.findChild(QPushButton, 'pushButton_2')


        # (3)  ToolButtons:
        self.btn_input = self.findChild(QToolButton, 'toolButton_1')
        self.btn_export = self.findChild(QToolButton, 'toolButton_2')


        # (4)  Labels:
        self.progress_label = self.findChild(QLabel, 'label')
        self.progress_label.setText('Patchify is waiting for orders!')


        # (5)  lineEdits:
        self.lineEdit_input = self.findChild(QLineEdit, 'lineEdit_1')
        self.lineEdit_export = self.findChild(QLineEdit, 'lineEdit_2')
        self.lineEdit_winx = self.findChild(QLineEdit, 'lineEdit_3')
        self.lineEdit_winy = self.findChild(QLineEdit, 'lineEdit_4')
        self.lineEdit_stridex = self.findChild(QLineEdit, 'lineEdit_5')
        self.lineEdit_stridey = self.findChild(QLineEdit, 'lineEdit_6')
        self.lineEdit_outname = self.findChild(QLineEdit, 'lineEdit_7')
        self.lineEdit_train = self.findChild(QLineEdit, 'lineEdit_8')
        self.lineEdit_test = self.findChild(QLineEdit, 'lineEdit_9')
        self.lineEdit_valid = self.findChild(QLineEdit, 'lineEdit_10')


        # (6)  RadioButtons:
        self.radio_all = self.findChild(QRadioButton, 'radioButton_1')
        self.radio_custom = self.findChild(QRadioButton, 'radioButton_2')
        

        # (7)  CheckBoxes:
        self.check_original = self.findChild(QCheckBox, 'checkBox_1')
        self.check_rotate90 = self.findChild(QCheckBox, 'checkBox_2')
        self.check_rotate180 = self.findChild(QCheckBox, 'checkBox_3')
        self.check_rotate270 = self.findChild(QCheckBox, 'checkBox_4')
        self.check_flipv = self.findChild(QCheckBox, 'checkBox_5')
        self.check_fliph = self.findChild(QCheckBox, 'checkBox_6')
        self.check_flipvh = self.findChild(QCheckBox, 'checkBox_7')
        

        # Define Signal and Slots:
        self.radio_all.toggled.connect(self.allChecked)
        self.radio_custom.toggled.connect(self.customChecked)
        self.btn_cancel.clicked.connect(self.exitApp)
        self.btn_input.clicked.connect(self.pickImage)
        self.btn_export.clicked.connect(self.pickSavingFolder)
        self.btn_start.clicked.connect(self.patchifying)

        # Make the radioButton for all the augmentation methods on by default.
        self.radio_all.setChecked(True)
        self.allChecked()


        # Define Default values
        self.Train_val = 0
        self.Test_val = 0
        self.Valid_val = 0
        self.list_of_saved_names = []

        # Show the App
        self.show()

    # Slot functions:
    def allChecked(self):
        '''This function makes all the checkBoxes checked! and makes them disabled for being checked by the user.'''
        # Make all checked:
        self.check_original.setChecked(True)
        self.check_rotate90.setChecked(True)
        self.check_rotate180.setChecked(True)
        self.check_rotate270.setChecked(True)
        self.check_flipv.setChecked(True)
        self.check_fliph.setChecked(True)
        self.check_flipvh.setChecked(True)
        # Make all disabled:
        self.check_original.setEnabled (False)
        self.check_rotate90.setEnabled (False)
        self.check_rotate180.setEnabled (False)
        self.check_rotate270.setEnabled (False)
        self.check_flipv.setEnabled (False)
        self.check_fliph.setEnabled (False)
        self.check_flipvh.setEnabled (False)


    def customChecked(self):
        '''This function makes all the checkBoxes unchecked! and makes them Enabled for being checked by the user.'''
        # Make all checked:
        self.check_original.setChecked(False)
        self.check_rotate90.setChecked(False)
        self.check_rotate180.setChecked(False)
        self.check_rotate270.setChecked(False)
        self.check_flipv.setChecked(False)
        self.check_fliph.setChecked(False)
        self.check_flipvh.setChecked(False)
        # Make all disabled:
        self.check_original.setEnabled (True)
        self.check_rotate90.setEnabled (True)
        self.check_rotate180.setEnabled (True)
        self.check_rotate270.setEnabled (True)
        self.check_flipv.setEnabled (True)
        self.check_fliph.setEnabled (True)
        self.check_flipvh.setEnabled (True)

    def exitApp(self):
        '''This function is for exiting the App.'''
        sys.exit()

    def pickImage(self):
        '''This function picks and image by using a openDialogFileName.'''
        self.image_filename, _ = QFileDialog.getOpenFileName(self, "Select an Image", "C://", "tif file (*.tif);;png file (*.png);;jpg file (*.jpg)")
        self.imageNamePassifix = self.image_filename.split(".")[-1]
        self.imageName = self.image_filename.split("/")[-1].split(".")[0]
        

        if self.image_filename:
            self.lineEdit_input.setText(self.image_filename)
        

    def pickSavingFolder(self):
        self.saving_folder_name = QFileDialog.getExistingDirectory(self, "Select a Folder", "")
        
        if self.saving_folder_name:
            self.lineEdit_export.setText(self.saving_folder_name)
    # ************************************************************************************************************
    def check_for_mandatory_fillings(self, filed_name):
        ''' This function check if the mandatory filds are filled or not! and if not it opens an messageBox!
        Param: filed_name >> is the name of the unfilled field. '''

        msg = QMessageBox()
        msg.setWindowTitle('Incomplete form!')
        msg.setText(f"{filed_name} has left unfilled!")
        msg.setIcon(QMessageBox.Critical)
        
        x = msg.exec_()
    
    def popupIncorrect(self, message):
        '''This function pops up when the user provides an incorrect value.

        Param: message >> gets string and print it in the popup messageBox.
        '''
        msg = QMessageBox()
        msg.setWindowTitle('Incomplete data insertion!')
        msg.setWindowIcon(QtGui.QIcon('crop_icon_spare.png'))
        msg.setText(f"{message} is provided")
        msg.setIcon(QMessageBox.Critical)
        
        y = msg.exec_()

    def popupIncorrectValue(self):
        '''This function checks the provided values of the Train, Test, and Validation datasets.
        '''
        msg = QMessageBox()
        msg.setWindowTitle('Incorrect data insertion!')
        msg.setText(" Total Percentage for all Train, Test, and Validation needs to be 100\n Their value cannot exceed 100.\n Their addition can be exactly equal to 100.\n In case, one of the fileds remains unfilled, it will be considered as 0!")
        msg.setIcon(QMessageBox.Critical)
        
        z = msg.exec_()


    def popupIncorrectCharacterInsersion(self, name):
        msg = QMessageBox()
        msg.setWindowTitle('Incorrect data insertion!')
        msg.setText(f"{name} should be inserted as a positive integer.")
        msg.setIcon(QMessageBox.Critical)
        
        g = msg.exec_()
    
    def patchifying(self):
        # Load the image:
        # (1) Check if the filepath for input image is filled.
        if not self.lineEdit_input.text():
            self.check_for_mandatory_fillings("Input Image")
        # (2) Check if the folderpath for storing the results is filled.
        elif not self.lineEdit_export.text():
            self.check_for_mandatory_fillings("Export Folder")
        # (3) Read the image if the filepath & the export folderpath are filled!
        else:
            self.image = cv2.imread(self.image_filename)
        
        # Calculating Dim, height, width, channel: 
        self.dim = self.image.ndim
        
        if self.dim == 2:
            self.Height, self.Width = self.image.shape[:2]
            self.channel = 1
        if self.dim == 3:
            self.Height, self.Width, self.channel = self.image.shape[:3]


        # Getting the user-defined Patch Step and Size:
        self.patchSize_x = int(self.lineEdit_winx.text())
        self.patchSize_y = int(self.lineEdit_winy.text())
    
        self.patchStep_x = int(self.lineEdit_stridex.text())
        self.patchStep_y = int(self.lineEdit_stridey.text())
        
        print(f"Image Height >>  {self.Height} \nImage Width >> {self.Width}")
        print(f"Patch Size Y >>  {self.patchSize_y} \nPatch Size X >> {self.patchSize_x}")


       
        # Mask a set of the index numbers for the checked augmentation methods
        self.selected_augment_methods = set()          # Creating an empty set which will filled by the selected augmentation methods' indexes.
        if self.check_original.isChecked():
            self.selected_augment_methods.update([0])
        
        if self.check_rotate90.isChecked():
            self.selected_augment_methods.update([1])

        if self.check_rotate180.isChecked():
            self.selected_augment_methods.update([2])

        if self.check_rotate270.isChecked():
            self.selected_augment_methods.update([3])

        if self.check_flipv.isChecked():
            self.selected_augment_methods.update([4])

        if self.check_fliph.isChecked():
            self.selected_augment_methods.update([5])

        if self.check_flipvh.isChecked():
            self.selected_augment_methods.update([6])
        
        # A name-list related to the available augmentation techniques according to their index numbers provided by augment method
        self.augment_passifixes = ['o', 'r90', 'r180', 'r270', 'fv', 'fh', 'fvh']

        # Check if the inserted percentages for sample division is correctly assigned.
        # (1) Check Train, Test, and Validation individually, where they cannot get strings, or integers more than 100.
        if self.lineEdit_train.text():
            if self.lineEdit_train.text().isnumeric():
                self.Train_val = int(self.lineEdit_train.text())
                if self.Train_val > 100:
                    self.popupIncorrectValue()
            elif not self.lineEdit_train.text().isnumeric():
                self.popupIncorrectCharacterInsersion('Train Percentage')            
        elif not self.lineEdit_train.text():
            self.Train_val = 0
        print(f'Train_val is {self.Train_val}')
        
        
        if self.lineEdit_test.text():
            if self.lineEdit_test.text().isnumeric():
                self.Test_val = int(self.lineEdit_test.text())
                if self.Test_val > 100:
                    self.popupIncorrectValue()
            elif not self.lineEdit_test.text().isnumeric():
                self.popupIncorrectCharacterInsersion('Test Percentage')            
        elif not self.lineEdit_test.text(): 
            self.Test_val = 0
        print(f'Test_val is {self.Test_val}')

        if self.lineEdit_valid.text():
            if self.lineEdit_valid.text().isnumeric():
                self.Valid_val = int(self.lineEdit_valid.text())
                if self.Valid_val > 100:
                    self.popupIncorrectValue()
            elif not self.lineEdit_valid.text().isnumeric():
                self.popupIncorrectCharacterInsersion('Validation Percentage')
        elif not self.lineEdit_valid.text(): 
            self.Valid_val = 0
        print(f'Valid_val is {self.Train_val}')

        # (2) check if the summation of all three is 100.
        if (self.Train_val + self.Test_val + self.Valid_val) != 100:
            self.popupIncorrectValue()
        elif ((self.Train_val + self.Test_val + self.Valid_val) == 100) or ((self.Train_val + self.Test_val + self.Valid_val) == 0):
            self.total_path = os.path.join(self.saving_folder_name + "//" + "Total")
            os.mkdir(self.total_path)


            # Starting to crop and then augment the patches and finally save them.
            if self.patchSize_y > self.Height or self.patchSize_x > self.Width:
                self.popupIncorrect("Patch size cannot exceed your image size!\n See your command line to get informed about the input image size!")

            elif self.patchSize_y <= self.Height and self.patchSize_x <= self.Width:


            # Counting the number of Steps in a row and a column to complete the cropping operations:
                self.steps_in_height = math.floor((self.Height - self.patchSize_y) / self.patchStep_y) + 1
                self.steps_in_width = math.floor((self.Width - self.patchSize_x) / self.patchStep_x) + 1
                
                
                self.num_of_crop = 0      # This is the number of cropped images during the operations
                for row in range(self.steps_in_height):
                    for col in range(self.steps_in_width):
                        # Cropping operations
                        self.num_of_crop += 1        # Counting the number of cropped images
                        # self.progressbar.setValue(self.num_of_crop)
                        if self.channel == 1:        # The cropping operation for 1-channel input image
                            self.crop_image = self.image[row*self.patchStep_y:row*self.patchStep_y+self.patchSize_y, col*self.patchStep_x:col*self.patchStep_x+self.patchSize_x]

                        elif self.channel >= 2:        # The cropping operation for n-channel input image
                            self.crop_image = self.image[row*self.patchStep_y:row*self.patchStep_y+self.patchSize_y, col*self.patchStep_x:col*self.patchStep_x+self.patchSize_x, :]
                        
                        # Augmenting the cropped image:
                        self.augment_list = augment(self.crop_image)
                        

                        # Saving the augmented forms of cropped image in the selected augment formats
                        for aug_idx in list(self.selected_augment_methods):
                            name_for_saving = str(self.num_of_crop) + "_" + self.lineEdit_outname.text() + "_" +  self.augment_passifixes[aug_idx] + "." + self.imageNamePassifix
                            fullpath_for_saving = self.total_path + "//" + name_for_saving
                            cv2.imwrite(fullpath_for_saving, self.augment_list[aug_idx])
                            self.list_of_saved_names.append(name_for_saving)         # Creating name of saved files in a list

                            # Calculating the percentage needed to accomplish the whole patching process.
                            self.percent_of_completion = math.floor((self.num_of_crop)/(self.steps_in_height * self.steps_in_width)*100)
                            time.sleep(.05)
                            self.progress_label.setText(f' {self.percent_of_completion}% is completed!')
                            QApplication.processEvents()


        # Making Train, Test, Validation dataset from created Total dataset.                
        if (self.Train_val + self.Test_val + self.Valid_val) == 100:
            # Once all cropped data is stored in the "Total" Directory, it is time to divide them into Train, Test, and Validation dataset.
            # All the cropped images' full filepath is stored in the list named "self.list_of_saved_names", 
            # we need to first randomize them and then store them in the Train, Test, and Validation directories with respect to the user-defined percentages.
            self.randomized = self.list_of_saved_names.copy()
            random.shuffle(self.randomized)

            # Check if the inserted values for Train, Test, Validation datasets are correct!.
            # Create the required directories for Train, Test, and Validation if their user-defined value is greater than zero.
            if self.Train_val == 0:
                if self.Test_val == 0 and self.Valid_val == 100:
                    self.num_tobe_assigned_Valid = len(self.randomized)
                    self.valid_path = os.path.join(self.saving_folder_name + "//" + "Validation")
                    os.mkdir(self.valid_path)
                elif self.Test_val == 100 and self.Valid_val == 0:
                    self.num_tobe_assigned_Test = len(self.randomized)
                    self.test_path = os.path.join(self.saving_folder_name + "//" + "Test")
                    os.mkdir(self.test_path)
                else:
                    self.num_tobe_assigned_Test = math.floor((self.Test_val/100)* len(self.randomized))
                    self.num_tobe_assigned_Valid = len(self.randomized) - self.num_tobe_assigned_Test
                    self.num_tobe_assigned_Train = 0
                    self.test_path = os.path.join(self.saving_folder_name + "//" + "Test")
                    os.mkdir(self.test_path)
                    self.valid_path = os.path.join(self.saving_folder_name + "//" + "Validation")
                    os.mkdir(self.valid_path)

            elif self.Test_val == 0:
                if self.Valid_val == 0 and self.Train_val == 100:
                    self.num_tobe_assigned_Train = len(self.randomized)
                    self.train_path = os.path.join(self.saving_folder_name + "//" + "Train")
                    os.mkdir(self.train_path)
                else:
                    self.num_tobe_assigned_Train = math.floor((self.Train_val/100)* len(self.randomized))
                    self.num_tobe_assigned_Valid = len(self.randomized) - self.num_tobe_assigned_Train
                    self.num_tobe_assigned_Test = 0
                    self.train_path = os.path.join(self.saving_folder_name + "//" + "Train")
                    os.mkdir(self.train_path)
                    self.valid_path = os.path.join(self.saving_folder_name + "//" + "Validation")
                    os.mkdir(self.valid_path)


            elif self.Valid_val == 0:
                self.num_tobe_assigned_Train = math.floor((self.Train_val/100)* len(self.randomized))
                self.num_tobe_assigned_Test = len(self.randomized) - self.num_tobe_assigned_Train
                self.num_tobe_assigned_Valid = 0
                self.train_path = os.path.join(self.saving_folder_name + "//" + "Train")
                os.mkdir(self.train_path)
                self.test_path = os.path.join(self.saving_folder_name + "//" + "Test")
                os.mkdir(self.test_path)
                

            else:
                self.num_tobe_assigned_Train = math.floor((self.Train_val/100)* len(self.randomized))
                what_is_left = len(self.randomized) - self.num_tobe_assigned_Train
                self.num_tobe_assigned_Test =  math.floor((self.Test_val/(self.Test_val + self.Valid_val)) * what_is_left) 
                self.num_tobe_assigned_Valid = what_is_left - self.num_tobe_assigned_Test
                self.train_path = os.path.join(self.saving_folder_name + "//" + "Train")
                os.mkdir(self.train_path)
                self.test_path = os.path.join(self.saving_folder_name + "//" + "Test")
                os.mkdir(self.test_path)
                self.valid_path = os.path.join(self.saving_folder_name + "//" + "Validation")
                os.mkdir(self.valid_path)
            
            # (3) Dividing and Storing dataset on created Train, Test, and Validation directories.
            # - Updating Progress Label for the data division section.
            self.progress_label.setText('Division section is Starting...')
            QApplication.processEvents()       # Avoid Freezing the GUI while asks for the updates on the progress label.
            time.sleep(3)

            self.percent_of_completion = 0     # Reseting the precent of completion
            self.progress_label.setText(f'Process of dataset devision: {self.percent_of_completion}% is completed!')
            QApplication.processEvents()       # Avoid Freezing the GUI while asks for the updates on the progress label.


            saved_counting = 0
            total_number = len(self.randomized)

            # Storing samples in the Train directory.
            for _ in range(self.num_tobe_assigned_Train):
                fileName = self.randomized.pop(0)
                shutil.copy2(self.total_path+"//"+fileName, self.train_path+"//"+fileName)
                saved_counting +=1
                self.percent_of_completion = math.floor((saved_counting)/(total_number)*100)
                self.progress_label.setText(f' {self.percent_of_completion}% is completed!')
                QApplication.processEvents()

            # Storing samples in the Test directory.
            for _ in range(self.num_tobe_assigned_Test):
                fileName = self.randomized.pop(0)
                shutil.copy2(self.total_path+"//"+fileName, self.test_path+"//"+fileName)
                saved_counting +=1
                self.percent_of_completion = math.floor((saved_counting)/(total_number)*100)
                self.progress_label.setText(f'Process of dataset devision: {self.percent_of_completion}% is completed!')
                QApplication.processEvents()

            # Storing samples in the Validation directory.
            for _ in range(self.num_tobe_assigned_Valid):
                fileName = self.randomized.pop(0)
                shutil.copy2(self.total_path+"//"+fileName, self.valid_path+"//"+fileName)
                saved_counting +=1
                self.percent_of_completion = math.floor((saved_counting)/(total_number)*100)
                self.progress_label.setText(f'Process of dataset devision: {self.percent_of_completion}% is completed!')
                QApplication.processEvents()

          


# Initialize The App:
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
