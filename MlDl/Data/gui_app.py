import tkinter as tk
from tkinter import ttk
import random
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

class FloatingButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text
        self.command = command
        
        # Configuration du canvas
        self.configure(
            width=300,
            height=50,
            bg='#2E1A47',
            highlightthickness=0
        )
        
        # Créer le bouton avec effet d'ombre
        self.shadow = self.create_rectangle(
            15, 15, 285, 45,
            fill='#4B2A77',
            outline='#4B2A77'
        )
        
        self.button = self.create_rectangle(
            10, 10, 280, 40,
            fill='#9370DB',
            outline='#9370DB'
        )
        
        self.button_text = self.create_text(
            145, 25,
            text=text,
            fill='white',
            font=('Helvetica', 14, 'bold')
        )
        
        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
        # Animation variables
        self.floating = False
        self.float_up = True
        self.after(50, self.animate)
    
    def animate(self):
        if self.floating:
            current_pos = self.coords(self.button)
            if self.float_up:
                dy = -0.2
            else:
                dy = 0.2
            
            self.move(self.button, 0, dy)
            self.move(self.button_text, 0, dy)
            
            if current_pos[1] <= 8:
                self.float_up = False
            elif current_pos[1] >= 12:
                self.float_up = True
        
        self.after(50, self.animate)
    
    def on_enter(self, event):
        self.floating = True
        self.itemconfig(self.button, fill='#8A2BE2')
        self.itemconfig(self.shadow, fill='#4B2A77')
    
    def on_leave(self, event):
        self.floating = False
        self.itemconfig(self.button, fill='#9370DB')
        self.coords(self.button, 10, 10, 280, 40)
        self.coords(self.button_text, 145, 25)
        self.itemconfig(self.shadow, fill='#4B2A77')
    
    def on_click(self, event):
        if self.command:
            self.command()
            self.itemconfig(self.button, fill='#7B68EE')
            self.after(100, lambda: self.itemconfig(self.button, fill='#9370DB'))

class YouTubeTitleGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Title Generator")
        
        # Configuration de la fenêtre
        self.root.geometry("900x700")
        self.root.configure(bg='#2E1A47')
        
        # Chargement du modèle et du tokenizer
        try:
            self.model = load_model('youtube_title_model.h5')
            with open('tokenizer.pkl', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            self.model_loaded = True
            print("Modèle chargé avec succès!")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            self.model_loaded = False
        
        # Style personnalisé
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#2E1A47')
        self.style.configure('Custom.TLabel',
                           font=('Helvetica', 12),
                           background='#2E1A47',
                           foreground='#E6E6FA')
        
        # Style de la barre de défilement
        self.style.configure("Custom.Horizontal.TScale",
                           background='#2E1A47',
                           troughcolor='#4B2A77',
                           slidercolor='#9370DB',
                           activecolor='#8A2BE2')
        
        # Frame principal
        main_frame = ttk.Frame(root, style='Custom.TFrame', padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre
        title_label = tk.Label(main_frame,
                             text="✨ YouTube Title Generator ✨",
                             font=('Helvetica', 28, 'bold'),
                             fg='#E0B0FF',
                             bg='#2E1A47')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Status
        status_text = "🟢 Modèle actif" if self.model_loaded else "⚡ Mode créatif"
        status_label = tk.Label(main_frame,
                              text=status_text,
                              font=('Helvetica', 10),
                              fg='#B19CD9',
                              bg='#2E1A47')
        status_label.grid(row=1, column=0, pady=(0, 30))
        
        # Zone de saisie
        input_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        input_frame.grid(row=2, column=0, pady=(0, 30), sticky=(tk.W, tk.E))
        input_frame.grid_columnconfigure(1, weight=1)
        
        input_label = tk.Label(input_frame,
                             text="💭 Votre idée:",
                             font=('Helvetica', 12),
                             fg='#E6E6FA',
                             bg='#2E1A47')
        input_label.grid(row=0, column=0, padx=(0, 15))
        
        self.input_text = tk.Entry(input_frame,
                                 font=('Helvetica', 14),
                                 width=50,
                                 bg='#4B2A77',
                                 fg='white',
                                 insertbackground='white',
                                 relief=tk.FLAT)
        self.input_text.insert(0, "Comment faire")
        self.input_text.grid(row=0, column=1, sticky=(tk.W, tk.E), ipady=8)
        
        # Paramètres
        params_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        params_frame.grid(row=3, column=0, pady=(0, 30), sticky=(tk.W, tk.E))
        params_frame.grid_columnconfigure(1, weight=1)
        
        words_label = tk.Label(params_frame,
                             text="🎯 Longueur:",
                             font=('Helvetica', 12),
                             fg='#E6E6FA',
                             bg='#2E1A47')
        words_label.grid(row=0, column=0, padx=(0, 15))
        
        self.words_var = tk.IntVar(value=5)
        self.words_scale = ttk.Scale(params_frame,
                                   from_=1,
                                   to=10,
                                   orient=tk.HORIZONTAL,
                                   variable=self.words_var,
                                   style="Custom.Horizontal.TScale")
        self.words_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Bouton flottant
        self.generate_button = FloatingButton(
            main_frame,
            "✨ Générer un titre magique ✨",
            self.generate_title
        )
        self.generate_button.grid(row=4, column=0, pady=(0, 30))
        
        # Zone de résultat
        result_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        result_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        result_label = tk.Label(result_frame,
                              text="✨ Titre généré:",
                              font=('Helvetica', 12),
                              fg='#E6E6FA',
                              bg='#2E1A47')
        result_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        self.result_text = tk.Text(
            result_frame,
            width=50,
            height=4,
            font=('Helvetica', 14),
            wrap=tk.WORD,
            bg='#4B2A77',
            fg='#E6E6FA',
            insertbackground='white',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.result_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Mode démo
        self.demo_words = [
            "YouTube", "incroyable", "tutoriel", "facile", "rapide", "2024",
            "meilleur", "comment", "faire", "créer", "apprendre", "découvrir"
        ]
        
        # Rendre la fenêtre redimensionnable
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
    
    def generate_with_model(self, seed_text, next_words):
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], padding='pre')
            predicted = np.argmax(self.model.predict(token_list, verbose=0))
            
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " " + output_word
        return seed_text
    
    def generate_demo(self, seed_text, num_words):
        title = seed_text
        for _ in range(num_words):
            title += " " + random.choice(self.demo_words)
        return title
    
    def generate_title(self):
        seed_text = self.input_text.get()
        num_words = self.words_var.get()
        
        if self.model_loaded:
            try:
                title = self.generate_with_model(seed_text, num_words)
            except Exception as e:
                print(f"Erreur lors de la génération: {e}")
                title = self.generate_demo(seed_text, num_words)
        else:
            title = self.generate_demo(seed_text, num_words)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, title)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeTitleGenerator(root)
    root.mainloop()
