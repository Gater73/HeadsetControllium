import customtkinter, subprocess, schedule
from PIL import Image

## Theme Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

## Interface Setup
root = customtkinter.CTk()
root.geometry("600x800")

## Functions
#Run pending scheduled tasks and schedule the update again after a short delay.
def schedule_update():

    # Run pending scheduled tasks
    schedule.run_pending()

    # Schedule the update again after a short delay
    root.after(1000, schedule_update)


# A function to print test, configure the battery text and image, and print "Test".
def updateState():
    global battery
    print(getBatteryLevel())
    battery.configure(text=(" "*8 + str(getBatteryLevel())), image=batteryDisplay())
    print("Battery Updated")
    print(getHeadsetModel())

def lightOn():
    # Define the first command
    command1 = ["headsetcontrol", "-l", "1"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Headset Lights turned on")

def lightOff():
    # Define the first command
    command1 = ["headsetcontrol", "-l", "0"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Headset Lights turned off")

def rot2muteOn():
    # Define the first command
    command1 = ["headsetcontrol", "-r", "1"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Rotate to Mute turned on")

def rot2muteOff():
    # Define the first command
    command1 = ["headsetcontrol", "-r", "0"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Rotate to Mute turned off")

def voiceOn():
    # Define the first command
    command1 = ["headsetcontrol", "-v", "1"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Voices turned on")

def voiceOff():
    # Define the first command
    command1 = ["headsetcontrol", "-v", "0"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    print("Voices turned off")


def getHeadsetModel():
    # Define the first command
    command1 = ["headsetcontrol", "-?"]
    
    # Run the first command and capture its output
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
    output_from_first_command = result1.stdout.strip()
    
    # Define the second command with separate arguments
    command2 = ["grep", "-oP", "Found \K.*?(?=!)"]
    
    # Run the second command, passing the output of the first command as input
    result2 = subprocess.run(command2, input=output_from_first_command, stdout=subprocess.PIPE, text=True)
    output_from_second_command = result2.stdout.strip()
    
    # Define the third command with separate arguments
    command3 = ["sed", 's/ *$//']
    
    # Run the third command, passing the output of the second command as input
    final_result = subprocess.run(command3, input=output_from_second_command, stdout=subprocess.PIPE, text=True)

    # Access the final output
    final_output = final_result.stdout.strip()
    
    return final_output


def getBatteryLevel():
    final_output = "Plugged in"
    try:
        # Define the first command
        command1 = ["headsetcontrol", "-b"]
        
        # Run the first command and capture its output
        result1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
        output_from_first_command = result1.stdout.strip()
        
        # Define the second command with separate arguments
        command2 = ["grep", "-o", "[0-9]\\+%"]
        
        # Run the second command, passing the output of the first command as input
        result2 = subprocess.run(command2, input=output_from_first_command, stdout=subprocess.PIPE, text=True)
        output_from_second_command = result2.stdout.strip()
        
        # Define the third command with separate arguments
        command3 = ["awk", '$1 <= 20 {print $1 "Low"} $1 > 20 {print $1}']
        
        # Run the third command, passing the output of the second command as input
        result3 = subprocess.run(command3, input=output_from_second_command, stdout=subprocess.PIPE, text=True)
        output_from_third_command = result3.stdout.strip()
        
        # Define the fourth command with separate arguments
        command4 = ["tail", "-c", "5"]
        
        # Run the fourth command, passing the output of the third command as input
        final_result = subprocess.run(command4, input=output_from_third_command, stdout=subprocess.PIPE, text=True)
        
        # Access the final output
        final_output = final_result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return final_output
    

# Determines the battery level and returns the corresponding data based on the level.
def batteryDisplay():
    try:
        if int(getBatteryLevel().replace("%","")) <= 49:
            return batteryLowData
        elif int(getBatteryLevel().replace("%","")) <= 79 and int(getBatteryLevel().replace("%","")) >= 50:
            return batteryMedData
        else:
            return batteryHighData
    except:
        return batteryChargingData


## Widgets
# Main Frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Headset Label
headsetLabel = customtkinter.CTkLabel(master=frame, text=getHeadsetModel())
headsetLabel.pack(pady=12, padx=10)

# Display image of headset
headsetImageData = customtkinter.CTkImage(light_image=Image.open("assets/headsets/c-void-e-s.png"),
                                  dark_image=Image.open("assets/headsets/c-void-e-s.png"),
                                  size=(120, 120))
headsetImage = customtkinter.CTkLabel(master=frame, text="",image=headsetImageData)
headsetImage.pack(pady=12, padx=10)

# Displays low battery porcentage
batteryLowData = customtkinter.CTkImage(light_image=Image.open("assets/icons/battery-low.png"),
                                  dark_image=Image.open("assets/icons/battery-low.png"),  
                                  size=(50, 20))
#Displays med battery porcentage
batteryMedData = customtkinter.CTkImage(light_image=Image.open("assets/icons/battery-med.png"),
                                  dark_image=Image.open("assets/icons/battery-med.png"),  
                                  size=(50, 20))
#Displays high battery porcentage
batteryHighData = customtkinter.CTkImage(light_image=Image.open("assets/icons/battery-high.png"),
                                  dark_image=Image.open("assets/icons/battery-high.png"),  
                                  size=(50, 20))
#Displays charging battery porcentage
batteryChargingData = customtkinter.CTkImage(light_image=Image.open("assets/icons/battery-charging.png"),
                                  dark_image=Image.open("assets/icons/battery-charging.png"),  
                                  size=(50, 20))

# Displays battery
global battery
battery = customtkinter.CTkLabel(master=frame, 
                                fg_color=["#2CC985", "#2FA572"],
                                corner_radius=8,
                                font=("Roboto", 16),
                                text=" " * 8 + str(getBatteryLevel()),
                                image=batteryDisplay())
battery.pack(pady=12, padx=10)

#runs PrintTest every 30 seconds
schedule.every(2).seconds.do(updateState)

# Button
button = customtkinter.CTkButton(master=frame, text="Print Test", command=updateState)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Light On", command=lightOn)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Light Off", command=lightOff)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Rotate to Mute On", command=rot2muteOn)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Rotate to Mute Off", command=rot2muteOff)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Voices On", command=voiceOn)
button.pack(pady=12, padx=10)
# Button
button = customtkinter.CTkButton(master=frame, text="Voices Off", command=voiceOff)
button.pack(pady=12, padx=10)

# Checks if headset is connected
if str(getHeadsetModel()) != "Corsair Headset Device":
    print("Headset Not Connected")
    print("Exiting...")
    exit(1)

# Start the schedule
schedule_update()

# Start the GUI
root.mainloop()