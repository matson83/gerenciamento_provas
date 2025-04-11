# Projeto de Autenticação com Django Ninja

Este projeto é uma API de gerenciamento de provas com autenticação desenvolvida com Django e Django Ninja.

---

##  Tecnologias utilizadas

- Python 3.11+
- Django 4.x
- Django Ninja
- SQLite
- Pydantic

---

##  Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/matson83/gerenciamento_provas.git
cd gerenciamento_provas
```

### 2. Criar um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Aplicar a migração
```bash
python manage.py migrate
```

### 4. Executar o servidor
```bash
python manage.py runserver
````

### A API estará disponível em http://127.0.0.1:8000/api/docs

---

## Endpoints para testar no Postman :

### POST http://127.0.0.1:8000/api/auth/registro :
#### Entrada para registrar participante: 
```json
{
  "username": "participante_teste",
  "password": "123",
  "email": "participante_teste@example.com",
  "role": "PARTICIPANTE"
}
```
#### Exemplo de Saída :
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDQ3ODE4MCwiaWF0IjoxNzQ0MzkxNzgwLCJqdGkiOiI0NjFiN2JmNmU0MjU0ZWYwOTQ0MjdjMWFkYWNhNjYyMyIsInVzZXJfaWQiOjExfQ.XHeR0j1fy_UCbks1utKjn2Hjj8Pnhd4JmFqOcf7Mr70",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MzkyMDgwLCJpYXQiOjE3NDQzOTE3ODAsImp0aSI6ImQ0MTEyNTRlZjE1MzQwNTJiNWM1OWVkNjRmNjczYjMyIiwidXNlcl9pZCI6MTF9.fqg1-JopKiIFPRmTcL9WU62hKRaHJEFWqJI8Z_uERz0",
    "user": {
        "username": "participante_teste",
        "role": "PARTICIPANTE"
    }
}
```
#### Entrada para registrar admin: 
```json
{
  "username": "admin_teste",
  "password": "123",
  "email": "admin_teste@example.com",
  "role": "ADMIN"
}
```
#### Exemplo de Saída :
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDQ3OTcyOCwiaWF0IjoxNzQ0MzkzMzI4LCJqdGkiOiJhN2JhMWJkYmEwNmY0YjkyYjZmMDBiZjg3NDM1ZWVhZiIsInVzZXJfaWQiOjEyfQ.sJ9ugYQPTTYNYdb4FsGQWqDK6JDXtOma9Q9KeEoVyLk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MzkzNjI4LCJpYXQiOjE3NDQzOTMzMjgsImp0aSI6IjQyY2Y2ZjAxOWE5ODRhODE5OTk2ZDJmNzQwOWUxZmQ1IiwidXNlcl9pZCI6MTJ9.eb5WHXdcgUs71HrK-b8OUOuU9yM4LCBiERtkmC2daic",
    "user": {
        "username": "admin_teste",
        "role": "ADMIN"
    }
}
```
---
### POST http://127.0.0.1:8000/api/auth/login :
#### Usando o token access gerado ao registrar no Bearer Token

