package battlenet;

public class Main {
    public static void main(String[] args) {
        // Boot the game: start UI input thread, sensor thread, and enter Hub state
        UI ui = UI.getInstance();
        User player = User.getInstance();
        player.init();
        new Thread(ui).start();                  // keyboard input
        new Thread(TCP_Client.getInstance()).start(); // sensor stream
        System.out.println("Battle Network started. Type 'start game' to begin.");
    }
}
