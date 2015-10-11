# CS:GO Server Blocker for Linux

# To make things clear:

1. THIS WILL NOT GET YOU VAC-BANNED! (only blocks server IPs)
2. This script MUST run with root access.
3. Changes made by this script are not permanent. (reboot to reset all changes)
4. This script uses 'iptables' and small tools to block servers.
5. This script will affect to Competetive and Casual servers. (possibly demolition etc..)

# Prepare & Run:

1. Make sure these following things are installed: bash, iptools, coreutils and dpkg-query.
2. Open a terminal, 'cd' to the directory where you have extracted the script 
and type 'chmod +x ./csgosb' to give run access.
3. Start the script by typing 'sudo ./csgosb' to the open terminal.

# How to use:

1. Answer to the questions by typing the answer and pressing enter.
2. Servers are numbered. Type server's number and press enter.
3. Type your answer and press enter.

# Faq:

Q: How to fix "Failed to connect the match."?
A: Restart CS:GO and set your max ping to 350ms.

Q: I'm in a lobby and stuck at "Confirming match..."
A: Make sure the lobby leader has blocked the same servers.

Q: Why does this script need root access?
A: iptables won't work without root access. This script won't edit other files.

Q: Why can't I see server's ping after unblocking it?
A: You've probably blocked it multiple times. Try to unblock it again.

Q: Am I allowed to modify and publish my version of this script?
A: Yes, but please tell me about it so I can fix my version of the script.

If you find bugs or missing servers from this script, please report them to me.

-santeri3700 aka LuomuBanaani
