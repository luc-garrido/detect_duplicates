# 📁 Detector de Arquivos Repetidos (.pdf e .docx)

Este é um script em Python para detectar e, opcionalmente, apagar arquivos PDF e DOCX duplicados em um diretório. Ele compara os arquivos com base no conteúdo (não apenas no nome) e pergunta ao usuário se deseja excluir as cópias encontradas.

## ✅ Funcionalidades

- Suporte a arquivos `.pdf` e `.docx`
- Verificação baseada no conteúdo dos arquivos (hashing)
- Interface interativa no terminal para decidir se apaga os duplicados
- Rápido e fácil de usar

## 📦 Requisitos

- Python 3.7+
- Bibliotecas:
  - `hashlib`
  - `os`
  - `docx`
  - `PyPDF2` (ou outra usada por você)

Instale as dependências com:

```bash
pip install python-docx PyPDF2
