#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "santeri3700"
__copyright__ = "Copyright 2020, santeri3700"
__license__ = "GPLv2"
__version__ = "0.0.1"

import platform
import iptc
import ipaddress
import requests
import re

#GUI and async stuff.
import asyncio
import ping3
import glibcoro
glibcoro.install()
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject

class CSGOSB():

    app_name = "CSGOSB"
    debug = True # Enable/Disable debug messages and tests.

    def __init__(self):
        self.log(self.app_name + " starting...")

    def log(self, text, severity = "INFO"):
        if(severity == "INFO"):
            print("[" + self.app_name + "][INFO ] " + text)
        elif(severity == "WARN"):
            print("[" + self.app_name + "][WARN ] " + text)
        elif(severity == "ERROR"):
            print("[" + self.app_name + "][ERROR] " + text)
        elif(severity == "FATAL"):
            print("[" + self.app_name + "][FATAL] " + text)
        elif(severity == "DEBUG" and self.debug):
            print("[" + self.app_name + "][DEBUG] " + text)
        elif(self.debug):
            print("[" + self.app_name + "][UNKNW] " + text)

class Firewall(CSGOSB):
    def __init__(self):
        self.log(self.app_name + " Initializing Firewall...", "DEBUG")
        
        # Linux is using iptables.
        if(platform.system() == "Linux"):

            try:
                self.iptc_table = iptc.Table(iptc.Table.FILTER) #IPv4
                self.iptc_chain = iptc.Chain(self.iptc_table, "OUTPUT")
            except iptc.IPTCError as e:
                self.log("Failed to initialize IPTC!", "FATAL")
                self.log(str(e), "DEBUG")
                exit(1)
            except Exception as e:
                self.log("Unknown error occurred while initializing Firewall with iptables!", "FATAL")
                self.log(str(e), "DEBUG")
                exit(1)

            def block_range(network_range):
                if(not is_valid_network(network_range)):
                    self.log("Aborting...", "DEBUG")
                    exit(1)
                self.log("Blocking range: " + network_range, "DEBUG")

                # TODO: Improve exception handling.
                try:
                    if not self.is_blocked(network_range):
                        self.iptc_chain.insert_rule(rule(network_range))
                    else:
                        self.log("Was already blocked.", "DEBUG")
                except iptc.IPTCError as e:
                    self.log("Failed to add an iptables rule!", "WARN")
                    self.log(str(e), "DEBUG")

            def unblock_range(network_range):
                if(not is_valid_network(network_range)):
                    self.log("Aborting...", "DEBUG")
                    exit(1)
                self.log("Unblocking range: " + network_range, "DEBUG")

                # TODO: Improve exception handling.
                # When trying to delete an unexistent rule: iptc.ip4tc.IPTCError: can't delete entry from chain CSGOSB: b'Bad rule (does a matching rule exist in that chain?)'
                try:
                    if self.is_blocked(network_range):
                        self.iptc_chain.delete_rule(rule(network_range))
                    else:
                        self.log("Was not blocked before?", "DEBUG")
                except iptc.IPTCError as e:
                    self.log("Failed to delete an iptables rule. Maybe it does not exist?", "WARN")
                    self.log(str(e), "DEBUG")

            def is_blocked(network_range):
                if(not is_valid_network(network_range)):
                    self.log("Aborting...", "DEBUG")
                    exit(1)
                iptc_rule = rule(network_range)

                # Return true/false if a matching rule exists.
                if iptc_rule in self.iptc_chain.rules:
                    self.log(network_range + " is blocked.", "DEBUG")
                    return True
                else:
                    self.log(network_range + " is not blocked.", "DEBUG")
                    return False

            def is_valid_network(network_range):
                try:
                    if(ipaddress.ip_network(network_range, strict=True)):
                        return True
                except ValueError as e:
                    self.log("Invalid network range!", "DEBUG")
                    self.log(str(e), "DEBUG")
                    return False

            def rule(network_range):
                iptc_rule = iptc.Rule()
                #TODO: Add option to choose the network interface. iptc_rule.in_interface = "eno1"
                iptc_rule.dst = network_range
                iptc_target = iptc.Target(iptc_rule, "DROP")
                iptc_rule.target = iptc_target

                return iptc_rule
            
        # Windows is using Windows Firewall.
        elif(platform.system() == "Windows"):
            # TODO: Implement support for Windows Firewall.
            self.log("Windows support is not implemented yet!", "FATAL")
            exit(1)
        # MacOS is using OpenBSD packet filter "pf" | https://man.openbsd.org/pfctl
        elif(platform.system() == "Darwin"):
            # TODO: Implement support for MacOS.
            self.log("MacOS support is not implemented yet!", "FATAL")
            exit(1)
        else:
            self.log("Unsupported/unknown platform: " + platform.system(), "FATAL")
            exit(1)

        self.block_range = block_range
        self.unblock_range = unblock_range
        self.is_blocked = is_blocked
        self.is_valid_network = is_valid_network

