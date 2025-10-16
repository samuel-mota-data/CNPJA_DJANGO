curl --location 'https://api.cnpja.com/office/37335118000180' \
--header 'Accept: application/json' \
--header 'Authorization: f9574be4-d65a-4290-9d7c-b4e44ada129c-bf9e42d5-c2ff-4ac4-b4df-7fac6fb77ee0'

saida

{
    "updated": "2025-10-15T13:44:10.000Z",
    "taxId": "37335118000180",
    "company": {
        "id": 37335118,
        "name": "CNPJA TECNOLOGIA LTDA",
        "equity": 1000,
        "nature": {
            "id": 2062,
            "text": "Sociedade Empresária Limitada"
        },
        "size": {
            "id": 1,
            "acronym": "ME",
            "text": "Microempresa"
        },
        "members": [
            {
                "since": "2020-06-05",
                "role": {
                    "id": 49,
                    "text": "Sócio-Administrador"
                },
                "person": {
                    "id": "0ee5ad51-e58d-4400-a68a-1ae0aaf394c6",
                    "name": "Etienne Rodrigues Bechara",
                    "type": "NATURAL",
                    "taxId": "***538418**",
                    "age": "31-40"
                }
            },
            {
                "since": "2020-06-05",
                "role": {
                    "id": 22,
                    "text": "Sócio"
                },
                "person": {
                    "id": "84cda86b-7b46-4be3-9b2e-4c374da9879b",
                    "name": "Camila Pedrosa Alves",
                    "type": "NATURAL",
                    "taxId": "***708668**",
                    "age": "31-40"
                }
            }
        ]
    },
    "alias": "Cnpja",
    "founded": "2020-06-05",
    "head": true,
    "statusDate": "2020-06-05",
    "status": {
        "id": 2,
        "text": "Ativa"
    },
    "address": {
        "municipality": 3550308,
        "street": "Avenida Brig Faria Lima",
        "number": "2369",
        "details": "Conj 1102",
        "district": "Jardim Paulistano",
        "city": "São Paulo",
        "state": "SP",
        "zip": "01452922",
        "country": {
            "id": 76,
            "name": "Brasil"
        }
    },
    "phones": [
        {
            "type": "MOBILE",
            "area": "11",
            "number": "71564144"
        }
    ],
    "emails": [
        {
            "ownership": "CORPORATE",
            "address": "fazenda@cnpja.com",
            "domain": "cnpja.com"
        }
    ],
    "mainActivity": {
        "id": 6311900,
        "text": "Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet"
    },
    "sideActivities": [
        {
            "id": 6201501,
            "text": "Desenvolvimento de programas de computador sob encomenda"
        },
        {
            "id": 6201502,
            "text": "Web design"
        },
        {
            "id": 6202300,
            "text": "Desenvolvimento e licenciamento de programas de computador customizáveis"
        },
        {
            "id": 6203100,
            "text": "Desenvolvimento e licenciamento de programas de computador não-customizáveis"
        },
        {
            "id": 6204000,
            "text": "Consultoria em tecnologia da informação"
        },
        {
            "id": 6209100,
            "text": "Suporte técnico, manutenção e outros serviços em tecnologia da informação"
        },
        {
            "id": 6319400,
            "text": "Portais, provedores de conteúdo e outros serviços de informação na internet"
        },
        {
            "id": 6399200,
            "text": "Outras atividades de prestação de serviços de informação não especificadas anteriormente"
        },
        {
            "id": 8599603,
            "text": "Treinamento em informática"
        }
    ]
}