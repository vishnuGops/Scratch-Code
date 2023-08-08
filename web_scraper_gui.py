import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup


def scrape_url():
    url = url_entry.get()
    word = word_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        clean_text = '\n'.join(line.strip()
                               for line in text_content.splitlines() if line.strip())

        result_text.delete(1.0, tk.END)  # Clear previous content
        result_text.insert(tk.END, clean_text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create main window
root = tk.Tk()
root.title("URL Text Scraper")

# Create URL input field
url_label = ttk.Label(root, text="Enter URL:")
url_label.pack(pady=10)
url_entry = ttk.Entry(root, width=100)
url_entry.pack(padx=20, pady=5)

word_label = ttk.Label(root, text="Enter word to count:")
word_label.pack(pady=10)
word_entry = ttk.Entry(root, width=50)
word_entry.pack(padx=20, pady=5)

# Create "Scrape" button
scrape_button = ttk.Button(root, text="Scrape", command=scrape_url)
scrape_button.pack(pady=10)

# Create result text area
result_text = tk.Text(root, wrap=tk.WORD, height=50, width=100)
result_text.pack(padx=20, pady=10)

root.mainloop()
