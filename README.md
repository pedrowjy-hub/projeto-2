# Projeto 2 — API de Imóveis

## Deploy

A API está disponível em [http://34.224.222.250:5000/].

## Rotas

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/imoveis` | Lista todos os imóveis cadastrados. |
| `GET` | `/imoveis/<id>` | Retorna os dados de um imóvel pelo seu identificador. |
| `POST` | `/imoveis` | Cadastra um novo imóvel. |
| `PUT` | `/imoveis/<id>` | Atualiza todos os dados de um imóvel existente. |
| `DELETE` | `/imoveis/<id>` | Remove um imóvel pelo seu identificador. |
| `GET` | `/imoveis/tipo/<tipo>` | Lista os imóveis de um tipo específico. |
| `GET` | `/imoveis/cidade/<cidade>` | Lista os imóveis de uma cidade específica. |

