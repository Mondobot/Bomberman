import java.util.ArrayList;
import java.util.Map;

public class GameWorld {

	public int id;
	private ArrayList<Client> clientList;
	public Client owner;
	int map[][];
	int started;

	public void initMap() {
		int vect[][] = {
				{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
				{ 1, 0, 0, 2, 0, 2, 0, 0, 24, 2, 22, 0, 0, 0, 0, 0, 34, 1 },
				{ 1, 31, 1, 0, 1, 22, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1 },
				{ 1, 2, 21, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1 },
				{ 1, 25, 1, 0, 1, 0, 1, 2, 1, 21, 1, 0, 1, 0, 1, 0, 1, 1 },
				{ 1, 0, 0, 0, 2, 23, 2, 2, 2, 22, 2, 24, 0, 2, 2, 21, 0, 1 },
				{ 1, 0, 1, 0, 1, 2, 1, 0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 1 },
				{ 1, 0, 0, 0, 2, 35, 2, 2, 0, 2, 0, 2, 25, 0, 0, 2, 0, 1 },
				{ 1, 0, 1, 0, 1, 0, 1, 24, 1, 21, 1, 2, 1, 2, 1, 2, 1, 1 },
				{ 1, 2, 21, 0, 0, 2, 0, 2, 0, 2, 0, 2, 36, 2, 0, 2, 0, 1 },
				{ 1, 2, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 1, 1 },
				{ 1, 23, 2, 2, 0, 21, 0, 2, 0, 23, 0, 2, 2, 2, 2, 21, 0, 1 },
				{ 1, 0, 1, 22, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1 },
				{ 1, 0, 0, 0, 25, 2, 2, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 1 },
				{ 1, 32, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 33, 1 },
				{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },

		// 0=gol; 1=indestructibil; 2= destructibil fara powerup
		// 31-36=spawn points pt jucatori
		// 11-15=powerup descoperit
		// 21-25=powerup nedescoperit

		};

		map = vect;

	}

	public void init() {
		int i, u, t;
		started = 1;
		for (i = 0; i < clientList.size(); i++) {

			Client juc = clientList.get(i);
			for (u = 0; u < map.length; u++)
				for (t = 0; t < map[0].length; t++) {
					if (map[u][t] == 30 + i + 1) {
						juc.pozX = u;
						juc.pozY = t;
						juc.spawnX = u;
						juc.spawnY = t;
						juc.lives = 3;
					}
				}
		}
	}

	public GameWorld(Client owner, int id) {
		this.id = id;
		this.owner = owner;
		started = 0;
		clientList = new ArrayList<Client>();
		initMap();
	}

	public void addClient(Client client) {
		this.clientList.add(client);
		info();
	}

	public ArrayList<Client> getClients() {
		return clientList;
	}

	public String stringifyMap(int clientId) {
		String string = "6";
		string += (char) map.length;
		string += (char) map[0].length;
		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[i].length; j++) {
				string += (char) map[i][j];
			}
		}
		string += (char) clientId;
		System.out.println(clientId);
		string += (char) clientList.size();

		for (Client client : clientList) {
			string += (char) client.pozY;
			string += (char) client.pozX;
		}
		int size = 0;
		for (Client client : clientList) {
			size += client.bombs.size();
		}

		string += (char) size;
		for (Client client : clientList) {
			for (Bomba bomb : client.bombs) {
				string += (char) bomb.posY;
				string += (char) bomb.posX;
			}
		}

		size = 0;
		for (Client client : clientList) {
			for (Bomba bomb : client.bombs) {
				size += bomb.explozii.size();
			}
		}
		string += (char) (size / 2);
		for (Client client : clientList) {
			for (Bomba bomb : client.bombs) {
				for (Map.Entry<Integer, Integer> explozie : bomb.explozii) {

					string += (char) explozie.getValue().intValue();
					string += (char) explozie.getKey().intValue();
				}
			}
		}
		return string;
	}

	public void info() {

		// nr jucatori, lista
		String message = "8";
		message+=(char)clientList.size();
		for (int i = 0; i < clientList.size(); i++) {
			message+=(char)clientList.get(i).userName.length();
			message+=clientList.get(i).userName;
		}
		for (Client client: clientList) {
			client.sendMessage(message);
		}

	}
}
