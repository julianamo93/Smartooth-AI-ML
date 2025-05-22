# 🦷 Smartooth AI – Cuidando do seu sorriso com inteligência artificial

Smartooth AI é um sistema inteligente voltado para clínicas odontológicas que utiliza **machine learning** para fornecer recomendações personalizadas de cuidados com a saúde bucal. O projeto também conta com um sistema de gerenciamento de pacientes, utilizando **Flask**, **Pandas**, e **MongoDB** para armazenar, analisar e prever riscos com base nos hábitos dos usuários.

---

## 🪐 Developers 

- [Juliana Moreira](https://github.com/julianamo93) - Modelagem de Dados e Cloud - RM554113 - 2TDSPR
- [Kevin Nobre](https://github.com/KevinNobre) - Backend e Front - RM552590 - 2TDSZ
- [Sabrina Couto](https://github.com/sabrinacouto) - Backend Developer - RM552728 - 2TDSZ

## 📌 Objetivos

- Promover a saúde bucal com o auxílio de IA.
- Auxiliar clínicas odontológicas na análise dos hábitos de seus pacientes.
- Detectar riscos potenciais com base em dados clínicos e comportamentais.
- Automatizar o cadastro e gerenciamento de pacientes.
- Oferecer uma interface de API RESTful para consumo de serviços.

---

## 🚀 Funcionalidades

### ✅ CRUD de Pacientes
- **POST /patients**: Adiciona um novo paciente ao sistema.
- **GET /patients**: Lista todos os pacientes cadastrados.
- **GET /patients/&lt;id&gt;**: Retorna os dados de um paciente específico.
- **PUT /patients/&lt;id&gt;**: Atualiza os dados de um paciente.
- **DELETE /patients/&lt;id&gt;**: Remove um paciente do sistema.

### 🧠 Predição de Risco Bucal com IA
- **POST /predict**: Recebe dados clínicos (`age`, `history`, `severity`) e retorna uma predição de risco gerada pelo modelo de Machine Learning.

---

## 📊 Exemplo de Payloads

### 🔹 POST /patients
```json
{
  "id": 1,
  "name": "João Silva",
  "age": 34,
  "last_visit": "2024-10-10",
  "habits": "escova_2x_dia"
}
```

## 💬 Rodando a Solução

### Clone o repositório
```
git clone https://github.com/seu-usuario/Smartooth-AI-ML.git
cd Smartooth-AI-ML
```
- (Opcional) Crie e ative um ambiente virtual
```
python -m venv venv
```
- No Windows
```
venv\Scripts\activate
```
- No Linux/Mac
```
source venv/bin/activate
```
- Instale as dependências
```
pip install -r requirements.txt
```
### Execute a aplicação Flask
```
python run.py
```
---




