public class TLB {
    private AlgoritmoDeSubstituicao algoritmo;

    private int quantidadeDeMiss;

    private int quantidadeDeHit;

    public TLB(AlgoritmoDeSubstituicao algoritmo) {
        this.algoritmo = algoritmo;
        this.quantidadeDeMiss = 0;
        this.quantidadeDeHit = 0;
    }

    public int getMissRatio() {
        return quantidadeDeMiss;
    }

    public int getHitRatio() {
        return quantidadeDeHit;
    }

    public Integer mapearPagina(Integer page) throws Exception {
        try {
            this.quantidadeDeHit++;
            return this.algoritmo.procurarPagina(page);
        } catch (MissInterruption miss) {
            this.quantidadeDeMiss++;
            throw new MissInterruption();
        }
    }

    public void adicionarPagina(Pair<Integer, Integer> paginaMapina) {
        this.algoritmo.adicionaPagina(paginaMapina);
    }

}