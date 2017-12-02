import requests
import console

def install_gpm():
	console.set_color(1.0, .0, .0)
	print("Downloading GPM...")
	request = requests.get("https://raw.githubusercontent.com/GhostHackz861/gpm/master/gpm.py")
	data = request.text
	print("Installing GPM...")
	opened = open("stash_extensions/bin/gpm.py", "w")
	opened.write(data)
	opened.close()
	print("Initializing GPM...")
	request.close()
	console.set_color(.0, 1.0, .0)
	print("[SUCCESS]: Ghost Package Manager (GPM) installed!")
	console.set_color()
	print("Restart Pythonista and try running 'gpm -h' in StaSh for help.")

console.set_color(.97, 1.0, .28)

print("[NOTE]: This script will install Ghost Package Manager (GPM) on your device.")

if __name__ == "__main__":
	install_gpm()
