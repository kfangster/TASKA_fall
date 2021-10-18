# Steps to getting Glide to work on the TASKA and active wrist
- Before starting anything make sure to know the rules of ensuring the battery/power source is TURNED OFF when removing the TASKA hand or active wrist
- The correct configuration for the active wrist and TASKA is the following:
   - Active wrist to controller
   - Brown wire is Channel B (Analog B)
   - Orange wire is Channel A (Analog A)
   - Purple wire is the i^2 C communicator, goes into the gray port sticking out 
   - Power port goes into the hand (dimple facing in)
   - The gray port goes to where it's labeled wrist
- Through lots of meetings with Tina all the links below to a dropbox will need to be downloaded:
   - https://www.dropbox.com/sh/n5j0ngx7krhnuon/AAAVDb4MGAERa4F4J0Qj2CP3a?dl=0 (download everything but the 4c9c9b4 -wired programming) When downloading the dist folder make sure to drag/replace everything that's downloaded in the Glide setup
   - If there are issues such as generating Error 255 from the controller, you can try flashing the controller but going to the top left of the program and pressing update firmware to Flash it with the 4c9c9b4.bin file in the dropbox link listed above
   - Make sure when flashing that you are connected to the correct bluetooth/COM port (IF IT DOES NOT SAY Flash successful/restart program, it is NOT flashing it)
- Some more details are as follows:
   - In the glide software everything about the wheel can be changed (drag the inner radius to make it so that the grip actuates faster or drag the outer radius to make it so that it reaches max grip speed
	 - As for OPEN and CLOSE grips on the library those aren't actually an open and close grip. Instead each "grasp" has a certain open and close. For example tripod, key grip and general grasp each have their own open/close grip. General grasp is the one that has the generic open and close.
	 - Install glide the normal way, and ensure that the correct JRE is installed and drag and drop the glide software that allows one to change the device software in the control type (ALLOWS TO TEST FOR SENSE then come to the laptop and use the glide)
	 - The glide and sense catalyst software are different (don't use streaming that's not for us to use, it's for consumer use) This is why you could not see Glide on the Catalyst Software, they are separate. 


