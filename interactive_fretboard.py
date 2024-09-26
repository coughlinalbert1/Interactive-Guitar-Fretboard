import tkinter as tk
from tkinter import ttk
from board_info import TUNING_LIST, NOTES_SHARP, NOTES_FLAT, NOTE_COLOR, FRETBOARD_LENGTH
from keys import major_keys, minor_keys, harmonic_minor, melodic_minor, dorian, phrygian


# Function to get the note at a specific fret
def get_note_at_fret(start_note, fret, notes):
    start_index = notes.index(start_note)
    return notes[(start_index + fret) % len(notes)]

# Function to determine the color of a note
def get_note_color(note):
    return NOTE_COLOR.get(note, "white")  # Default color for any unexpected notes

# Function to generate the fretboard
def generate_fretboard(tuning, notes):
    fretboard = []
    for string in tuning:
        string_notes = [get_note_at_fret(string, fret, notes) for fret in range(FRETBOARD_LENGTH)]  # 22 frets + 1 open string
        fretboard.append(string_notes)
    
    return fretboard

# Function to display the fretboard in a grid
def display_fretboard(fretboard, canvas, notes):
    canvas.delete("all")
    
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    fret_width = width / FRETBOARD_LENGTH
    string_height = height / (len(fretboard) + 1)
    
    print(f"Canvas size: {width}x{height}")
    print(f"Fret width: {fret_width}, String height: {string_height}")
    
    # Add fret numbers
    for fret_idx in range(FRETBOARD_LENGTH):
        x = fret_idx * fret_width + fret_width / 2
        canvas.create_text(x, string_height / 2, text=str(fret_idx), font=("Arial", 10, "bold"), fill="black")
    
    # Add string numbers and notes
    for string_idx, string in enumerate(fretboard):
        y = (string_idx + 1) * string_height + string_height / 2
        canvas.create_text(fret_width / 2, y, text=f"{len(fretboard) - string_idx}", font=("Arial", 10, "bold"), fill="black")
        for fret_idx, note in enumerate(string):
            color = get_note_color(note)
            x = fret_idx * fret_width + fret_width / 2
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)
            canvas.create_text(x, y, text=note, font=("Arial", 8, "bold"), fill="black")

# Function to handle dropdown selection and button click
def on_generate():
    error_label.config(text="")  # Clear previous error messages
    selected_tuning = tuning_var.get()
    if selected_tuning == "Custom":
        custom_tuning = custom_tuning_entry.get().split(',')
        tuning = [note.strip() for note in custom_tuning if note.strip()]
        if len(tuning) != 6:
            error_label.config(text="Error: Custom tuning must have exactly 6 notes.")
            return
    else:
        tuning = TUNING_LIST[selected_tuning]
    
    # Normalize tuning notes based on selected notation
    if notation_var.get() == "Sharps":
        normalized_tuning = []
        for note in tuning:
            if note in NOTES_SHARP:
                normalized_tuning.append(note)
            elif note in NOTES_FLAT:
                normalized_tuning.append(NOTES_SHARP[NOTES_FLAT.index(note)])
            else:
                error_label.config(text=f"Error: Invalid note '{note}' in tuning.")
                return
        fretboard = generate_fretboard(normalized_tuning, NOTES_SHARP)
        display_fretboard(fretboard, fretboard_canvas, NOTES_SHARP)
    else:
        normalized_tuning = []
        for note in tuning:
            if note in NOTES_FLAT:
                normalized_tuning.append(note)
            elif note in NOTES_SHARP:
                normalized_tuning.append(NOTES_FLAT[NOTES_SHARP.index(note)])
            else:
                error_label.config(text=f"Error: Invalid note '{note}' in tuning.")
                return
        fretboard = generate_fretboard(normalized_tuning, NOTES_FLAT)
        display_fretboard(fretboard, fretboard_canvas, NOTES_FLAT)

# Create the main application window
root = tk.Tk()
root.title("Guitar Fretboard Generator")
root.geometry("1200x800")  # Set default window size

# Create and place the input field
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Dropdown menu for tuning selection
ttk.Label(main_frame, text="Select the guitar tuning:").grid(column=0, row=0, padx=10, pady=10)
tuning_var = tk.StringVar()
tuning_menu = ttk.OptionMenu(main_frame, tuning_var, "Standard", *TUNING_LIST.keys(), "Custom")
tuning_menu.grid(column=0, row=1, padx=10, pady=10)

# Input box for custom tuning
ttk.Label(main_frame, text="Or enter custom tuning (comma-separated: E,A,D,G,B,E):").grid(column=0, row=2, padx=10, pady=10)
custom_tuning_entry = ttk.Entry(main_frame, width=50)
custom_tuning_entry.grid(column=0, row=3, padx=10, pady=10)

# Dropdown menu for notation selection
ttk.Label(main_frame, text="Select notation:").grid(column=0, row=4, padx=10, pady=10)
notation_var = tk.StringVar()
notation_menu = ttk.OptionMenu(main_frame, notation_var, "Sharps", "Sharps", "Flats")
notation_menu.grid(column=0, row=5, padx=10, pady=10)

# Create and place the generate button
generate_button = ttk.Button(main_frame, text="Generate Fretboard", command=on_generate)
generate_button.grid(column=0, row=6, padx=10, pady=10)

# Create canvas for the fretboard
fretboard_canvas = tk.Canvas(main_frame, bg="white")
fretboard_canvas.grid(column=0, row=7, padx=7, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create label for error messages
error_label = ttk.Label(main_frame, text="", foreground="red")
error_label.grid(column=0, row=8, padx=10, pady=10)

# Configure resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(7, weight=1)

# Bind the resize event to redraw the fretboard
def on_resize(event):
    selected_tuning = tuning_var.get()
    if selected_tuning == "Custom":
        custom_tuning = custom_tuning_entry.get().split(',')
        tuning = [note.strip() for note in custom_tuning if note.strip()]
        if len(tuning) != 6:
            error_label.config(text="Error: Custom tuning must have exactly 6 notes.")
            return
    else:
        tuning = TUNING_LIST[selected_tuning]
    
    # Normalize tuning notes based on selected notation
    if notation_var.get() == "Sharps":
        normalized_tuning = []
        for note in tuning:
            if note in NOTES_SHARP:
                normalized_tuning.append(note)
            elif note in NOTES_FLAT:
                normalized_tuning.append(NOTES_SHARP[NOTES_FLAT.index(note)])
            else:
                error_label.config(text=f"Error: Invalid note '{note}' in tuning.")
                return
        fretboard = generate_fretboard(normalized_tuning, NOTES_SHARP)
        display_fretboard(fretboard, fretboard_canvas, NOTES_SHARP)
    else:
        normalized_tuning = []
        for note in tuning:
            if note in NOTES_FLAT:
                normalized_tuning.append(note)
            elif note in NOTES_SHARP:
                normalized_tuning.append(NOTES_FLAT[NOTES_SHARP.index(note)])
            else:
                error_label.config(text=f"Error: Invalid note '{note}' in tuning.")
                return
        fretboard = generate_fretboard(normalized_tuning, NOTES_FLAT)
        display_fretboard(fretboard, fretboard_canvas, NOTES_FLAT)

root.bind("<Configure>", on_resize)

# Start the main event loop
root.mainloop()