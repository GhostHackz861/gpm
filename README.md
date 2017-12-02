# Ghost Package Manager (GPM)

`apt-get` for Pythonista's StaSh.

## What's GPM?

GPM is a CLI utility for [StaSh - Shell For Pythonista](https://github.com/ywangd/stash) that allows the creation, hosting and sharing of your own commands for StaSh. Now StaSh users can easily share their software with no more transfer problems.

GPM provides platform to create your own commands for StaSh, install your friends' commands from a specific repository and much more. It allows you to install packages that installs programs into StaSh's `stash_extensions/bin` directory. Now you can create your own commands!

## Installing

NOTE: Ghost Package Manager (GPM) is built to run on StaSh. Make sure you have already installed StaSh.

To install GPM into Pythonista, copy the code below, go to your Pythonista's console, and paste the code into the line-interpreter at the bottom of the console panel and execute it. This will run the GPM installer script. Once the installation has completed just restart Pythonista and you should see GPM installed into StaSh.

```python
import requests as r; exec(r.get("http://bit.ly/2AkrHNJ").text);
```

## Getting Started

### Creating Your Own Package:

```sh
gpm new ProjectName
```

This command will create a new project on the current working directory. You can edit the `app.py` and `package.gpm` files.

### Installing A Package:

```sh
gpm install PackageName
```

NOTE: This command will install the packages from the default GPM repository (GPM Universe).

### Running A Program:

```sh
PackageName (-h) ARGUMENT1 ARGUMENT2 ....
```

### Adding A 3rd Party Repo:

```sh
gpm add-repo URL
```

Note: If you are hosting the repository in GitHub, the URL must be in raw format and you must include the branch. (e.g. https://raw.githubusercontent.com/RepoOwner/RepoName/master)

If you want to know the GPM repo format, take a look at [GPM Universe](https://github.com/GhostHackz861/gpm-universe), the default repository of GPM.

### Installing A 3rd Party Program:

```sh
gpm install RepoName/PackageName
```

## Credits

We are the affiliated with any of the software/program listed below.

[Pythonista](http://omz-software.com/pythonista/) - Ole Zorn

[StaSh](https://github.com/ywangd/stash) - ywangd
