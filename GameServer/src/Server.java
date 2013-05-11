import java.io.File;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class Server extends Thread {

	private static ServerSocket mSocketServer;
	private static ArrayList<GameWorld> games;
	private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
	private DocumentBuilderFactory factory;
	private DocumentBuilder parser;
	private File database;
	private Document doc;
	public Server(int port) {
		try {
			database = new File("database.xml");
			mSocketServer = new ServerSocket(port);
			factory = DocumentBuilderFactory.newInstance();
			parser = factory.newDocumentBuilder();
			if (!database.exists()) {
				database.createNewFile();
				doc = parser.newDocument();
				Element root = doc.createElement("users");
				doc.appendChild(root);
				TransformerFactory transformerFactory = TransformerFactory.newInstance();
				Transformer transformer = transformerFactory.newTransformer();
				transformer.transform(new DOMSource(doc), new StreamResult(database));
			}
			doc = parser.parse(database);
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (TransformerConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (TransformerException e) {
			// TODO Auto-generated catch block
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
	
	public boolean clientExists(String nickname, String passwd) {
		NodeList existingClients = doc.getElementsByTagName("user");
		for (int i = 0; i < existingClients.getLength(); i++) {
			Element client = (Element) existingClients.item(i);
			if (client.getElementsByTagName("nickname").item(0).getTextContent().equals(nickname)&&
					client.getElementsByTagName("passwd").item(0).getTextContent().equals(passwd)) {
				return true;
			}
		}
		return false;
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
