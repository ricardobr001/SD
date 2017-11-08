import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.*;

public class Client {
    public static void main(String[] args) {
        System.setProperty("java.rmi.server.hostname", "192.168.0.10");

        if (args.length != 2) {
            System.out.println("MODO DE USAR: java Client <IP do server> <nome do arquivo>");
        }

        try {
            Registry registry = LocateRegistry.getRegistry(args[0]);
            Transfere stub = (Transfere) registry.lookup("Transfere");
            byte[] dados = new byte[1048576];
            FileInputStream entrada = new FileInputStream(args[1]);
            int qtddLida = entrada.read(dados);

            System.out.println("Enviando o arquivo " + args[1] + "...");
            while (qtddLida > 0) {
                stub.envia(args[1], dados, qtddLida);
                qtddLida = entrada.read(dados);
            }

            System.out.println("Arquivo " + args[1] + " enviado!");
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}