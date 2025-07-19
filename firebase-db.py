"""
Upload dos dados do Firebase para o Firestore e consulta de dados. Dados usados foram feitos no trabalho de BD e convertidos para este trabalho.
Firebase Firestore Data Migration and Query Script
Organized for clarity and maintainability.
"""

# Imports
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from collections import Counter

# Firestore Initialization

def init_firestore(key_path: str = 'key.json'):
    """Initialize Firestore client."""
    try:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Conexão com o Firestore estabelecida com sucesso!")
        return db
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")
        print("Por favor, verifique se o caminho para 'serviceAccountKey.json' está correto e se o arquivo existe.")
        return None

# Data Definitions

# --- Dados MySQL (convertidos para dicionários Python) ---
# Estamos usando os INSERTs convertidos para listas de dicionários Python.
# Observação: 'Foto' e 'Fotos' foram mantidos como None ou string de caminho.
# Datas e Horários foram convertidos para objetos date e time do Python.

# Seus dados originais
original_data = {
    'Empresa': [
        {'CodEmpresa': 1, 'CNPJ': '12345678000100'},
        {'CodEmpresa': 2, 'CNPJ': '12345678000101'},
        {'CodEmpresa': 3, 'CNPJ': '12345678000102'},
        {'CodEmpresa': 4, 'CNPJ': '12345678000103'},
        {'CodEmpresa': 5, 'CNPJ': '12345678000104'},
        {'CodEmpresa': 6, 'CNPJ': '12345678000105'},
        {'CodEmpresa': 7, 'CNPJ': '12345678901234'},
        {'CodEmpresa': 8, 'CNPJ': '56789012345678'},
        {'CodEmpresa': 9, 'CNPJ': '90123456789012'},
        {'CodEmpresa': 10, 'CNPJ': '34567890123456'},
        {'CodEmpresa': 11, 'CNPJ': '78901234567890'},
        {'CodEmpresa': 12, 'CNPJ': '23456789012345'}
    ],
    'Mao_de_Obra': [
        {'CodFuncionario': 1, 'Foto': None, 'Salario': 10000.00, 'RG': '123456789', 'CPF': '12300000800', 'Cargo': 'Engenheiro', 'Nome': 'Robson Neves'},
        {'CodFuncionario': 2, 'Foto': None, 'Salario': 8000.00, 'RG': '123456788', 'CPF': '32100000800', 'Cargo': 'Eletricista', 'Nome': 'Joana Nunes'},
        {'CodFuncionario': 3, 'Foto': None, 'Salario': 25000.00, 'RG': '123456787', 'CPF': '45600000800', 'Cargo': 'Engenheiro Civil', 'Nome': 'Johann Strauss'},
        {'CodFuncionario': 4, 'Foto': None, 'Salario': 4000.00, 'RG': '123456786', 'CPF': '65400000800', 'Cargo': 'Pedreiro', 'Nome': 'Robert Denilson'},
        {'CodFuncionario': 5, 'Foto': None, 'Salario': 7500.00, 'RG': '123456785', 'CPF': '78900000800', 'Cargo': 'Arquiteto', 'Nome': 'Sol da Silva'},
        {'CodFuncionario': 6, 'Foto': None, 'Salario': 6500.00, 'RG': '123456784', 'CPF': '98700000800', 'Cargo': 'Engenheiro', 'Nome': 'Julie Powers'},
        {'CodFuncionario': 7, 'Foto': 'caminho_foto7.jpg', 'Salario': 3000.00, 'RG': '123456701', 'CPF': '78901234567', 'Cargo': 'Pedreiro', 'Nome': 'João da Silva'},
        {'CodFuncionario': 8, 'Foto': 'caminho_foto8.jpg', 'Salario': 2500.00, 'RG': '765432102', 'CPF': '45678901234', 'Cargo': 'Eletricista', 'Nome': 'Maria Oliveira'},
        {'CodFuncionario': 9, 'Foto': 'caminho_foto9.jpg', 'Salario': 3500.00, 'RG': '987654303', 'CPF': '12345678901', 'Cargo': 'Encanador', 'Nome': 'Carlos Souza'},
        {'CodFuncionario': 10, 'Foto': 'caminho_foto10.jpg', 'Salario': 2800.00, 'RG': '345678904', 'CPF': '56789012345', 'Cargo': 'Carpinteiro', 'Nome': 'Ana Santos'},
        {'CodFuncionario': 11, 'Foto': 'caminho_foto11.jpg', 'Salario': 3200.00, 'RG': '876543205', 'CPF': '90123456789', 'Cargo': 'Pintor', 'Nome': 'Roberto Lima'},
        {'CodFuncionario': 12, 'Foto': 'caminho_foto12.jpg', 'Salario': 3000.00, 'RG': '234567806', 'CPF': '34567890123', 'Cargo': 'Mestre de Obras', 'Nome': 'Luiza Fernandes'}
    ],
    'Obra': [
        {'CodObra': 1, 'Endereco': 'Avenida Trobson Azambuja', 'Fotos': None, 'Data_inicio': datetime(2023, 5, 11), 'Data_previsao': datetime(2025, 6, 21)},
        {'CodObra': 2, 'Endereco': 'Avenida Relâmpago Marquinhos', 'Fotos': None, 'Data_inicio': datetime(2024, 8, 3), 'Data_previsao': datetime(2027, 3, 17)},
        {'CodObra': 3, 'Endereco': 'Avenida Paulista', 'Fotos': None, 'Data_inicio': datetime(2023, 7, 25), 'Data_previsao': datetime(2025, 8, 20)},
        {'CodObra': 4, 'Endereco': 'Rua Alexandre de Matos', 'Fotos': None, 'Data_inicio': datetime(2023, 8, 21), 'Data_previsao': datetime(2028, 1, 1)},
        {'CodObra': 5, 'Endereco': 'Rua Pennywise', 'Fotos': None, 'Data_inicio': datetime(2021, 4, 7), 'Data_previsao': datetime(2023, 12, 19)},
        {'CodObra': 6, 'Endereco': 'Rua Mitocôndria Azul', 'Fotos': None, 'Data_inicio': datetime(2022, 1, 17), 'Data_previsao': datetime(2024, 12, 11)},
        {'CodObra': 7, 'Endereco': 'Rua A, 123', 'Fotos': 'caminho_foto_obra7.jpg', 'Data_inicio': datetime(2025, 12, 7), 'Data_previsao': datetime(2028, 6, 10)},
        {'CodObra': 8, 'Endereco': 'Avenida B, 456', 'Fotos': 'caminho_foto_obra8.jpg', 'Data_inicio': datetime(2023, 2, 15), 'Data_previsao': datetime(2023, 8, 15)},
        {'CodObra': 9, 'Endereco': 'Rua C, 789', 'Fotos': 'caminho_foto_obra9.jpg', 'Data_inicio': datetime(2025, 3, 20), 'Data_previsao': datetime(2029, 9, 20)},
        {'CodObra': 10, 'Endereco': 'Avenida D, 101', 'Fotos': 'caminho_foto_obra10.jpg', 'Data_inicio': datetime(2023, 4, 25), 'Data_previsao': datetime(2025, 10, 25)},
        {'CodObra': 11, 'Endereco': 'Rua E, 112', 'Fotos': 'caminho_foto_obra11.jpg', 'Data_inicio': datetime(2021, 5, 30), 'Data_previsao': datetime(2024, 11, 30)},
        {'CodObra': 12, 'Endereco': 'Avenida F, 213', 'Fotos': 'caminho_foto_obra12.jpg', 'Data_inicio': datetime(2023, 6, 5), 'Data_previsao': datetime(2026, 12, 5)}
    ],
    'Proprietario': [
        {'CodProp': 1, 'NomeProp': 'Gideon Graves', 'CPF': '12355500812'},
        {'CodProp': 2, 'NomeProp': 'Ken Masters', 'CPF': '32306578450'},
        {'CodProp': 3, 'NomeProp': 'Sypha Belnades', 'CPF': '82468675806'},
        {'CodProp': 4, 'NomeProp': 'Ramza Beoulve', 'CPF': '10987154321'},
        {'CodProp': 5, 'NomeProp': 'Raimundo Rodrigues', 'CPF': '17368055896'},
        {'CodProp': 6, 'NomeProp': 'Patinhas McPato', 'CPF': '27334945857'},
        {'CodProp': 7, 'NomeProp': 'José Silva', 'CPF': '98765432109'},
        {'CodProp': 8, 'NomeProp': 'Ana Oliveira', 'CPF': '54321098765'},
        {'CodProp': 9, 'NomeProp': 'Carlos Pereira', 'CPF': '10987654321'},
        {'CodProp': 10, 'NomeProp': 'Marina Souza', 'CPF': '87654321098'},
        {'CodProp': 11, 'NomeProp': 'Fernando Lima', 'CPF': '43210987654'},
        {'CodProp': 12, 'NomeProp': 'Camila Santos', 'CPF': '21098765432'}
    ],
    'Diario': [
        {'CodDiario': 1, 'Endereco': 'Rua Alexandre de Matos', 'Fotos': None, 'Obs_Geral': 'Construção em Andamento', 'Obs_Func': 'Eletricista terminou a fiação', 'Data': datetime(2026, 10, 12, 19, 0, 0), 'Clima': 'Parcialmente Nublado'},
        {'CodDiario': 2, 'Endereco': 'Rua Mitocôndria Azul', 'Fotos': None, 'Obs_Geral': 'Acidente com o Engenheiro', 'Obs_Func': 'Engenheiro conferiu se vai ser necessário levantar a viga do salão, um pedaço de madeira caiu em cima dele.', 'Data': datetime(2027, 1, 19, 17, 0, 0), 'Clima': 'Ensolarado'},
        {'CodDiario': 3, 'Endereco': 'Avenida Trobson Azambuja', 'Fotos': None, 'Obs_Geral': 'Caminhões do concreto chegaram atrasados.', 'Obs_Func': 'Arquiteto conferiu a planta da obra.', 'Data': datetime(2024, 3, 6, 16, 30, 0), 'Clima': 'Chuva Fraca'},
        {'CodDiario': 4, 'Endereco': 'Avenida Relâmpago Marquinhos', 'Fotos': None, 'Obs_Geral': 'Problema de filtração no banheiro', 'Obs_Func': 'Pedreiro começou a tirar o rejunte antigo.', 'Data': datetime(2023, 11, 17, 17, 0, 0), 'Clima': 'Nublado'},
        {'CodDiario': 5, 'Endereco': 'Avenida Relâmpago Marquinhos', 'Fotos': None, 'Obs_Geral': 'Obra em andamento', 'Obs_Func': 'Arquiteto conferiu a mudança do salão principal.', 'Data': datetime(2024, 5, 19, 18, 0, 0), 'Clima': 'Nublado'},
        {'CodDiario': 6, 'Endereco': 'Avenida F, 213', 'Fotos': None, 'Obs_Geral': 'Obra quase finalizada', 'Obs_Func': 'Engenheiro conferiu a o descarte perigosos.', 'Data': datetime(2026, 1, 25, 17, 30, 0), 'Clima': 'Chuvoso'},
        {'CodDiario': 7, 'Endereco': 'Rua Mitocôndria Azul', 'Fotos': 'caminho_foto_diario1.jpg', 'Obs_Geral': 'N/A', 'Obs_Func': 'Equipe produtiva, bom progresso hoje.', 'Data': datetime(2023, 1, 10, 17, 0, 0), 'Clima': 'Ensolarado'},
        {'CodDiario': 8, 'Endereco': 'Avenida B, 456', 'Fotos': 'caminho_foto_diario2.jpg', 'Obs_Geral': 'Atenção: Vazamento detectado na tubulação principal.', 'Obs_Func': 'Equipe de encanadores acionada.', 'Data': datetime(2023, 2, 15, 18, 0, 0), 'Clima': 'Chuvoso'},
        {'CodDiario': 9, 'Endereco': 'Rua Pennywise', 'Fotos': 'caminho_foto_diario3.jpg', 'Obs_Geral': 'N/A', 'Obs_Func': 'Dia tranquilo, sem incidentes.', 'Data': datetime(2023, 3, 20, 17, 30, 0), 'Clima': 'Nublado'},
        {'CodDiario': 10, 'Endereco': 'Avenida D, 101', 'Fotos': 'caminho_foto_diario4.jpg', 'Obs_Geral': 'Atenção: Atraso na entrega de materiais.', 'Obs_Func': 'Equipe de logística notificada.', 'Data': datetime(2023, 4, 25, 18, 0, 0), 'Clima': 'Ensolarado'},
        {'CodDiario': 11, 'Endereco': 'Rua E, 112', 'Fotos': 'caminho_foto_diario5.jpg', 'Obs_Geral': 'N/A', 'Obs_Func': 'Conclusão da estrutura principal.', 'Data': datetime(2023, 5, 30, 16, 30, 0), 'Clima': 'Parcialmente nublado'},
        {'CodDiario': 12, 'Endereco': 'Avenida F, 213', 'Fotos': 'caminho_foto_diario6.jpg', 'Obs_Geral': 'Atenção: Equipamento danificado.', 'Obs_Func': 'Equipe de manutenção trabalhando no reparo.', 'Data': datetime(2023, 6, 5, 17, 0, 0), 'Clima': 'Chuvoso'}
    ],
    'Equipamentos': [
        {'CodEquipamento': 1, 'Tipo': 'EPI', 'Marca': 'MSA'},
        {'CodEquipamento': 2, 'Tipo': 'EPI', 'Marca': 'Marluvas'},
        {'CodEquipamento': 3, 'Tipo': 'EPI', 'Marca': '3M'},
        {'CodEquipamento': 4, 'Tipo': 'Retroescavadeira', 'Marca': 'Armac'},
        {'CodEquipamento': 5, 'Tipo': 'Betoneira', 'Marca': 'Armac'},
        {'CodEquipamento': 6, 'Tipo': 'Trator', 'Marca': 'John Deere'},
        {'CodEquipamento': 7, 'Tipo': 'Escavadeira', 'Marca': 'Caterpillar'},
        {'CodEquipamento': 8, 'Tipo': 'Betoneira', 'Marca': 'Bosch'},
        {'CodEquipamento': 9, 'Tipo': 'Guincho', 'Marca': 'Hercules'},
        {'CodEquipamento': 10, 'Tipo': 'Serra Elétrica', 'Marca': 'DeWalt'},
        {'CodEquipamento': 11, 'Tipo': 'Martelo Pneumático', 'Marca': 'Makita'},
        {'CodEquipamento': 12, 'Tipo': 'Empilhadeira', 'Marca': 'Toyota'}
    ],
    'Materiais': [
        {'CodMaterial': 1, 'Tipo': 'Lixas', 'Quantidade': 500, 'Unidade': 'm', 'Custo': 1800.00},
        {'CodMaterial': 2, 'Tipo': 'Tijolos', 'Quantidade': 3000, 'Unidade': 'unid', 'Custo': 1000.00},
        {'CodMaterial': 3, 'Tipo': 'Brita', 'Quantidade': 1500, 'Unidade': 'm3', 'Custo': 1525.00},
        {'CodMaterial': 4, 'Tipo': 'Tubos', 'Quantidade': 200, 'Unidade': 'm', 'Custo': 450.00},
        {'CodMaterial': 5, 'Tipo': 'Concreto', 'Quantidade': 1300, 'Unidade': 'm3', 'Custo': 1900.00},
        {'CodMaterial': 6, 'Tipo': 'Espuma isolante', 'Quantidade': 50, 'Unidade': 'unid', 'Custo': 1500.00},
        {'CodMaterial': 7, 'Tipo': 'Cimento', 'Quantidade': 1000, 'Unidade': 'sc50', 'Custo': 800.00},
        {'CodMaterial': 8, 'Tipo': 'Vergalhao de Aço', 'Quantidade': 3000, 'Unidade': 'm', 'Custo': 2500.00},
        {'CodMaterial': 9, 'Tipo': 'Massa Corrida', 'Quantidade': 9, 'Unidade': 'kg', 'Custo': 350.00},
        {'CodMaterial': 10, 'Tipo': 'Tintas', 'Quantidade': 50, 'Unidade': 'unid', 'Custo': 200.00},
        {'CodMaterial': 11, 'Tipo': 'Telhas', 'Quantidade': 100, 'Unidade': 'm3', 'Custo': 300.00},
        {'CodMaterial': 12, 'Tipo': 'Vidros', 'Quantidade': 30, 'Unidade': 'm', 'Custo': 400.00}
    ],
    'Plano_de_Aproveitamento': [
        {'CodPlano': 1, 'Descricao': 'Plano A: resíduo C - reciclados e/ou recuperação', 'Emp_Empresa': 1},
        {'CodPlano': 2, 'Descricao': 'Plano B: resíduo A - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 2},
        {'CodPlano': 3, 'Descricao': 'Plano C: resíduo A - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 3},
        {'CodPlano': 4, 'Descricao': 'Plano D: resíduo B - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 4},
        {'CodPlano': 5, 'Descricao': 'Plano E: resíduo A - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 5},
        {'CodPlano': 6, 'Descricao': 'Plano F: resíduos F - manuseio e tratamento especial', 'Emp_Empresa': 6},
        {'CodPlano': 7, 'Descricao': 'Plano G: resíduo A - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 7},
        {'CodPlano': 8, 'Descricao': 'Plano H: resíduo B - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 8},
        {'CodPlano': 9, 'Descricao': 'Plano I: resíduo C - reciclados e/ou recuperação', 'Emp_Empresa': 9},
        {'CodPlano': 10, 'Descricao': 'Plano J: resíduo D - PERIGOSO E POLUENTE! Manuseio e tratamento especial', 'Emp_Empresa': 10},
        {'CodPlano': 11, 'Descricao': 'Plano K: resíduo A - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 11},
        {'CodPlano': 12, 'Descricao': 'Plano L: resíduo B - reciclagem e/ou reaproveitamento', 'Emp_Empresa': 12}
    ],
    'Residuos': [
        {'Classe': 'Classe C', 'PA_CodPlano': 1},
        {'Classe': 'Classe A', 'PA_CodPlano': 2},
        {'Classe': 'Classe A', 'PA_CodPlano': 3},
        {'Classe': 'Classe B', 'PA_CodPlano': 4},
        {'Classe': 'Classe A', 'PA_CodPlano': 5},
        {'Classe': 'Classe F', 'PA_CodPlano': 6},
        {'Classe': 'Classe A', 'PA_CodPlano': 7},
        {'Classe': 'Classe B', 'PA_CodPlano': 8},
        {'Classe': 'Classe C', 'PA_CodPlano': 9},
        {'Classe': 'Classe D', 'PA_CodPlano': 10},
        {'Classe': 'Classe A', 'PA_CodPlano': 11},
        {'Classe': 'Classe B', 'PA_CodPlano': 12}
    ],
    'Cadastro': [
        {'Cad_CodEmpresa': 1, 'Cad_CodObra': 8, 'Cad_CodFuncionario': 9},
        {'Cad_CodEmpresa': 2, 'Cad_CodObra': 7, 'Cad_CodFuncionario': 8},
        {'Cad_CodEmpresa': 3, 'Cad_CodObra': 10, 'Cad_CodFuncionario': 7},
        {'Cad_CodEmpresa': 4, 'Cad_CodObra': 11, 'Cad_CodFuncionario': 6},
        {'Cad_CodEmpresa': 5, 'Cad_CodObra': 12, 'Cad_CodFuncionario': 5},
        {'Cad_CodEmpresa': 6, 'Cad_CodObra': 1, 'Cad_CodFuncionario': 4},
        {'Cad_CodEmpresa': 7, 'Cad_CodObra': 11, 'Cad_CodFuncionario': 3},
        {'Cad_CodEmpresa': 8, 'Cad_CodObra': 8, 'Cad_CodFuncionario': 2},
        {'Cad_CodEmpresa': 9, 'Cad_CodObra': 6, 'Cad_CodFuncionario': 1},
        {'Cad_CodEmpresa': 10, 'Cad_CodObra': 5, 'Cad_CodFuncionario': 12},
        {'Cad_CodEmpresa': 11, 'Cad_CodObra': 6, 'Cad_CodFuncionario': 11},
        {'Cad_CodEmpresa': 12, 'Cad_CodObra': 7, 'Cad_CodFuncionario': 10}
    ],
    'Contrato': [
        {'Cont_CodEmpresa': 1, 'Cont_CodObra': 8, 'Cont_CodProp': 9},
        {'Cont_CodEmpresa': 2, 'Cont_CodObra': 7, 'Cont_CodProp': 8},
        {'Cont_CodEmpresa': 3, 'Cont_CodObra': 10, 'Cont_CodProp': 7},
        {'Cont_CodEmpresa': 4, 'Cont_CodObra': 11, 'Cont_CodProp': 6},
        {'Cont_CodEmpresa': 5, 'Cont_CodObra': 12, 'Cont_CodProp': 5},
        {'Cont_CodEmpresa': 6, 'Cont_CodObra': 1, 'Cont_CodProp': 4},
        {'Cont_CodEmpresa': 7, 'Cont_CodObra': 11, 'Cont_CodProp': 3},
        {'Cont_CodEmpresa': 8, 'Cont_CodObra': 8, 'Cont_CodProp': 2},
        {'Cont_CodEmpresa': 9, 'Cont_CodObra': 6, 'Cont_CodProp': 1},
        {'Cont_CodEmpresa': 10, 'Cont_CodObra': 5, 'Cont_CodProp': 12},
        {'Cont_CodEmpresa': 11, 'Cont_CodObra': 6, 'Cont_CodProp': 11},
        {'Cont_CodEmpresa': 12, 'Cont_CodObra': 7, 'Cont_CodProp': 10}
    ],
    'Trabalho': [
        {'Trab_CodObra': 1, 'Trab_CodFuncionario': 1, 'Trab_CodDiario': 3},
        {'Trab_CodObra': 6, 'Trab_CodFuncionario': 2, 'Trab_CodDiario': 2},
        {'Trab_CodObra': 2, 'Trab_CodFuncionario': 3, 'Trab_CodDiario': 4},
        {'Trab_CodObra': 4, 'Trab_CodFuncionario': 4, 'Trab_CodDiario': 1},
        {'Trab_CodObra': 5, 'Trab_CodFuncionario': 5, 'Trab_CodDiario': 9},
        {'Trab_CodObra': 6, 'Trab_CodFuncionario': 6, 'Trab_CodDiario': 7},
        {'Trab_CodObra': 2, 'Trab_CodFuncionario': 7, 'Trab_CodDiario': 1},
        {'Trab_CodObra': 8, 'Trab_CodFuncionario': 8, 'Trab_CodDiario': 8},
        {'Trab_CodObra': 12, 'Trab_CodFuncionario': 9, 'Trab_CodDiario': 6},
        {'Trab_CodObra': 10, 'Trab_CodFuncionario': 10, 'Trab_CodDiario': 10},
        {'Trab_CodObra': 11, 'Trab_CodFuncionario': 11, 'Trab_CodDiario': 11},
        {'Trab_CodObra': 12, 'Trab_CodFuncionario': 12, 'Trab_CodDiario': 12}
    ],
    'Aluguel': [
        {'Alug_CodEquipamento': 1, 'Alug_CodDiario': 1, 'Valor': 215.00, 'Periodo': 30},
        {'Alug_CodEquipamento': 2, 'Alug_CodDiario': 1, 'Valor': 140.00, 'Periodo': 20},
        {'Alug_CodEquipamento': 3, 'Alug_CodDiario': 7, 'Valor': 175.00, 'Periodo': 15},
        {'Alug_CodEquipamento': 4, 'Alug_CodDiario': 7, 'Valor': 1850.00, 'Periodo': 10},
        {'Alug_CodEquipamento': 5, 'Alug_CodDiario': 6, 'Valor': 1525.00, 'Periodo': 25},
        {'Alug_CodEquipamento': 6, 'Alug_CodDiario': 11, 'Valor': 1900.00, 'Periodo': 12},
        {'Alug_CodEquipamento': 7, 'Alug_CodDiario': 11, 'Valor': 2150.00, 'Periodo': 18},
        {'Alug_CodEquipamento': 8, 'Alug_CodDiario': 8, 'Valor': 200.00, 'Periodo': 30},
        {'Alug_CodEquipamento': 9, 'Alug_CodDiario': 8, 'Valor': 150.00, 'Periodo': 20},
        {'Alug_CodEquipamento': 10, 'Alug_CodDiario': 8, 'Valor': 570.00, 'Periodo': 15},
        {'Alug_CodEquipamento': 11, 'Alug_CodDiario': 10, 'Valor': 120.00, 'Periodo': 10},
        {'Alug_CodEquipamento': 12, 'Alug_CodDiario': 11, 'Valor': 1675.00, 'Periodo': 25}
    ],
    'Consumo': [
        {'Consume_CodFuncionario': 1, 'Consume_CodMaterial': 12},
        {'Consume_CodFuncionario': 2, 'Consume_CodMaterial': 11},
        {'Consume_CodFuncionario': 3, 'Consume_CodMaterial': 10},
        {'Consume_CodFuncionario': 4, 'Consume_CodMaterial': 9},
        {'Consume_CodFuncionario': 5, 'Consume_CodMaterial': 8},
        {'Consume_CodFuncionario': 6, 'Consume_CodMaterial': 7},
        {'Consume_CodFuncionario': 7, 'Consume_CodMaterial': 6},
        {'Consume_CodFuncionario': 8, 'Consume_CodMaterial': 5},
        {'Consume_CodFuncionario': 9, 'Consume_CodMaterial': 4},
        {'Consume_CodFuncionario': 10, 'Consume_CodMaterial': 3},
        {'Consume_CodFuncionario': 11, 'Consume_CodMaterial': 2},
        {'Consume_CodFuncionario': 12, 'Consume_CodMaterial': 1}
    ],
    'Recebimento': [
        {'Receb_CodDiario': 1, 'Receb_CodMaterial': 1},
        {'Receb_CodDiario': 2, 'Receb_CodMaterial': 2},
        {'Receb_CodDiario': 3, 'Receb_CodMaterial': 3},
        {'Receb_CodDiario': 4, 'Receb_CodMaterial': 4},
        {'Receb_CodDiario': 5, 'Receb_CodMaterial': 5},
        {'Receb_CodDiario': 6, 'Receb_CodMaterial': 6},
        {'Receb_CodDiario': 7, 'Receb_CodMaterial': 7},
        {'Receb_CodDiario': 8, 'Receb_CodMaterial': 8},
        {'Receb_CodDiario': 9, 'Receb_CodMaterial': 9},
        {'Receb_CodDiario': 10, 'Receb_CodMaterial': 10},
        {'Receb_CodDiario': 11, 'Receb_CodMaterial': 11},
        {'Receb_CodDiario': 12, 'Receb_CodMaterial': 12}
    ],
    'Uso': [
        {'Uso_CodMaterial': 1, 'Uso_Classe': 'Classe C', 'Inicial': 'Lixamento e acabamento - Geral', 'Subsequente': 'Material de base'},
        {'Uso_CodMaterial': 2, 'Uso_Classe': 'Classe A', 'Inicial': 'Alvenaria - Geral', 'Subsequente': 'Tijolos'},
        {'Uso_CodMaterial': 3, 'Uso_Classe': 'Classe A', 'Inicial': 'Pavimentação - Geral', 'Subsequente': 'Material de base'},
        {'Uso_CodMaterial': 4, 'Uso_Classe': 'Classe B', 'Inicial': 'Sistema hidráulico', 'Subsequente': 'Material de base'},
        {'Uso_CodMaterial': 5, 'Uso_Classe': 'Classe A', 'Inicial': 'Revestimento - Banheiro', 'Subsequente': 'Não reaproveital'},
        {'Uso_CodMaterial': 6, 'Uso_Classe': 'Classe F', 'Inicial': 'Isolação térmica - Quarto', 'Subsequente': None},
        {'Uso_CodMaterial': 7, 'Uso_Classe': 'Classe A', 'Inicial': 'Produção concreto - Geral', 'Subsequente': 'Material de base'},
        {'Uso_CodMaterial': 8, 'Uso_Classe': 'Classe B', 'Inicial': 'Reforço em estrutura - Geral', 'Subsequente': 'Aço reciclado'},
        {'Uso_CodMaterial': 9, 'Uso_Classe': 'Classe C', 'Inicial': 'Preparação de superfície - Geral', 'Subsequente': 'Massa corrida'},
        {'Uso_CodMaterial': 10, 'Uso_Classe': 'Classe D', 'Inicial': 'Pintura - Segundo andar', 'Subsequente': None},
        {'Uso_CodMaterial': 11, 'Uso_Classe': 'Classe A', 'Inicial': 'Cobertura - Teto', 'Subsequente': 'Material de base'},
        {'Uso_CodMaterial': 12, 'Uso_Classe': 'Classe B', 'Inicial': 'Cobertura - Janelas', 'Subsequente': 'Material de base'}
    ]
}

# Firestore Upload Function
def upload_data_to_firestore(data_dict, db_client):
    """Upload data to Firestore collections."""
    for collection_name, documents in data_dict.items():
        print(f"\nSubindo dados para a coleção: {collection_name}...")
        for doc in documents:
            try:
                doc_id = None
                if collection_name == 'Empresa':
                    doc_id = str(doc['CodEmpresa'])
                elif collection_name == 'Mao_de_Obra':
                    doc_id = str(doc['CodFuncionario'])
                elif collection_name == 'Obra':
                    doc_id = str(doc['CodObra'])
                elif collection_name == 'Proprietario':
                    doc_id = str(doc['CodProp'])
                elif collection_name == 'Diario':
                    doc_id = str(doc['CodDiario'])
                elif collection_name == 'Equipamentos':
                    doc_id = str(doc['CodEquipamento'])
                elif collection_name == 'Materiais':
                    doc_id = str(doc['CodMaterial'])
                elif collection_name == 'Plano_de_Aproveitamento':
                    doc_id = str(doc['CodPlano'])
                elif collection_name == 'Residuos':
                    # Chave composta (Classe, PA_CodPlano) - concatena para formar o ID
                    doc_id = f"{doc['Classe']}_{doc['PA_CodPlano']}"
                elif collection_name == 'Cadastro':
                    doc_id = f"{doc['Cad_CodEmpresa']}_{doc['Cad_CodObra']}_{doc['Cad_CodFuncionario']}"
                elif collection_name == 'Contrato':
                    doc_id = f"{doc['Cont_CodEmpresa']}_{doc['Cont_CodObra']}_{doc['Cont_CodProp']}"
                elif collection_name == 'Trabalho':
                    doc_id = f"{doc['Trab_CodObra']}_{doc['Trab_CodFuncionario']}_{doc['Trab_CodDiario']}"
                elif collection_name == 'Aluguel':
                    doc_id = f"{doc['Alug_CodEquipamento']}_{doc['Alug_CodDiario']}"
                elif collection_name == 'Consumo':
                    doc_id = f"{doc['Consume_CodFuncionario']}_{doc['Consume_CodMaterial']}"
                elif collection_name == 'Recebimento':
                    doc_id = f"{doc['Receb_CodDiario']}_{doc['Receb_CodMaterial']}"
                elif collection_name == 'Uso':
                    doc_id = f"{doc['Uso_CodMaterial']}_{doc['Uso_Classe']}"


                if doc_id:
                    db_client.collection(collection_name).document(doc_id).set(doc)
                    # print(f"  Documento '{doc_id}' adicionado à coleção '{collection_name}'.")
                else:
                    # Se não houver um ID explícito, deixe o Firestore gerar um
                    db_client.collection(collection_name).add(doc)
                    # print(f"  Documento (ID automático) adicionado à coleção '{collection_name}'.")

            except Exception as e:
                print(f"Erro ao adicionar documento à coleção '{collection_name}': {doc} - Erro: {e}")

# Example Queries and Test Code
def example_queries(db):
    """Run example Firestore queries."""
    from google.cloud.firestore_v1 import FieldFilter
    # Empresa CNPJ LIKE '123%'
    docs = db.collection("Empresa") \
        .where(filter=FieldFilter("CNPJ", ">=", "123")) \
        .where(filter=FieldFilter("CNPJ", "<", "124")) \
        .stream()
    for doc in docs:
        print(doc.to_dict())
    # Aluguel Valor BETWEEN 500 AND 2000
    docs = db.collection("Aluguel") \
        .where(filter=FieldFilter("Valor", ">=", 500)) \
        .where(filter=FieldFilter("Valor", "<=", 2000)) \
        .stream()
    for doc in docs:
        print(doc.to_dict())
    # Mao_de_Obra Salario > 5000 ORDER BY Nome ASC
    docs = db.collection("Mao_de_Obra") \
        .where(filter=FieldFilter("Salario", ">", 5000)) \
        .order_by("Nome") \
        .stream()
    for doc in docs:
        print(doc.to_dict())
    # Aluguel Alug_CodEquipamento = 10 LIMIT 5
    docs = db.collection("Aluguel") \
        .where(filter=FieldFilter("Alug_CodEquipamento", "==", 10)) \
        .limit(5) \
        .stream()
    for doc in docs:
        print(doc.to_dict())
    # Obra Data_previsao > '2025-01-01'
    docs = db.collection("Obra") \
        .where(filter=FieldFilter("Data_previsao", ">", datetime(2025, 1, 1))) \
        .stream()
    for doc in docs:
        print(doc.to_dict().get("Endereco"))
    # Materiais GROUP BY Unidade
    docs = db.collection("Materiais").stream()
    unidades = [doc.to_dict()['Unidade'] for doc in docs]
    contagem = Counter(unidades)
    for unidade, total in contagem.items():
        print(unidade, total)
    # Cadastro WHERE Cad_CodEmpresa = 3 AND Cad_CodObra = 10
    docs = db.collection("Cadastro") \
        .where(filter=FieldFilter("Cad_CodEmpresa", "==", 3)) \
        .where(filter=FieldFilter("Cad_CodObra", "==", 10)) \
        .stream()
    for doc in docs:
        print(doc.to_dict())
    # Empresa - List all
    collection_ref = db.collection('Empresa')
    docs = collection_ref.get()
    print("Diary Entries:")
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")

# Main Execution Block
def main():
    db = init_firestore()
    if db:
        upload_data_to_firestore(original_data, db)
        print("\nProcesso de migração concluído!")
        example_queries(db)
    else:
        print("\nNão foi possível prosseguir com o upload. Verifique a configuração do Firebase.")

if __name__ == "__main__":
    main()

# Note: SQLite example code removed for clarity. Move to a separate file if needed.