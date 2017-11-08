import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;

public class Server implements Transfere {
    public Server() {}

    public void envia(String nome, byte[] dados, int tamanho){
        try{
            File arquivo = new File(nome);
            arquivo.createNewFile();
            FileOutputStream out = new FileOutputStream(arquivo,true);
            out.write(dados, 0, tamanho);
            out.flush();
            out.close();
            System.out.println("Recebendo dados do arquivo " + nome + "...");
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public static void main (String[] args) {
        System.setProperty("java.rmi.server.hostname", "192.168.0.10");

        try {
            Server obj = new Server();
            Transfere stub = (Transfere) UnicastRemoteObject.exportObject(obj, 0);
            Registry registry = LocateRegistry.getRegistry();
            registry.bind("Transfere", stub);
            System.err.println("Servidor pronto!");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
