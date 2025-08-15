package battlenet;

public class User implements Observer {
    private static User instance;
    public int health=100, maxHealth=100, gold=0, damage=5;
    public State state;
    public Location l;
    public boolean shieldUp=false;

    private User(){}
    public static synchronized User getInstance(){
        if(instance==null) instance = new User();
        return instance;
    }
    public void init(){
        UI.getInstance().addObserver(this);
        l = Hub.getInstance();
        state = Hub.getInstance();
        gold += 5; // starter coins
    }
    public void setState(State s){ this.state = s; }
    public void startOgre(){ l = OgrePit.getInstance(); setState(OgrePit.getInstance()); l.lookAround(); }
    public void startVampire(){ l = new VampireLair(this); setState(l); l.lookAround(); }
    public void startDragon(){ l = new DragonDen(this); setState(l); l.lookAround(); }
    public void startFinal(){ l = new FinalStage(this); setState(l); l.lookAround(); }

    @Override public void update(Message m) {
        if("UI".equals(m.topic)){
            String cmd = m.payload.trim().toLowerCase();
            switch (cmd){
                case "start game": l = Hub.getInstance(); setState(Hub.getInstance()); l.lookAround(); break;
                case "go to hub": l = Hub.getInstance(); setState(Hub.getInstance()); l.lookAround(); break;
                case "buy wooden": if(gold>=5){ gold-=5; damage=5; UI.getInstance().UIWrite("Bought Wooden Sword"); } break;
                case "buy enchanted": if(gold>=10){ gold-=10; damage=10; UI.getInstance().UIWrite("Bought Enchanted Sword"); } break;
                case "buy shield": if(gold>=15){ gold-=15; UI.getInstance().UIWrite("Bought Fire Shield"); } break;
                case "brew gold": new GoldenPotion().preparePotion(); maxHealth+=20; UI.getInstance().UIWrite("Max health now "+maxHealth); break;
                case "brew silver": new SilverPotion().preparePotion(); damage+=3; UI.getInstance().UIWrite("Damage now "+damage); break;
                case "pause": ControlPanel.getInstance().in(0); break;
                default: UI.getInstance().UIWrite("Unknown: " + cmd);
            }
        } else if("time".equals(m.topic)){
            UI.getInstance().UIWrite("Time up signal -> " + (l!=null? l.getClass().getSimpleName():""));
        } else if("sensor".equals(m.topic)){
            String[] parts = m.payload.split(":");
            if(parts.length==2 && "shield".equals(parts[0])){
                shieldUp = Boolean.parseBoolean(parts[1]);
            }
        }
    }
}
