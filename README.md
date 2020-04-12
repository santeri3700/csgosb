# CS:GO Server Blocker for Linux
##### (and possibly soon for Windows and MacOS also)
---
# To make things clear

1. **THIS WILL NOT GET YOU VAC- OR GAMEBANNED!**
2. This script **MUST** run be run with root access. Iptables won't work otherwise.
3. Changes made by this script are not permanent*. (*Linux: reboot to reset all of the changes)
4. This script basically uses 'iptables' (on Linux) to block servers.
5. This script will affect all Official Valve servers (including SDR relays).

# Prepare & Run

1. Make sure you have a backup of your iptables rules. I am not responsible if this script destroys your precious custom rules.
2. Make sure you have all of the required dependencies:
* Python 3.5+
* iptables enabled
* [python-iptables / iptc](https://github.com/ldx/python-iptables)
* [Requests](https://requests.readthedocs.io/en/master/)
* [Ping3](https://github.com/kyan001/ping3)
* [glibcoro](https://github.com/ldo/glibcoro) (a copy is included in this repository, might be replaced with [asyncio-glib](https://github.com/jhenstridge/asyncio-glib) in the future)
* [PyGObject](https://pygobject.readthedocs.io/en/latest/index.html)

3. Open a terminal, 'cd' in to the directory where you have extracted the script 
and then run 'chmod +x ./csgosb.py' to give it run access.
4. Start the script by running 'sudo ./csgosb.py'.
5. Choose regions which you want to block and then start CS:GO.

# How to use

**TODO**: Write documentation about the usage.

# FAQ

Q: Why am I getting connected to a region I have blocked?
A: Sometimes CS:GO routes your connection via a *Steam Datagram Relay* to another server in another region. As of now, there is no way around it that I know of.

Q: How to fix "Failed to connect the match."?
A: Restart CS:GO and set your max ping to 350ms (`mm_dedicated_search_maxping 350`)

Q: I'm in a lobby and stuck at "*Confirming match...*"
A: Make sure the lobby leader has blocked the same servers as you.

Q: Am I allowed to modify and publish my own version of this script?
A: Yes, see [LICENSE.md](https://github.com/santeri3700/csgosb/blob/master/LICENSE.md).

# Plans and work in progress before version 1.0.0
- [ ] Implement a CLI / command line arguments
- [ ] Implement a proper GUI (GTK+ 3)
- [ ] Implement asynchronous pinging (for GUI) / Replace glibcoro with asyncio-glib
- [ ] Implement a way to get missing POP descriptions from IATA information
- [ ] Improve exception handling
- [ ] Implement network config caching
- [ ] Implement Windows compatibility (Windows Firewall)
- [ ] Implement MacOS compatibility (Packer Filter / pf)
- [ ] (Make GUI dependencies optional?)
- [ ] (Separate classes to their own files?)
- [ ] (Package for Ubuntu, Windows and MacOS?)

**Suggestions and bug reports are welcome via GitHub issues.**
