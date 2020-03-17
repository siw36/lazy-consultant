from pyvirtualdisplay import Display
import hvv
import helper

print("Starting a virtual display")
display = Display(visible=0, size=(1920, 1080))
display.start()

print("Start collecting bills")
hvv.fetch_bill(helper.start_browser())

if parse_config('WEBDAV', 'WEBDAV_UPLOAD_URL') == "true":
    print("Uploading tickets to webdav")
    helper.upload_webdav()

display.stop()
