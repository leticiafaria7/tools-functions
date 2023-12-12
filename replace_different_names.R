# bibliotecas
library(stringr)
library(dplyr)
library(purrr)


# exemplo de comentários e nomes próprios
df_comentarios <- data.frame(
  comentario = c("O João foi ao mercado.", "Maria comprou flores.", "O João e a Maria são amigos.")
)

df_nomes_proprios <- data.frame(
  nome_proprio = c("João", "Maria")
) %>% 
  mutate(replace = 'nome_proprio')

# criar lista
lista_nomes_proprios <- purrr::set_names(df_nomes_proprios$replace, df_nomes_proprios$nome_proprio)

# aplicar função na coluna
df_comentarios <- df_comentarios %>% 
  mutate(comentario = str_replace_all(comentario, lista_nomes_proprios))

# printar tabela
df_comentarios



