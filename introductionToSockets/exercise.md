**Team-Mitglied 1**: Sarah Tiefert <br>
**Team-Mitglied 2**: Alexander Brese

## 4.1 Lokale Kommunikation

### für jedes gesendete Paket bestimmen, welcher Befehl in welchem Skript (Client/Server) dafür verantwortlich ist, dass das Paket gesendet wird
- 4	11:51:52.137186	127.0.0.1	127.0.0.2	TCP	44	2152 → 5000 [ACK] Seq=2 Ack=2 Win=10233 Len=0
- 5	11:52:09.558407	127.0.0.1	127.0.0.2	TCP	56	2210 → 5000 [SYN] Seq=0 Win=65535 Len=0 MSS=65495 WS=256 SACK_PERM=1
- [client] self.clientSocket.connect((self.ip, self.port))
- 6	11:52:09.558435	127.0.0.2	127.0.0.1	TCP	56	5000 → 2210 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=65495 WS=256 SACK_PERM=1
- [server] connectionSocket, _ = self.serverSocket.accept()
- 7	11:52:09.558479	127.0.0.1	127.0.0.2	TCP	44	2210 → 5000 [ACK] Seq=1 Ack=1 Win=2619648 Len=0
### für jeden blockierenden Befehl bestimmen, die Ankunft welches Pakets dafür verantwortlich ist, dass die Ausführung des Befehls vervollständigt wird
- 7	11:52:09.558479	127.0.0.1	127.0.0.2	TCP	44	2210 → 5000 [ACK] Seq=1 Ack=1 Win=2619648 Len=0
- [server] connectionSocket, _ = self.serverSocket.accept()
- 9	11:52:11.720903	127.0.0.2	127.0.0.1	TCP	44	5000 → 2210 [ACK] Seq=1 Ack=32 Win=2619648 Len=0
- [server] msg = connectionSocket.recv(2048)
- 11	11:52:11.721253	127.0.0.1	127.0.0.2	TCP	44	2210 → 5000 [ACK] Seq=32 Ack=9 Win=2619648 Len=0
- [client] result = self.clientSocket.recv(2048)

## 4.2 Netzwerk-Kommunikation
### Wie können Sie im Client Python-Skript die IP-Adresse und Port-Nummer des verwendeten lokalen Sockets bestimmen (im Sinne von herausfinden)?
ipaddr, port = socket.getsockname()
### Wann (in welcher Code-Zeile) und woher erhält ein Client seine IP-Adresse und Port-Nummer?
[client] self.clientSocket.connect((self.ip, self.port))
### Wie können Sie im Client-Skript die IP-Adresse und Port-Nummer des Sockets setzen? 
socket.setsockopt
### Warum müssen Sie Timeouts verwenden und wie funktioniert try … except? Mit welchem Befehl können Sie einen gemeinsamen Timeout für alle Sockets setzen?
- Timeouts weil Pakete verloren gehen können und es anders nicht möglich ist zu sagen ob wein Paket verloren gegangen ist
- try versucht den Code im Block auszuführen, wenn eine exception geworfen wird führt es stattdessen den Code im entsprechenden except block aus
- Setzen des Timeouts für alle Sockets: socket.setdefaulttimeout(timeout)
### Finden Sie experimentell heraus, ob Sie einen Server betreiben können, der ECHO-Anfragen auf dem gleichen Port für UDP und TCP beantwortet?
Ja es geht aber es müssen zwei Sockets sein.

## 5.3 Fragen
### Geben Sie die Liste der offenen TCP und UDP Ports an. 
- TCP: [9,7,13,17,19]
- UDP: Alle 50
### Wählen Sie für TCP und UDP jeweils einen offenen und einen geschlossenen Port und erklären Sie die entsprechende Paketsequenz, die Sie in WireShark aufgezeichnet haben.
### Auf Port 7 des Servers läuft ein ECHO-Dienst. Testen Sie ihr Client-Script mit dem ECHOServer. Versuchen Sie das TCP und das UDP Script.

- tcp b'13:36:57 18.05.2021\n' port 13
- tcp b'Hello World!' port 7
- tcp b' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg\r\n!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_
`abcdefgh\r\n"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghi\r\n#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[
\\]^_`abcdefghij\r\n$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijk\r\n%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUV
WXYZ[\\]^_`abcdefghijkl\r\n&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklm\r\n\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQ
RSTUVWXYZ[\\]^_`abcdefghijklmn\r\n()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmno\r\n)*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN
OPQRSTUVWXYZ[\\]^_`abcdefghijklmnop\r\n*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopq\r\n+,-./0123456789:;<=>?@ABCDEFGHIJK
LMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqr\r\n,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrs\r\n-./0123456789:;<=>?@ABCDEFGH
IJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghij' port 19
- tcp b'"My spelling is Wobbly.  It\'s good spelling but it Wobbles, and the letters\r\n get in the wrong places." A. A. Milne (1882-1958)\r\x00' port 
17
- udp b'Hello World!' port 7
- udp b' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg\r\n!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_
`abcdefgh\r\n"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghi\r\n#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[
\\]^_`abcdefghij\r\n$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijk\r\n%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUV
WXYZ[\\]^_`abcdefghijkl\r\n&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklm\r\n\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQ
RSTUVWXYZ[\\]^_`abcdefghijklmn\r\n()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmno\r\n)*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN
OPQRSTUVWXYZ[\\]^_`abcdefghijklmnop\r\n*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopq\r\n+,-./0123456789:;<=>?@ABCDEFGHIJK
LMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqr\r\n,' port 19
- udp b'"Here\'s the rule for bargains: "Do other men, for they would do you."\r\n That\'s the true business precept." Charles Dickens (1812-70)\r\x00'
 port 17
- udp b'13:36:57 18.05.2021\n' port 13