#### Entrada para login como participante :
```json
  {
  "username": "participante_teste",
  "password": "123"
}
```
#### Exemplo de Saída :
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDQ4MDEzNywiaWF0IjoxNzQ0MzkzNzM3LCJqdGkiOiI1MTNjNDVkYjA0M2E0ZmMwYjZhY2FhZjllMDY2NjQ1MCIsInVzZXJfaWQiOjExfQ.fXbVLSBRmNUpSg8El4Z06Lv5_yMGE40TLjde_GE6_bE",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0Mzk0MDM3LCJpYXQiOjE3NDQzOTM3MzcsImp0aSI6IjI0YTc0ZTczODU5MzQ0MDJhMWE1NjIzYmM2ODQwZjViIiwidXNlcl9pZCI6MTF9.QESwFLMZTKH8jmK2J45yQCuwmH2tX0LmmwCi0oxfCjw",
    "user": {
        "username": "participante_teste",
        "role": "PARTICIPANTE"
    }
}
```
#### Entrada para login como admin :
```json
  {
  "username": "admin_teste",
  "password": "123"
}
```
#### Exemplo de Saída :
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDQ3OTcyOCwiaWF0IjoxNzQ0MzkzMzI4LCJqdGkiOiJhN2JhMWJkYmEwNmY0YjkyYjZmMDBiZjg3NDM1ZWVhZiIsInVzZXJfaWQiOjEyfQ.sJ9ugYQPTTYNYdb4FsGQWqDK6JDXtOma9Q9KeEoVyLk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MzkzNjI4LCJpYXQiOjE3NDQzOTMzMjgsImp0aSI6IjQyY2Y2ZjAxOWE5ODRhODE5OTk2ZDJmNzQwOWUxZmQ1IiwidXNlcl9pZCI6MTJ9.eb5WHXdcgUs71HrK-b8OUOuU9yM4LCBiERtkmC2daic",
    "user": {
        "username": "admin_teste",
        "role": "ADMIN"
    }
}
```
---
### GET http://127.0.0.1:8000/api/admin/provas :
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Saída :
```json
[
    {
        "id": 1,
        "username": "matson",
        "provas": []
    },
    {
        "id": 4,
        "username": "teste",
        "provas": [
            {
                "id": 2,
                "titulo": "Prova de Matemática - Atualizada"
            }
        ]
    },
    {
        "id": 6,
        "username": "aluno1",
        "provas": []
    },
    {
        "id": 7,
        "username": "participante123",
        "provas": []
    },
    {
        "id": 10,
        "username": "joaodasilva",
        "provas": [
            {
                "id": 2,
                "titulo": "Prova de Matemática - Atualizada"
            }
        ]
    },
    {
        "id": 11,
        "username": "participante_teste",
        "provas": []
    }
]
```
---
### POST http://127.0.0.1:8000/api/admin/provas/criar :
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de entrada :
```json
{
  "titulo": "Prova de Algebra molecular",
  "descricao": "Avaliação sobre álgebra e geometria.",
  "questoes": [
    {
      "enunciado": "Qual é o valor de 2 + 2?",
      "alternativas": [
        { "texto": "3", "correta": false },
        { "texto": "4", "correta": true },
        { "texto": "5", "correta": false }
      ]
    },
    {
      "enunciado": "Qual a fórmula da área do círculo?",
      "alternativas": [
        { "texto": "π * r²", "correta": true },
        { "texto": "2 * π * r", "correta": false }
      ]
    }
  ]
}
```
#### Exemplo de Saída :
```json
{
    "message": "Prova criada com sucesso",
    "prova_id": 3
}
```
---
### GET http://127.0.0.1:8000/api/admin/provas/detalhes/{prova_id} :
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Saída :
```json
{
    "id": 3,
    "titulo": "Prova de Algebra molecular",
    "descricao": "Avaliação sobre álgebra e geometria.",
    "questoes": [
        {
            "id": 5,
            "enunciado": "Qual é o valor de 2 + 2?",
            "alternativas": [
                {
                    "id": 13,
                    "texto": "3",
                    "correta": false
                },
                {
                    "id": 14,
                    "texto": "4",
                    "correta": true
                },
                {
                    "id": 15,
                    "texto": "5",
                    "correta": false
                }
            ]
        },
        {
            "id": 6,
            "enunciado": "Qual a fórmula da área do círculo?",
            "alternativas": [
                {
                    "id": 16,
                    "texto": "π * r²",
                    "correta": true
                },
                {
                    "id": 17,
                    "texto": "2 * π * r",
                    "correta": false
                }
            ]
        }
    ]
}
```
---
### POST http://127.0.0.1:8000/api/admin/provas/atribuir
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "prova_id": 3,
  "participantes_ids": [10]
}

```
#### Exemplo de Saída :
```json
{
    "message": "Prova atribuída com sucesso",
    "atribuidos": [
        {
            "participante_id": 10,
            "status": "criado"
        }
    ]
}
```
---
### PUT http://127.0.0.1:8000/api/admin/provas/{prova_id}
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "titulo": "Prova de Algebra molecular - Atualizada",
  "descricao": "Conteúdo atualizado com novas questões.",
  "questoes": [
    {
      "enunciado": "Qual é o valor de 2 + 2?",
      "alternativas": [
        { "texto": "3", "correta": false },
        { "texto": "4", "correta": true },
        { "texto": "5", "correta": false }
      ]
    }
  ]
}
```
#### Exemplo de Saída 
```json
{
    "message": "Prova atualizada com sucesso"
}
```
---
### PUT http://127.0.0.1:8000/api/admin/provas/{prova_id}/questoes/{questao_id}
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "enunciado": "Qual o resultado de 2 + 4?",
  "alternativas": [
    {
      "texto": "6",
      "correta": true
    },
    {
      "texto": "7",
      "correta": false
    }
  ]
}

