import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

public class Client extends Thread {

	public Socket socket;
	private static String okMsg = "OK";
	private static String startGame = "START";
	BufferedReader socketReader;
	public PrintWriter socketWriter;
	private boolean authenticated;
	public int pozX, pozY;
	public int spawnX, spawnY;
	public ArrayList<Bomba> bombs;
	public final int gasit = 0;

	public ArrayList<Integer> powerUp;
	public String userName;
	public int lives;
	public int clientId;
	private Server server;
	private int gameId;

	public Client(Socket socket, Server server) {
		this.socket = socket;
		this.authenticated = false;
		this.server = server;
		this.powerUp = new ArrayList<Integer>();
		bombs = new ArrayList<Bomba>();

		try {
			this.socketReader = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
			this.socketWriter = new PrintWriter(new OutputStreamWriter(
					socket.getOutputStream()), true);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void run() {
		String message;
		Update t = null;
		while (true) {
			try {
				message = socketReader.readLine();
				System.out.println(message);
				if (authenticated == false) {
					if (message.charAt(0) == '0') {
						handleClient(message);
						t=new Update(server,this);
					
						t.start();
					
					} else {
						continue;
					}
				}
				if (message.charAt(0) == '1') {
					createNewGame();
					t.gasit=1;
				} else if (message.charAt(0) == '2') {
					joinGame(message);
					t.gasit=1;
				} else if (message.charAt(0) == '3') {
					startGame();
					
				} else if (message.charAt(0) == '4') {
					// 4 reprezinta mesaj de miscare
					attemptMove(message);
				} else if (message.charAt(0) == '5') {
					// clientul doreste sa puna bomba la pozitia la care se afla
					putBomb();
				} else if (message.charAt(0) == '9') {
					for (Client client : server.games.get(gameId).getClients()) {
					    String messageAux=message.substring(1);
					    message="9";
					    message+=(char)this.userName.length();
					    message+=this.userName;
					    message+=(char)messageAux.length();
					    message+=messageAux;
						client.sendMessage(message);
					}
				}

			} catch (IOException e) {
				e.printStackTrace();
				return;
			}
		}
	}

	synchronized void putBomb() {
		// daca numarul de bombe puse deja depaseste limita
		if (bombs.size() >= 1)
			return;
		/*
		 * Map.Entry<Integer,Integer> bomb = new
		 * AbstractMap.SimpleEntry<Integer, Integer>(pozX,pozY);
		 * bombs.add(bomb);
		 */

		Bomba bomba = new Bomba(server.getGameWorld(gameId), clientId, 4, pozX,
				pozY);
		bombs.add(bomba);
		bomba.start();

	}

	boolean handleClient(String message) {
		System.out.println(message);
		String userName = getUserName(message);
		this.userName=userName;
		String passwd = getPasswd(message);
		System.out.println(userName + " " + passwd);
		// if handle client successfully set authenticated
		if (server.clientExists(userName, passwd)) {
			authenticated = true;
			sendMessage("ok");
			System.out.println("ok");
		} else {
			sendMessage("not ok");
		}
		return true;
	}

	String getUserName(String message) {
		return message.substring(2, message.indexOf(' ', 2));
	}

	String getPasswd(String message) {
		return message.substring(message.indexOf(' ',message.indexOf(' ', 2)) + 1);
	}

	synchronized boolean createNewGame() {
		sendOk(1);
		server.createNewGame(this);
		gameId = server.getSize();
	
		return true;
	}

	synchronized void attemptMove(String message) {
		char dir = message.charAt(1);
		int newPozx = pozX;
		int newPozy = pozY;
		if (dir == '1')
			newPozy += 1;
		if (dir == '2')
			newPozx += 1;
		if (dir == '3')
			newPozy -= 1;
		if (dir == '4')
			newPozx -= 1;
		GameWorld joc = server.getGameWorld(gameId);
		if (joc.map[newPozx][newPozy] == 1)
			return;
		
		if (joc.map[newPozx][newPozy] == 2)
			return;
		
		if (joc.map[newPozx][newPozy] >= 21 && joc.map[newPozx][newPozy] <= 25)
			return;

		int i, j;
		
		// verific bombele sale
		for (i = 0; i < bombs.size(); i++) {
			int bombX = bombs.get(i).posX;
			int bombY = bombs.get(i).posY;
			if (bombX == newPozx && bombY == newPozy)
				return;
		}

		for (i = 0; i < joc.getClients().size(); i++) {
			if (i != clientId) {
				// verific bombele celorlalti jucatori
				Client juc = joc.getClients().get(i);
				for (j = 0; j < bombs.size(); j++) {
					int bombX = bombs.get(j).posX;
					int bombY = bombs.get(j).posY;
					if (bombX == newPozx && bombY == newPozy)
						return;
				}
				// verific pozitia celorlalti jucatori
				if (newPozx == juc.pozX && newPozy == juc.pozY)
					return;
			}
		}
		// inseamna ca se poate muta acolo
		System.out.println(pozX+" "+pozY+" "+newPozx+" "+newPozy);
		pozX = newPozx;
		pozY = newPozy;
	}

	boolean joinGame(String message) {
		gameId = Integer.parseInt(message.substring(1, message.length()));
		sendOk(2);
		server.joinGame(this, gameId);
		
		return true;
	}

	void sendOk(int tip) {
		sendMessage(okMsg + " " +tip);
	}

	synchronized void sendMessage(String message) {
		this.socketWriter.write(message);
		this.socketWriter.flush();
	}

	boolean startGame() {
		server.startGame(gameId);
		
		return true;
	}

	void notifyStart() {
		sendOk(3);
	}

	void update() {
		sendMessage(server.getGameWorld(this.gameId)
				.stringifyMap(this.clientId));
	}
	
	Server getServer() {
		return server;
	}
	
}
