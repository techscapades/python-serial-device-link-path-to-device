'''
ALL CODE 
This programme scans USB ports for serial
devices and tags these serial devices to 
their associated device paths based on
pre-configured JSON properties recieved
from the serial device. 

This example code scans for devices with 
a user definable list of device_ids of 
nodeMCUs. It also scans serial devices 
and gets their paths, then it sends a 
JSON message to the serial device 
and then based on its output appends 
a dictionary with the name of the device
that's recieved and its path

@techscapades 2023 https://github.com/techscapades
'''

import usb.core
import usb.util
import json
import serial
import serial.tools.list_ports
import time

baud_rate = 115200  # default baud rate
device_id_list = ["1a86:7523"]  # list of device_ids to scan for
device_dictionary = {}


def get_usb_device_metadata(device):
    # Function to get USB device metadata
    metadata = {
        "device_id": f"{device.idVendor:04x}:{device.idProduct:04x}"
    }
    return metadata


def detect_usb_devices(device_id_list):
    # Function to detect and list USB devices with device_id in device_id_list
    devices = usb.core.find(find_all=True)
    usb_device_list = []

    for device in devices:
        device_metadata = get_usb_device_metadata(device)
        if device_metadata["device_id"] in device_id_list:
            usb_device_list.append(device_metadata)

    return usb_device_list


def list_serial_ports():
    # function to detect all serial ports
    ports_list = []
    ports = serial.tools.list_ports.comports()
    serial_ports = [port.device for port in ports]
    for available_port in serial_ports:
        ports_list.append(available_port)
    return serial_ports


def generate_serial_objects(get_device_ports):
    device_serial_list = []
    for i in range(len(get_device_ports)):
        device_serial_list.append(
            serial.Serial(get_device_ports[i], baud_rate))
    return device_serial_list


# Main function
if __name__ == "__main__":

    device_ports = list_serial_ports()  # get a list of all serial ports
    # get a list of all relevant usb devices
    usb_devices = detect_usb_devices(device_id_list)
    serial_objects = generate_serial_objects(
        device_ports)  # get a list of all serial objects

    print(device_ports)
    print(usb_devices)
    print(serial_objects)

    i = 0  # iterator for device_ports list
    for serial_object in serial_objects:
        while True:  # keep sending the message on the same serial port until response is received
            data = json.dumps({"message": "on"})  # send some JSON data
            serial_object.write(data.encode('utf-8'))
            time.sleep(0.01)  # short interval to pause serial activity
            received_data = serial_object.readline().decode('utf-8')  # recieve data
            try:
                json_data = json.loads(received_data)
                print("Received JSON data:")
                print(json_data)
                if json_data['message'] == 'hello':
                    print(json_data['device'])
                    device_dictionary[json_data['device']] = {'path': device_ports[i],
                                                              'serial_info': serial_object}
                    i = i + 1
                    break  # message is successflly recieved
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")  # might happen

    # include this for double checking device types
    device_dictionary['usb_devices'] = usb_devices

    print(device_dictionary)
