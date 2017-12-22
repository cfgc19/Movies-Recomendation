# Movies-Recomendation


# Interfaces gráficas
GUI_sent_analysis.py

Ao correr este script é possível fazer uma de duas ações:
1 - Obter o score referente a uma review existente no dataset - para isto é necessário selecionar um filme e um utilizador

2 - Inserir uma nova review para um filme existente no dataset - no final é devolvido o score dessa mesma review

GUI_recommendation.py

Deve ser selecionado um utilizador - posteriormente irão ser mostradas três caixas de texto: a primeira contém o nome do filme que é recomendado; a segunda contém o ID do user que gostou desse mesmo filme; a terceira contém os filmes gostados pelo utilizador ao qual é feita a recomendação; na quarta encontram-se dois nomes de filmes adicionais que podem também ser do agrado do utilizador.

# Outros scripts

write_dataset_with_movies.py
Funções que permitiram completar o dataset através do acesso à API do Amazon.

open_data.py
Funções que permitem aceder aos dados, fazendo a triagem dos mesmos.

sent_analysis.py
Funções utilizadas na fase de análise de sentimentos.

analyse_sent_scores.py
Análise dos scores obtidos por todos os métodos implementados na fase de análise de sentimentos, com vista à obtenção de um score final.

recommender_system.py
Funções utilizadas na construção do sistema de recomendação.
