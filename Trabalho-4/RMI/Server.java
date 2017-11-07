import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;

public class Server implements Transfere {
    public Server() {}

    public boolean envia(String nome, byte[] dados, int tamanho){
        try{
            File arquivo = new File("foto-teste.jpg");
            arquivo.createNewFile();
            FileOutputStream out = new FileOutputStream(arquivo,true);
            out.write(dados, 0, tamanho);
            out.flush();
            out.close();
            System.out.println("Done writing data...");
        }catch(Exception e){
            e.printStackTrace();
        }
        return true;
    }

    public static void main (String[] args) {
        try {
            Server obj = new Server();
            Transfere stub = (Transfere) UnicastRemoteObject.exportObject(obj, 0);
            Registry registry = LocateRegistry.getRegistry();
            registry.bind("Transfere", stub);
            System.err.println("Server ready");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