```
#### Exemplo de Saída :
```json
{
    "message": "Questão atualizada com sucesso"
}
```
---
### PUT http://127.0.0.1:8000/api/admin/provas/{prova_id}/questoes/{questao_id}/alternativas/{alternativa_id}
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "texto": "Nenhuma",
  "correta": false
}
```
#### Exemplo de Saída :
```json
{
    "message": "Alternativa atualizada com sucesso.",
    "alternativa_id": 22
}
```
---
### GEt http://127.0.0.1:8000/api/participante/dashboard
#### Usando o token access do participante gerado ao logar no Bearer Token

#### Exemplo de Saída :
```json
{
    "message": "Olá participante_teste",
    "provas_atribuidas": [
        {
            "id": 3,
            "titulo": "Prova de Algebra molecular - Atualizada",
            "descricao": "Conteúdo atualizado com novas questões.",
            "respondida": false,
            "score": null,
            "questoes": [
                {
                    "id": 5,
                    "enunciado": "Qual o resultado de 2 + 4?",
                    "alternativas": [
                        {
                            "id": 13,
                            "texto": "3"
                        },
                        {
                            "id": 14,
                            "texto": "4"
                        },
                        {
                            "id": 15,
                            "texto": "5"
                        },
                        {
                            "id": 21,
                            "texto": "6"
                        },
                        {
                            "id": 22,
                            "texto": "Nenhuma"
                        }
                    ]
                },
                {
                    "id": 6,
                    "enunciado": "Qual a fórmula da área do círculo?",
                    "alternativas": [
                        {
                            "id": 16,
                            "texto": "π * r²"
                        },
                        {
                            "id": 17,
                            "texto": "2 * π * r"
                        }
                    ]
                },
                {
                    "id": 7,
                    "enunciado": "Qual é o valor de 2 + 2?",
                    "alternativas": []
                },
                {
                    "id": 8,
                    "enunciado": "Qual é o valor de 2 + 2?",
                    "alternativas": [
                        {
                            "id": 18,
                            "texto": "3"
                        },
                        {
                            "id": 19,
                            "texto": "4"
                        },
                        {
                            "id": 20,
                            "texto": "5"
                        }
                    ]
                }
            ]
        }
    ]
}
```
---
### POST http://127.0.0.1:8000/api/participante/responder/3 
#### Usando o token access do participante gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "prova_id": 3,
  "respostas": [
    {
      "questao_id": 5,
      "alternativa_id": 21
    }
  ]
}
```
#### Exemplo de Saída :
```json
{
    "message": "Respostas registradas e prova corrigida",
    "acertos": 1,
    "total_questoes": 1,
    "nota_percentual": 100.0
}
```

---
### PUT http://127.0.0.1:8000/api/participante/editar/3
#### Usando o token access do participante gerado ao logar no Bearer Token

#### Exemplo de Entrada :
```json
{
  "prova_id": 3,
  "respostas": [
    {
      "questao_id": 5,
      "alternativa_id": 22
    }
  ]
}
```
#### Exemplo de Saída :
```json
{
    "message": "Respostas editadas com sucesso",
    "acertos": 0,
    "total_questoes": 4,
    "nota_percentual": 0.0
}
```

---
### GET http://127.0.0.1:8000/api/admin/ranking/{prova_id}
#### Usando o token access do admin gerado ao logar no Bearer Token

#### Exemplo de Saída :
```json
{
    "prova_id": 3,
    "ranking": [
        {
            "participante": "participante_teste",
            "acertos": 1,
            "total": 1,
            "nota": 100.0
        },
        {
            "participante": "joaodasilva",
            "acertos": 0,
            "total": 0,
            "nota": 0
        }
    ]
}
```
### Para os DELETE de prova,questão e alternativa :
#### Usando o token access do admin gerado ao logar no Bearer Token

### DELETE http://127.0.0.1:8000/api/admin/provas/{prova_id}
### DELETE http://127.0.0.1:8000/api/admin/provas/{prova_id}/questoes/{questao_id}
### DELETE http://127.0.0.1:8000/api/admin/provas/{prova_id}/questoes/{questao_id}/alternativas/{alternativa_id}



