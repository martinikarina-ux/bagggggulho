
# Solicitamos o peso e a altura do usuário
# Usamos 'float' para permitir números decimais (ex: 70.5 ou 1.75)
peso = float(input("Digite o seu peso (em kg): "))
altura = float(input("Digite a sua altura (em metros, ex: 1.75): "))

# Cálculo do IMC: peso dividido pela altura elevada ao quadrado
imc = peso / (altura ** 2)

# Exibe o valor do IMC formatado com duas casas decimais
print(f"\nSeu IMC é: {imc:.2f}")

# Estrutura condicional para classificar o IMC
if imc < 18.5:
    print("Classificação: Abaixo do peso")
    
elif 18.5 <= imc < 25:
    # Esta linha avalia se o IMC está entre 18.5 (inclusive) e menos que 25
    print("Classificação: Peso normal")
    
else:
    # Se não for nenhum dos anteriores, com certeza é 25 ou mais
    print("Classificação: Acima do peso")