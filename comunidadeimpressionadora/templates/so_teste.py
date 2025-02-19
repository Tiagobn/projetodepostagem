import hashlib

def gerar_chave(usuario):
    # Gera uma chave com base em uma string (como nome ou e-mail do usuário)
    base = f"chave-{usuario}-secreta"
    chave = hashlib.sha256(base.encode()).hexdigest()
    return chave[:16]  # Retorna uma chave de 16 caracteres

def validar_chave(usuario, chave_fornecida):
    # Verifica se a chave fornecida corresponde ao usuário
    chave_correta = gerar_chave(usuario)
    return chave_correta == chave_fornecida

# Exemplo de uso
usuario = "usuario_teste"
chave = gerar_chave(usuario)
print("Chave gerada:", chave)

# Testando validação
chave_valida = validar_chave(usuario, chave)
print("Chave válida?", chave_valida)

# Testando com chave errada
chave_errada = "1234567890abcdef"
print("Chave válida com erro?", validar_chave(usuario, chave_errada))
