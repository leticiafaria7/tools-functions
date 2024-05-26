
# a sequência de fibonacci é uma sequência onde cada número da sequência é a soma dos dois anteriores
# começa com 0 e 1

# o início da sequência fica assim:
# 0, 1, 1, 2, 3, 5, 8, 13, 21

# fazer uma função em que se imputa um valor n e a função retorna o n-ésimo número da sequência de fibonacci

rm(list = ls())

seq_fibonacci <- function(x) {
  
  if (class(x) != "numeric" | x - round(x) != 0) {
    
    return('a entrada deve ser um número inteiro')
    
  }
  
  if (x <= 0) {
    
    return('a entrada deve ser um número maior do que 0')
    
  }
  
  if (x == 1) {

    return(0)

  }
  
  if (x == 2) {
    
    return(1)
    
  } else {
    
    seq <- c(0, 1)
    
    i <- 3
    
    for (i in 3:x) {
      
      # valor a ser adicionado na sequência
      add <- seq[length(seq)] + seq[length(seq) - 1]
      
      # adicionando o valor na sequência
      seq[i] <- add
      
    }
    
    return(seq[x])
    
  }
  
}

# teste

seq_fibonacci(5)



