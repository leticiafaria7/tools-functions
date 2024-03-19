
# bibliotecas
library(tidyverse)
library(openxlsx)

# diretório de trabalho
setwd("G:/Meu Drive/5. Cursos/programming/tools-functions/analise_contas_energia")

# limpar ambiente
rm(list = ls())

# base de dados
contas_luz <- read.xlsx('contas_luz.xlsx')

# tratamentos
contas_luz <- contas_luz %>%
  mutate(mes_vencimento_str = case_when(mes_vencimento < 10 ~ paste0("0", mes_vencimento),
                                        TRUE ~ as.character(mes_vencimento))) %>% 
  mutate(ano_mes = paste0(ano_vencimento, '_', mes_vencimento_str))

# gráficos
ggplot(contas_luz) +
  aes(x = ano_mes, y = `kwh/dia`) +
  geom_point() +
  geom_line(aes(group = 1)) +
  expand_limits(y = 0)

ggplot(contas_luz) +
  aes(x = ano_mes, y = valor_a_pagar) +
  geom_point() +
  geom_line(aes(group = 1)) +
  expand_limits(y = 0)

ggplot(contas_luz) +
  aes(x = ano_mes, y = preco_atual) +
  geom_point() +
  geom_line(aes(group = 1)) +
  expand_limits(y = 0)







