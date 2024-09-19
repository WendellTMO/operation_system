public interface AlgoritmoDeSubstituicao {
    
    public Integer procurarPagina(Integer page) throws MissInterruption;

    public void adicionaPagina(Pair<Integer, Integer> page);
}
