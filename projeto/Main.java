public class Main {

    public static void main(String[] args) throws MissInterruption {
        Pair<Integer, Integer> p1 = new Pair<Integer, Integer>(1, 1);
        Pair<Integer, Integer> p2 = new Pair<Integer, Integer>(2, 2);
        Pair<Integer, Integer> p3 = new Pair<Integer, Integer>(3, 3);
        Pair<Integer, Integer> p4 = new Pair<Integer, Integer>(4, 4);
        Pair<Integer, Integer> p5 = new Pair<Integer, Integer>(5, 5);

        LRU l = new LRU(4);
        l.adicionaPagina(p1);
        l.adicionaPagina(p2);
        l.adicionaPagina(p3);
        l.adicionaPagina(p4);
        l.adicionaPagina(p5);
        l.procurarPagina(3);
    }
    
}
