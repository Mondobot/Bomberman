
public class Update extends Thread {
	int gasit;
	Server server;
	Client client;
	public Update(Server server,Client client)
	{
		gasit=0;
		this.server=server;
		this.client=client;
				
	}
	public void run()
	{
		
		while (gasit==0)
		{
			//cate jocuri sunt, idul jocului, numar de cifre nume,nume,nr jucatori
			String message="7";
			int num=0;
			for (int i=0;i<server.games.size();i++)
			{
				if (server.games.get(i).started==0)
				{
					num++;
				}
			}
			message+=(char)num;
			
			for (int i=0;i<server.games.size();i++)
			{
				if (server.games.get(i).started==0)
				{
					message+=(char)server.games.get(i).id;
					message+=(char)server.games.get(i).owner.userName.length();
					message+=server.games.get(i).owner.userName;
					message+=(char)server.games.get(i).getClients().size();
				}
			}
			
			client.sendMessage(message);
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
