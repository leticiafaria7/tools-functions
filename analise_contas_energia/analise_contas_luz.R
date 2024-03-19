
# bibliotecas
library(tidyverse)
library(openxlsx)

# diretório de trabalho
setwd("G:\Meu Drive\5. Cursos\programming\tools-functions\analise_contas_energia")

# limpar ambiente
rm(list = ls())

# base de dados
contas_luz <- read.xlsx('contas_luz.xlsx')

# tratamentos
contas_luz <- contas_luz %>% 
  unite("ano_mes", ano_vencimento:mes_vencimento, remove = FALSE)

# gráficos
ggplot(contas_luz) +
  aes(x = ano_mes, y = `kwh/dia`) +
  geom_point() +
  geom_line(aes(group = 1)) +
  expand_limits(y = 0)









