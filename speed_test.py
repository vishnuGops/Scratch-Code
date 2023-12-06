# using speedtest-cli to get the network speed using python.
import speedtest
import Tkinter as tk
# Function to update the download and upload speed labels
def update_speeds():
    st = speedtest.Speedtest()
    download_speed = round(st.download() / 1048576, 2)
    upload_speed = round(st.upload() / 1048576, 2)

    download_label.config(text ="Download speed: " + str(download_speed) + " MB/s")
    upload_label.config(text = "Upload speed: " + str(upload_speed) + " MB/s")

    # uncomment to check the speed in intervals
    # window.after(30000, update_speeds)

# Create the main window
window = tk.Tk()
window.title("Network Speed Monitor")

# Create labels for download and upload speed
download_label = tk.Label(window, text="Download Speed:")
download_label.pack(pady=10)

upload_label = tk.Label(window, text="Upload Speed:")
upload_label.pack(pady=10)

# Create button to update speeds
update_button = tk.Button(window, text="Update Speeds", command=update_speeds)
update_button.pack(pady=10)

# Update the speed labels once
update_speeds()

# Start the main loop
window.mainloop()    