class NetworkConfig(CSGOSB):

    def __init__(self):
        self.log(self.app_name + " Initializing NetworkConfig...", "DEBUG")
    
        #network_config_json_url = "https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/platform/config/network_config.json"
        #network_config_json_url = "http://127.0.0.1/network_config.json"
        network_config_json_url = "https://steamcdn-a.akamaihd.net/apps/sdr/network_config.json"

        # Retrieve network configuration.
        # TODO: Improve exception handling.
        try:
            # TODO: Implement local caching for the network config json.
            network_config_json = requests.get(network_config_json_url, timeout=5)

            if(network_config_json.status_code == 200):
                network_config = network_config_json.json()
                self.log("Loaded network config revision " + str(network_config["revision"]), "INFO")
            else:
                self.log("Failed to load the network config!", "ERROR")
        except Exception as e:
            self.log("Unknown error occurred while initializing NetworkConfig with requests!", "FATAL")
            self.log(str(e), "DEBUG")
            exit(1)

        self.pops = network_config["pops"]

        for pop_name in self.pops:
            pop = self.pops[pop_name]

            if("desc" in pop):
                pop_desc = pop["desc"]
            else:
                # TODO: Get missing description from IATA information, pop_name = IATA sign. https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code
                pop_desc = "UNKNOWN"

            if self.debug:
                if("relays" in pop):
                    pop_relays = pop["relays"]
                else:
                    pop_relays = [] # To avoid errors later.

            # Convert dumb ranges to valid network ranges with subnet mask.
            if("service_address_ranges" in pop):
                pop_service_address_ranges = pop["service_address_ranges"]

                for key, pop_service_address_range in enumerate(pop_service_address_ranges):

                    if(not main.firewall.is_valid_network(pop_service_address_range)):
                        
                        # Search for dumb ranges like "123.123.123.0-123.123.123.254" and convert them to something like "123.123.123.0/24"
                        pop_service_address_range_dumb = re.search("^((?:[0-9]{1,3}\.){3}[0-9]{1,3})-((?:[0-9]{1,3}\.){3}[0-9]{1,3})$", pop_service_address_range)

                        if(pop_service_address_range_dumb != None):
                            # TODO: Add exception handling.
                            pop_service_address_range_start = ipaddress.IPv4Address(pop_service_address_range_dumb.group(1))
                            pop_service_address_range_end = ipaddress.IPv4Address(pop_service_address_range_dumb.group(2))

                            #FIXME: Could this for-loop be avoided?
                            for pop_service_address_range_good in ipaddress.summarize_address_range(pop_service_address_range_start, pop_service_address_range_end):
                                self.log("Converted a dumb range to: " + str(pop_service_address_range_good), "DEBUG")

                                # Replace the dumb range with the good range.
                                self.pops[pop_name]["service_address_ranges"][key] = str(pop_service_address_range_good)
                                break # We should only have one match so no need to iterate more than once. Could this for-loop be avoided?
            else:
                pop_service_address_ranges = [] # To avoid errors later.
            
            if self.debug:
                self.log("POP: " + pop_name + ", desc: \"" + pop_desc + "\", relays: " + str(len(pop_relays)) + ", service address ranges: " + str(len(pop_service_address_ranges)), "DEBUG")

class PopManager(CSGOSB):
    def __init__(self):
        self.log(self.app_name + " Initializing PopManager...", "DEBUG")
        self.pops = main.network_config.pops

        def block_all_pops():
            for pop in self.pops:
                block_pop(pop)

        def block_pop(pop_name, block_relays = True, block_service_addresses = True):
            self.log("Blocking pop \"" + pop_name + "\"")
            toggle_pop("block", pop_name, block_relays, block_service_addresses)

        def unblock_all_pops():
            for pop in self.pops:
                unblock_pop(pop)

        def unblock_pop(pop_name, unblock_relays = True, unblock_service_addresses = True):
            self.log("Unblocking pop \"" + pop_name + "\"")
            toggle_pop("unblock", pop_name, unblock_relays, unblock_service_addresses)

        def toggle_pop(mode, pop_name, toggle_relays, toggle_service_addresses):
            if "relays" in self.pops[pop_name]:
                relays = self.pops[pop_name]["relays"]
                if toggle_relays:
                    for relay in relays:
                        if mode == "block":
                            main.firewall.block_range(relay['ipv4'])
                        else:
                            main.firewall.unblock_range(relay['ipv4'])

            if "service_address_ranges" in self.pops[pop_name]:
                service_addresses = self.pops[pop_name]["service_address_ranges"]
                if toggle_service_addresses:
                    for service_address in service_addresses:
                        if mode == "block":
                            main.firewall.block_range(str(service_address))
                        else:
                            main.firewall.unblock_range(str(service_address))

        def is_blocked(pop_name):
            any_blocked = False

            if "relays" in self.pops[pop_name]:
                relays = self.pops[pop_name]["relays"]
                for relay in relays:
                    if(main.firewall.is_blocked(relay['ipv4'])):
                        any_blocked = True

            if "service_address_ranges" in self.pops[pop_name]:
                service_addresses = self.pops[pop_name]["service_address_ranges"]
                for service_address in service_addresses:
                    if(main.firewall.is_blocked(str(service_address))):
                        any_blocked = True

            return any_blocked

        self.block_all_pops = block_all_pops
        self.block_pop = block_pop
        self.unblock_all_pops = unblock_all_pops
        self.unblock_pop = unblock_pop
        self.is_blocked = is_blocked

