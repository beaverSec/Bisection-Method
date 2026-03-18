import socket
import ssl
import hashlib
import time
import re

# ==============================
# CONFIG
# ==============================

IRC_SERVER = "irc.hackthissite.org"
IRC_PORT = 6697
USE_SSL = True

IRC_NICK = "CacaBot_HTS"
IRC_NICKSERV_PASS = "CharlotteD1041241067"

BOT_VERSION = "HTS-Bot Python"

# ==============================
# IRC BOT
# ==============================

class IRCBot:

    def __init__(self):
        self.sock = None
        self.buffer = ""
        self.attack_mode = False


    def connect(self):

        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.settimeout(300)

        if USE_SSL:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self.sock = ctx.wrap_socket(raw_sock, server_hostname=IRC_SERVER)
        else:
            self.sock = raw_sock

        print("[*] Connecting to IRC...")
        self.sock.connect((IRC_SERVER, IRC_PORT))
        print("[*] Connected")


    def send(self, msg):
        self.sock.sendall((msg + "\r\n").encode())
        print(">>>", msg)


    def recv(self):

        data = self.sock.recv(4096)

        if not data:
            raise ConnectionError("Disconnected")

        self.buffer += data.decode(errors="ignore")

        while "\r\n" in self.buffer:
            line, self.buffer = self.buffer.split("\r\n", 1)
            yield line


    def run(self):

        self.connect()

        self.send(f"NICK {IRC_NICK}")
        self.send(f"USER {IRC_NICK} 0 * :HTS Bot")

        while True:

            for line in self.recv():

                print("<<<", line)

                # PING
                if line.startswith("PING"):
                    self.send("PONG :" + line.split(":")[1])


                # END OF MOTD
                if " 376 " in line:

                    print("[*] Identifying...")

                    self.send(f"PRIVMSG NickServ :IDENTIFY {IRC_NICKSERV_PASS}")

                    time.sleep(2)

                    self.send("JOIN #perm8")

                    time.sleep(1)

                    self.send("NOTICE moo :!perm8")


                self.handle_line(line)


    def handle_line(self, line):

        lower = line.lower()

        # =====================
        # MD5 CHALLENGE
        # =====================

        if "moo" in lower and "!md5" in lower:

            match = re.search(r"!md5\s+(.+)", line)

            if match:

                text = match.group(1).replace("\x01", "").strip()

                md5 = hashlib.md5(text.encode()).hexdigest()

                print("[*] MD5:", text, "->", md5)

                self.send(f"NOTICE moo :!perm8-result {md5}")


        # =====================
        # VERSION REQUEST
        # =====================

        if "\x01version\x01" in lower:

            nick = line.split("!")[0][1:]

            self.send(f"NOTICE {nick} :\x01VERSION {BOT_VERSION}\x01")


        # =====================
        # ATTACK COMMAND
        # =====================

        if "moo" in lower and "!perm8-attack" in lower:

            print("[!] Attack started")

            self.attack_mode = True

            self.send("JOIN #takeoverz")


        # =====================
        # GOT OP
        # =====================

        if "mode #takeoverz +o" in lower and IRC_NICK.lower() in lower:

            print("[+] GOT OP!")

            self.send("KICK #takeoverz moo :!perm8")

            self.attack_mode = False


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    try:
        bot = IRCBot()
        bot.run()

    except KeyboardInterrupt:
        print("\n[*] Bot stopped")