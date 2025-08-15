package battlenet;

import java.io.*;
import java.net.Socket;
import java.util.Map;
import java.util.HashMap;

public class TCP_Client implements Runnable {
    private static TCP_Client instance;
    private String host="127.0.0.1";
    private int port=5050;
    private volatile boolean running=true;
    private TCP_Client(){}
    public static synchronized TCP_Client getInstance(){ if(instance==null) instance=new TCP_Client(); return instance; }
    public void configure(String host, int port){ this.host=host; this.port=port; }
    public void stop(){ running=false; }

    @Override public void run() {
        try (Socket socket = new Socket(host, port)) {
            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String line;
            while(running && (line = br.readLine()) != null){
                // naive JSON parse for key:value pairs
                Map<String,String> kv = parse(line.trim());
                evaluate(kv);
            }
        } catch (Exception e){
            UI.getInstance().UIWrite("Sensor client error: "+e.getMessage());
        }
    }

    private Map<String,String> parse(String json){
        Map<String,String> m = new HashMap<>();
        json = json.replaceAll("[{}\" ]","");
        for(String p: json.split(",")){
            if(p.contains(":")){
                String[] kv = p.split(":",2);
                m.put(kv[0], kv[1]);
            }
        }
        return m;
    }

    private void evaluate(Map<String,String> m){
        try {
            double az = Double.parseDouble(m.getOrDefault("accelerometerAccelerationZ","0"));
            double gx = Double.parseDouble(m.getOrDefault("gyroRotationX","1"));
            double gy = Double.parseDouble(m.getOrDefault("gyroRotationY","1"));
            double gz = Double.parseDouble(m.getOrDefault("gyroRotationZ","1"));
            float db = Float.parseFloat(m.getOrDefault("avAudioRecorderAveragePower","-100"));

            boolean attack = (az < -1.02) || (az > -0.96);
            boolean shield = (gx > -0.1 && gx < 0.1) && (gy > -0.1 && gy < 0.1) && (gz > -0.1 && gz < 0.1);
            boolean noisy = (db > -30.0f);

            if(shield){
                UI.getInstance().publishMessage(new Message(this, "sensor", "shield:true"));
                UI.getInstance().UIWrite("[Sensor] Shield Activated");
            } else if(attack){
                UI.getInstance().UIWrite("[Sensor] Attack swing!");
            }
            if(noisy){
                UI.getInstance().UIWrite("[Sensor] Noise detected in stealth stage!");
            }
        } catch (Exception ignored){}
    }
}