class GUI(CSGOSB):

    def on_toggled(self, widget, row):
        widget.set_sensitive(True)
        self.liststore[row][0] = not self.liststore[row][0]

        if self.liststore[row][0]:
            self.log("Blocked " + self.liststore[row][2])
            main.pop_manager.block_pop(self.liststore[row][2])
        else:
            self.log("Unblocked " + self.liststore[row][2])
            main.pop_manager.unblock_pop(self.liststore[row][2])

    def load_rows(self):
        self.log("GUI loading rows...", "DEBUG")

        for index, pop_name in enumerate(main.pop_manager.pops):
            pop = main.pop_manager.pops[pop_name]

            if("desc" in pop):
                pop_desc = pop["desc"]
            else:
                # TODO: Get missing description from IATA information, pop_name = IATA sign. https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code
                pop_desc = "UNKNOWN"

            pop_blocked = main.pop_manager.is_blocked(pop_name)
            
            added_row = self.liststore.append([pop_blocked, pop_desc, pop_name, " - "])

            # TODO: FIXME: Currently we are unable to do an async ping. This might be because we are using glibcoro.
            #asyncio.ensure_future(self.ping_server(added_row, pop_name))
            #main.loop.run_until_complete(self.ping_server(added_row, pop_name))

    async def ping_server(self, row, pop_name):
        pops = main.pop_manager.pops

        #server_range = pops[pop_name]["service_address_ranges"][0]

        if "relays" in pops[pop_name]:
            relays = pops[pop_name]["relays"]
            for relay in relays:
                server_range = relay['ipv4']
                break

        if "service_address_ranges" in pops[pop_name]:
            service_addresses = pops[pop_name]["service_address_ranges"]
            for service_address in service_addresses:
                server_range = str(service_address)
                break

        #print("server_range: " + str(server_range))

        server_ip = re.search("([0-9]+(?:\.[0-9]+){3})", server_range)[0]

        server_ip = re.sub(r'\.0', '.1', server_ip)
        
        #print("server_ip: " + str(server_ip))

        host = server_ip #FIXME: this might not be pingable but .254 or .100 is.

        try:
            latency = ping3.ping(host)

            if latency != None:
                latency = latency * 1000
            else:
                latency = 0
            print("Ping response in %s ms" % latency)
            main.gui.liststore[row][3] = str(round(latency, 2)) + " ms" #FIXME:

        except Exception as e:
            print(str(e))
            print("Timed out")
            main.gui.liststore[row][3] = "Timed out!"

    def __init__(self):
        window = Gtk.Window(title=self.app_name + " version " + __version__)
        window.__init__(self)
        window.set_border_width(4)
        window.set_default_size(400, 200)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        renderer_text = Gtk.CellRendererText()
        renderer_toggle = Gtk.CellRendererToggle()

        renderer_toggle.connect("toggled", self.on_toggled)

        liststore = Gtk.ListStore(bool, str, str, str)

        treeview = Gtk.TreeView(model=liststore)

        column_toggle = Gtk.TreeViewColumn("Block", renderer_toggle, active=0)
        column_toggle.set_sort_column_id(0)
        treeview.append_column(column_toggle)

        column_name = Gtk.TreeViewColumn("Server", renderer_text, text=1)
        column_name.set_sort_column_id(1)
        treeview.append_column(column_name)

        column_popcode = Gtk.TreeViewColumn("POP code", renderer_text, text=2)
        column_popcode.set_sort_column_id(2) 
        treeview.append_column(column_popcode)

        column_ping = Gtk.TreeViewColumn("Ping", renderer_text, text=3)
        column_ping.set_sort_column_id(3) 
        treeview.append_column(column_ping)

        scrolled_window.add_with_viewport(treeview)
        window.add(scrolled_window)

        window.show_all()

        self.window = window
        self.liststore = liststore

##################
### Main logic ###
##################

def quit(self):
    print("Bye!")
    main.loop.stop()
    Gtk.main_quit() # FIXME: Should we use "g_application_quit()" here instead?

if __name__ == '__main__':
    main = CSGOSB()
    main.loop = asyncio.get_event_loop()
    
    main.firewall = Firewall()
    main.network_config = NetworkConfig()
    main.pop_manager = PopManager()

    # TEST, this will toggle pops "atl" and "sto" status opposite of each other on each run.
    if(main.pop_manager.is_blocked("sto")):
        main.pop_manager.unblock_all_pops()
        main.pop_manager.block_pop("atl")
    else:
        main.pop_manager.unblock_all_pops()
        main.pop_manager.block_pop("sto")

    main.gui = GUI()
    main.gui.window.connect("delete-event", lambda *args: quit(main))
    main.gui.load_rows()

    main.log("Ready!", "INFO")
    main.loop.run_forever()