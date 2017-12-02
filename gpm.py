import requests
import sys
import argparse
from os import remove, mkdir, rename, listdir, getcwd
from shutil import rmtree

cwd = getcwd()
documentsIndex = cwd.index("Documents")
documentsIndex += len("Documents")
ROOT = cwd[:documentsIndex]

class stansi:
	bold = u"\033[1m"
	underscore = u"\x9b4m"
	attr_end = u"\x9b0m"
	
	fore_red = u"\x9b31m"
	fore_green = u"\x9b32m"
	fore_brown = u"\x9b33m"
	fore_blue = u"\x9b34m"
	fore_pink = u"\x9b35m"
	fore_cyan = u"\x9b36m"
	fore_white = u"\x9b37m"
	fore_end = u"\x9b39m"
	
	back_red = u"\x9b41m"
	back_green = u"\x9b42m"
	back_brown = u"\x9b43m"
	back_blue = u"\x9b44m"
	back_pink = u"\x9b45m"
	back_cyan = u"\x9b46m"
	back_white = u"\x9b47m"
	back_end = u"\x9b49m"
	
def Red(text):
	return stansi.fore_red + text + stansi.fore_end
	
def Blue(text):
	return stansi.fore_blue + text + stansi.fore_end
	
def Green(text):
	return stansi.fore_green + text + stansi.fore_end
	
def Cyan(text):
	return stansi.fore_cyan + text + stansi.fore_end
	
def Success(text):
	return stansi.fore_green + stansi.bold + text + stansi.attr_end
	
def Error(text):
	return stansi.fore_red + stansi.bold + text + stansi.attr_end
	
class GPMConfig (object):
	def __init__(self, content):
		self.data = {}
		for line in content.splitlines():
			key = line.split(": ")[0]
			value = line.split(": ")[1]
			self.data[key] = value
			
	def __getitem__(self, key):
		return self.data[key]
		
	def keys(self):
		return self.data.keys()
		
def remove_line(content, lines_list):
	pointer = 0
	for line in lines_list:
		if content in line:
			lines_list.pop(pointer)
		pointer += 1
	return lines_list
	
def download_package(url, package_name):
	content_listing = ["app.py", "package.gpm"]
	mkdir(ROOT + "/" + package_name)
	for item in content_listing:
		requested = requests.get(url + "/" + package_name + "/" + item)
		content = requested.text
		requested.close()
		if content == "404: Not Found\n":
			print(Error("ERROR") + ": Package not found.")
			sys.exit()
		opened = open(ROOT + "/" + package_name + "/" + item, "w")
		opened.write(content)
		opened.close()

def main(sargs):
	parser = argparse.ArgumentParser()
	parser.add_argument("method", help="What action to perform (install, remove, etc)", type=str)
	parser.add_argument("package", help="Name of package", type=str)
	args = parser.parse_args(sargs)
	try:
		opened = open(".gpm-repos.gpmconfig", "r")
		opened.close()
	except:
		opened = open(".gpm-repos.gpmconfig", "w")
		print(Error("WARNING") + ": Repository cache doesn't exist, setting up with default...'")
		opened.write("ghost-universe: https://raw.githubusercontent.com/GhostHackz861/gpm-universe/master")
		opened.close()
	
	repo_listing_opened = open(".gpm-repos.gpmconfig", "r")
	listing_content = repo_listing_opened.read()
	repo_listing_opened.close()
	REPOSITORIES = GPMConfig(listing_content)
	
	if args.method == "install":
		packageSplitted = args.package.split("/")
		try:
			package_name = packageSplitted[1]
			repo_to_use = REPOSITORIES[packageSplitted[0]]
		except IndexError:
			repo_to_use = REPOSITORIES["gpm-universe"]
			package_name = packageSplitted[0]
		print(Error("WARNING") + ": No repository specified, using default repository...")
		try:
			download_package(repo_to_use, package_name)
		except:
			print(Error("ERROR") + ": Failed to find package.")
			sys.exit()
		print("Installing...")
		try:
			rename(ROOT + "/" + package_name + "/package.gpm", ROOT + "/stash_extensions/gpm/" + package_name + ".gpm")
		except:
			mkdir(ROOT + "/stash_extensions/gpm")
			rename(ROOT + "/" + package_name + "/package.gpm", ROOT + "/stash_extensions/gpm/" + package_name + ".gpm")
		rename(ROOT + "/" + package_name + "/app.py", ROOT + "/stash_extensions/bin/" + package_name + ".py")
		rmtree(ROOT + "/" + package_name)
		print(Success("SUCCESS") + ": Package '" + package_name + "' successfully installed!")
	elif args.method == "remove":
		try:
			remove(ROOT + "/stash_extensions/bin/" + args.package + ".py")
			remove(ROOT + "/stash_extensions/gpm/" + args.package + ".gpm")
		except:
			print(Error("ERROR") + ": Could not remove package.")
			sys.exit()
		print(Success("SUCCESS") + ": '" + args.package + "' removed!")
	elif args.method == "new":
		try:
			mkdir(args.package)
			config = open(args.package + "/package.gpm", "w")
			config.write("developer: Your name here\ndescription: Enter description of your app here\nversion: 0.1")
			config.close()
			index = open(args.package + "/app.py", "w")
			index.write("# This is just an example template. You can change this all you like.\n\nimport sys\nimport argparse\n\ndef main(sargs):\n\tparser = argparse.ArgumentParser()\n\tparser.add_argument('echo', help='What you want the command to echo back.')\n\targs = parser.parse_args(sargs)\n\t\n\tprint('Echoing back: '+args.echo)\n\nif __name__ == '__main__':\n\tmain(sys.argv[1:])")
			index.close()
			print(Success("SUCCESS") + ": Package '" + args.package + "' generated.")
		except:
			print(Error("ERROR") + ": Couldn't generate package. Package may already exist.")
	elif args.method == "add-repo":
		try:
			request = requests.get(args.package + "/repo.gpm")
			data = request.text
			request.close()
			data_org = GPMConfig(data)
			nickname = data_org["name"]
			repo_listing = open(".gpm-repos.gpmconfig", "a")
			repo_listing.write("\n" + nickname + ": " + args.package)
			repo_listing.close()
			print(Success("SUCCEESS") + ": '" + nickname + "' added to repositories cache.")
		except:
			print(Error("ERROR") + ": Repo doesn't follow the GPM Repo's format.")
	elif args.method == "list-repos":
		if args.package == "all":
			opened = open(".gpm-repos.gpmconfig")
			content = opened.read()
			opened.close()
			as_config = GPMConfig(content)
			for repo in as_config.keys():
				print(Cyan(repo) + ": " + Green(as_config[repo]))
	elif args.method == "remove-repo":
		opened = open(".gpm-repos.gpmconfig", "r")
		data = opened.read().splitlines()
		opened.close()
		
		removed = remove_line(args.package, data)
		opened = open(".gpm-repos.gpmconfig", "w")
		opened.write(removed)
		opened.close()
		
		print(Success("SUCCESS") + ": Removed '" + args.package + "' from repository cache!")
	else:
		print(Error("ERROR") + ": Unknown command '" + args.method + "'!")

if __name__ == "__main__":
	main(sys.argv[1:])
