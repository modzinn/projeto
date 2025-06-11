import java.util.Scanner;

public class conversor{

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Quantos Reais eu tenho? ");
 
         double reais = scanner.nextFloat();
         double dolares = reais / 5.56;

         System.out.printf("posso ter %.2f dolares\n ",dolares);
         
         temp(scanner);
         taxa(scanner);
         emprestimo(scanner);
         scanner.close();
    }
    private static void temp(Scanner scanner){
        System.out.println("Qual é a temperatura aqui? ");

        double F = scanner.nextDouble();
        double C = (F - 32) / 1.8;
        
        System.out.printf("Aqui está %.1f graus celcius\n", C);
    }
    public static void taxa(Scanner scanner){
        System.out.println("Qual é o valor do produto? ");
        double preco = scanner.nextDouble();
        double imposto = preco * 60 / 100; 
        System.out.printf("O imposto será de %.2f\n", imposto);

    }
    private static void emprestimo(Scanner scanner) {
    System.out.print("Qual é o valor do empréstimo? ");
    double valor = scanner.nextDouble();

    double juros = 0.20; // 20% de juros
    double totalComJuros = valor * (1 + juros);

    System.out.print("Em quantas parcelas você quer pagar? ");
    int parcelas = scanner.nextInt();

    double valorParcela = totalComJuros / parcelas;

    System.out.printf("O valor do seu empréstimo com os juros será R$ %.2f por mês (%d parcelas).%n", valorParcela, parcelas);
    }
 }
