# CS:GO Server Blocker for Linux

# To make things clear:

1. *THIS WILL NOT GET YOU VAC-BANNED!* (only blocks server IPs)
2. This script *MUST* run with root access.
3. Changes made by this script are not permanent. (reboot to reset all changes)
4. This script uses 'iptables' and small tools to block servers.
5. This script will affect to Competetive and Casual servers. (possibly demolition etc..)

# Prepare & Run:

1. Make sure these following things are installed: bash, iptools and coreutils.
2. Open a terminal, 'cd' to the directory where you have extracted the script 
and type 'chmod +x ./csgosb' to give it run access.
3. Start the script by typing 'sudo ./csgosb' to the open terminal.

# How to use:

The script works as any other basic command do in Linux.
Read _manual.txt_ for more info!

# Faq:

Q: How to fix "Failed to connect the match."?<br>
A: Restart CS:GO and set your max ping to 350ms.

Q: I'm in a lobby and stuck at "Confirming match..."<br>
A: Make sure the lobby leader has blocked the same servers.

Q: Why does this script need root access?<br>
A: iptables won't work without root access. This script won't edit other files.

Q: Why can't I see server's ping after unblocking it?<br>
A: The server may be offline or your ISP has blocked it.

Q: Am I allowed to modify and publish my version of this script?<br>
A: Yes, but please tell me about it so I can fix my version of the script.

Give me suggestions and if you find bugs or missing servers from this script, please report them to me.

-santeri3700 aka LuomuBanaani
