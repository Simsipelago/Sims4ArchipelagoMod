# Sims 4 Archipelago Project
This is the Sims 4 mod part of the Sims 4 Archipelago.gg integration. The goal of the mod is to enable the 
player to play their game together with other people as part of a multiworld and multigame experience. 

Check https://archipelago.gg for more information on Archipelago Multiworld. 

This mod is built upon the Sims4CommunityLibrary, a mod that offers easy to use APIs for mod programming. Check 
their github page for further information:
https://github.com/ColonolNutty/Sims4CommunityLibrary

## Installing the mod

1. Check the "releases" page for the newest release. 
2. Download the release package and unpack the files to your Sims 4 Installation directory into
the /Mods folder.

   The Package should contain a .ts4script and a .package file   

   The default directory should be something like _C:\Users\<Username>\Documents\Electronic Arts\The Sims 4_
3. Go to the [Sims4CommunityLibrary github](https://github.com/ColonolNutty/Sims4CommunityLibrary) and follow 
installation directions there

## Requirements
Due to relying on Sims4CommunityLibrary, it shares the same requirements as that mod. Check the game requirements
on the [Sims4CommunityLibrary github](https://github.com/ColonolNutty/Sims4CommunityLibrary)

## Manually building or adding to the mod
If you want to build the mod yourself, there's a few extra steps involved.
1. The mod was built upon the [Sims4CommunityLibrary Template project](https://github.com/ColonolNutty/s4cl-template-project)
Check installation instructions there to set up your workspace 
2. After you prepared the template project, your project should run on Python 3.7 and include the EA scripts as well as 
the Sims4CommunityLibrary files.
3. Additionally, this mod uses [websocket](https://github.com/websocket-client/websocket-client) and [rel](https://github.com/bubbleboy14/registeredeventlistener) to connect to the Archipelago Servers. To set this up in
your workspace follow these steps:
   * Download the websocket client source code and rel source code or install them and copy them from your Python 3.7 
     installation into the main folder
   * open the compile.py script from the Template project and change the following code:
     **names_of_modules_include=('s4ap', 'websocket', 'rel'),**
   * a few of the included files are for testing purposes only and will cause problems when being bundled with the mod so 
     we delete them: 
     * websocket/tests
     * websocket/_wsdump.py
     * rel/tests.py
     * rel/tools.py
   * The runtime inside The Sims 4 doesn't support IPv6, so you have to explicitly
     set the protocol to IPv4 in the websocket client code. To do so, follow these steps:
     * open the file *websocket/_http.py*
     * look for the function *_get_addrinfo_list*
     * Change the third parameter (should be a 0) to *socket.AF_INET* 
4. To build the mod, run the compile.py script from the template project. This should create a *Sims4Archipelago.ts4script*
   in the *Release/s4ap* folder. Copy this to your mods folder
5. To make changes to the .package, you need to install Sims4Studio. This should only matter if you want to add new
   localization options.

## Copyright

This mod is licensed under MIT license (check LICENSE for details)

### S4CL Attribution
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode

S4CL Copyright (c) COLONOLNUTTY
