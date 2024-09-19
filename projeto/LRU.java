import java.util.LinkedList;

public class LRU implements AlgoritmoDeSubstituicao{

    private LinkedList<Pair<Integer, Integer>> paginas;

    private int size;

    public LRU(int size) {
        this.size = size;
        this.paginas = new LinkedList<Pair<Integer, Integer>>();
    }

    @Override
    public Integer procurarPagina(Integer page) throws MissInterruption {
        for (Pair<Integer, Integer> pageAtual : this.paginas) {
            if (pageAtual.getPair1().equals(page)) {
                this.execucaoAlgoritmo(pageAtual);
                return pageAtual.getPair2();
            }
        }
        throw new MissInterruption();
    }

    @Override
    public void adicionaPagina(Pair<Integer, Integer> page) {
        if (this.size == this.paginas.size()) {
            this.paginas.removeFirst();
        } 
        this.paginas.addLast(page);
    }

    private void execucaoAlgoritmo(Pair<Integer, Integer> substituir) {
        this.paginas.remove(substituir);
        this.paginas.addLast(substituir);
    }
    
}