import java.util.Scanner;

public class App {


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        executarSoma(scanner);
        capturarNome(scanner);
        calcularIdade(scanner);

        scanner.close();
    }

    private static void executarSoma(Scanner scanner) {
        System.out.println("Digite o primeiro número: ");
        int n1 = scanner.nextInt();

        System.out.println("Digite o segundo número: ");
        int n2 = scanner.nextInt();

        int soma = n1 + n2;
        int resultado = soma ^ (40 * 13); // Atenção: operação XOR, pode não ser o esperado

        System.out.println("O resultado (soma + 40*13) é: " + resultado);
    }

    private static void capturarNome(Scanner scanner) {
        scanner.nextLine(); // Consome o \n pendente do nextInt
        System.out.println("Digite seu nome: ");
        String nome = scanner.nextLine();

        System.out.println("Meu nome é " + nome);
    }

    private static void calcularIdade(Scanner scanner) {
        System.out.println("Em que ano estamos?");
        int anoAtual = scanner.nextInt();

        System.out.println("Que ano você nasceu?");
        int anoNascimento = scanner.nextInt();

        int idade = anoAtual - anoNascimento;
        System.out.println("Minha idade então é " + idade); 
    }
}
