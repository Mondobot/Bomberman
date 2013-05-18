import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Map;


public class Bomba extends Thread {
	public int ownerId;
	public int radius;
	public int posX;
	public int posY;
	public GameWorld game;
	public ArrayList<Map.Entry<Integer, Integer>> explozii;
	public Bomba(GameWorld game, int ownerId,int radius,int posX,int posY)
	{
		this.game=game;
		this.ownerId=ownerId;
		this.radius=radius;
		this.posX=posX;
		this.posY=posY;
		explozii = new ArrayList<Map.Entry<Integer, Integer>>();
	}
	public void run()
	{
		try {
			Thread.sleep(3000);
			kill();
			Thread.sleep(500);
			explozii.clear();
			removeBomb();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public synchronized void removeBomb()
	{
		Client owner=game.getClients().get(ownerId);
		int i;
		for (i=0;i<owner.bombs.size();i++)
		{
			if (owner.bombs.get(i).posX==posX && owner.bombs.get(i).posY==posY)
			{
				owner.bombs.remove(i);
				return ;
			}
		}
	}
	public synchronized void kill()
	{
		int i,j;
		Client curent=game.getClients().get(ownerId);
		ArrayList<Client> decedati=new ArrayList<Client>();
		Map.Entry<Integer,Integer> expl =
			    new AbstractMap.SimpleEntry<Integer, Integer>(posX,posY);
		explozii.add(expl);
		Map.Entry<Integer,Integer> rad =
			    new AbstractMap.SimpleEntry<Integer, Integer>(radius,0);
		explozii.add(rad);
		int q,dir1=0,dir2=0;
		
		for (j=0;j<game.getClients().size();j++)
		{
			Client cli=game.getClients().get(j);
			if (cli.pozX==posX && cli.pozY==posY)
			{
				decedati.add(cli);
				
			}
		}
		
		
		for (q=1;q<=4;q++)
		{
			if (q==1)
			{
				dir1=0;
				dir2=1;
			}
			if (q==2)
			{
				dir1=0;
				dir2=-1;
			}
			if (q==3)
			{
				dir1=1;
				dir2=0;
			}
			if (q==4)
			{
				dir1=-1;
				dir2=0;
			}
			boolean gasit=false;
			for (i=1;i<=radius && gasit==false;i++)
			{
				Map.Entry<Integer,Integer> explozie =
					    new AbstractMap.SimpleEntry<Integer, Integer>(posX+i*dir1,posY+i*dir2);
				if (game.map[posX+i*dir1][posY+i*dir2]==1)
				{
					break;
				}
				if (game.map[posX+i*dir1][posY+i*dir2]==2)
				{
					
					//explozii.add(explozie);
					game.map[posX+i*dir1][posY+i*dir2]=0;
					break;
				}
				for (j=0;j<game.getClients().size();j++)
				{
					Client cli=game.getClients().get(j);
					if (cli.pozX==posX+i*dir1 && cli.pozY==posY+i*dir2)
					{
						gasit=true;
						//explozii.add(explozie);
						
						decedati.add(cli);
						
					}
				}
				if (game.map[posX+i*dir1][posY+i*dir2]>=21 && game.map[posX+i*dir1][posY+i*dir2]<=25)
				{
					
					gasit=true;
					//explozii.add(explozie);
					game.map[posX+i*dir1][posY+i*dir2]-=10;
					
				}
			}
		}
		for (i=0;i<decedati.size();i++)
		{
			Client cli=decedati.get(i);
			cli.lives=cli.lives-1;
			cli.pozX=cli.spawnX;
			cli.pozY=cli.spawnY;
		
		}
	}
}
