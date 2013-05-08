import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Server extends Thread {

	private static ServerSocket mSocketServer;
	private static ArrayList<GameWorld> games;
	private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
	public Server(int port) {
		try {
			mSocketServer = new ServerSocket(port);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void run() {
		while (true) {
			try {
				Socket socket = mSocketServer.accept();
				System.out.println("client connected " + socket.getInetAddress());
				Client client=new Client(socket,this);
				client.start();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void createNewGame(Client owner) {
		GameWorld newGame = new GameWorld(owner, games.size());
		games.add(newGame);
		owner.clientId = 0;
		newGame.addClient(owner);
	}
	
	public void joinGame(Client client, int id) {
		games.get(id).addClient(client);
		client.clientId = games.get(id).getClients().size() - 1;
	}
	
	public int getSize() {
		return games.size() - 1;
	}
	
	public GameWorld getGameWorld(int id) {
		return games.get(id);
	}
	public void startGame(final int id) {
		for (Client client:games.get(id).getClients()) {
			client.notifyStart();
		}
		GameWorld game=games.get(id);
		game.init();
		scheduler.scheduleAtFixedRate(new Runnable() {
			
			@Override
			public void run() {
				for (Client client:games.get(id).getClients()) {
					client.update();
				}	
			}
		}, 0, 300, TimeUnit.MILLISECONDS);
	}
	
	public static void main(String args[]) {
		Server s = new Server(25000);
		s.start();
	}
}
