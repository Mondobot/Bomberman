import java.util.ArrayList;
import java.util.Map;


public class GameWorld {

	private int id;
	private ArrayList<Client> clientList;
	private Client owner;
	int map[][];
	
	public void initMap()
	{
		int vect[][]={ 
				{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
				{1,31, 2, 2, 0, 2, 0, 0,24, 2,22, 0, 0, 0, 0, 0,34, 1},
				{1, 2, 1, 0, 1,22, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1},
				{1, 2,21, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1},
				{1,25, 1, 0, 1, 0, 1, 2, 1,21, 1, 0, 1, 0, 1, 0, 1, 1},
				{1, 0, 0, 0, 2,23, 2, 2, 2,22, 2,24, 0, 2, 2,21, 0, 1},
				{1, 0, 1, 0, 1, 2, 1, 0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 1},
			    {1, 0, 0, 0, 2,35, 2, 2, 0, 2, 0, 2,25, 0, 0, 2, 0, 1},
				{1, 0, 1, 0, 1, 0, 1,24, 1,21, 1, 2, 1, 2, 1, 2, 1, 1},
				{1, 2,21, 0, 0, 2, 0, 2, 0, 2, 0, 2,36, 2, 0, 2, 0, 1},
				{1, 2, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 1, 1},
				{1,23, 2, 2, 0,21, 0, 2, 0,23, 0, 2, 2, 2, 2,21, 0, 1},
				{1, 0, 1,22, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1},
				{1, 0, 0, 0,25, 2, 2, 0, 0,23, 0, 0, 0, 0, 0, 0, 0, 1},
				{1,32, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,33, 1},
				{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
				
				//0=gol; 1=indestructibil; 2= destructibil fara powerup
				//31-36=spawn points pt jucatori
				//11-15=powerup descoperit
				//21-25=powerup nedescoperit
				
		};
		map=vect;
		

	}
	public void init()
	{
		int i,u,t;
		for (i=0;i<clientList.size();i++)
		{
			Client juc=clientList.get(i);
			for (u=0;u<map.length;u++)
				for (t=0;t<map[0].length;t++)
				{
					if (map[u][t]==30+i+1)
					{
						juc.pozX=u;
						juc.pozY=t;
						juc.spawnX=u;
						juc.spawnY=t;
						juc.lives=3;
					}
				}
		}
	}
	public GameWorld(Client owner, int id) {
		this.id = id;
		this.owner = owner;
		initMap();
	}
	
	public void addClient(Client client) {
		this.clientList.add(client);
	}
	
	public ArrayList<Client> getClients() {
		return clientList;
	}
	
	public String stringifyMap(int clientId) {
		String string = "";
		string += (char) map.length;
		string += (char) map[0].length;
		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[i].length; j++) {
				string += (char) map[i][j];
			}
		}
		string += (char) clientId;
		string += (char) clientList.size();
		for (Client client: clientList) {
			string += (char)client.pozX;
			string += (char)client.pozY;
		}
		for (Client client: clientList) {
			string += (char) client.bombs.size();
			for (Bomba bomb: client.bombs) {
				string += (char)bomb.posX;
				string += (char)bomb.posY;
			}
		}
		for (Client client: clientList) {
			for (Bomba bomb: client.bombs) {
				string += (char) bomb.explozii.size();
				for (Map.Entry<Integer, Integer> explozie: bomb.explozii) {
					string += (char)explozie.getKey().intValue();
					string += (char)explozie.getValue().intValue();
				}
			}
		}
		for (Client client: clientList) {
			for (Integer power:client.powerUp) {
				string += (char) power.intValue();
			}
		}
		return string;
	}
}
