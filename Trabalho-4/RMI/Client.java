import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.*;

public class Client {
    public static void main(String[] args) {

        if (args.length != 2) {
            System.out.println("MODO DE USAR: java Client <IP do server> <nome do arquivo>");
        }

        try {
            Registry registry = LocateRegistry.getRegistry(args[0]);
            Transfere stub = (Transfere) registry.lookup("Transfere");
            byte[] dados = new byte[1048576];
            FileInputStream entrada = new FileInputStream(args[1]);
            int qtddLida = entrada.read(dados);

            while (qtddLida > 0) {
                boolean response = stub.envia(args[1], dados, qtddLida);
                System.out.println("Transferido " + qtddLida + " bytes do arquivo " + args[1]);
                qtddLida = entrada.read(dados);
            }

        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
