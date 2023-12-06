# using speedtest-cli to get the network speed using python.
import speedtest

st = speedtest.Speedtest()
download_speed = (st.download() /1048576) 
upload_speed = (st.upload() /1048576)

print("Download speed: " + str(download_speed) + " MB/s")
print("Upload speed: " + str(upload_speed) + " MB/s")
