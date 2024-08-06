
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 14:04:25 2024

@author: Administrator
"""

import tkinter as tk
from tkinter import messagebox
import subprocess 



class ColorfulButtonsApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x400")  # Width x Height
        self.root.title("Main GUI")

        # Define button configurations with labels, colors, and callback functions
        button_configs = [
            ("O- Sample creation", "purple", self.on_purple_button_click)
            ("1- Annotation", "lightcoral", self.on_red_button_click),
            ("2- Training", "lightsalmon", self.on_green_button_click),
            ("3- Prediction", "orchid", self.on_blue_button_click),
            ("4- Combine prediction with movie", "yellow", self.on_yellow_button_click),
            
        ]

        # Create and pack buttons
        for label, color, command in button_configs:
            button = tk.Button(self.root, text=label, bg=color, fg="black", padx=50, pady=10, command=command)
            button.pack(pady=5)

    # Define callback functions for each button
    def on_red_button_click(self):
        #run annotation algoritm
       print(1)
       self.root.destroy()

    def on_green_button_click(self):
       #run training algoritm
      print(2)
      self.root.destroy()

    def on_blue_button_click(self):
        #run prediction algoritm
        print(3)
        self.root.destroy()

    def on_yellow_button_click(self):
        #run prediction plus movie algoritm
        print(4)
        self.root.destroy()

    def on_purple_button_click(self):
        #sample creation for annotation- choosing images
        print(5)
        self.root.destroy()