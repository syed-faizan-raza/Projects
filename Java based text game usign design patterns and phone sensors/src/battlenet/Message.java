package battlenet;

public class Message {
    public Object sender;
    public String topic;
    public String payload;
    public Message(Object sender, String topic, String payload) {
        this.sender = sender;
        this.topic = topic;
        this.payload = payload;
    }
}
