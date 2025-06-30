from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes.routes import main_bp
from instalacao_schema import InstalacaoSchema

app = Flask(__name__)
CORS(app, origins=["null"])


swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "GEE Dashboard API",
        "description": "API para gerenciamento de dados de emissões por instalação.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "components": {
        "schemas": {
            "Instalacao": {
                "type": "object",
                "properties": {
                    "Ano": {"type": "string", "example": "2023"},
                    "Bacia": {"type": "string", "example": "Santos"},
                    "Instalacao": {"type": "string", "example": "FPSO Alpha"},
                    "Operador": {"type": "string", "example": "Petrobras"},
                    "Campo": {"type": "string", "example": "Búzios"},
                    "Emissoes_Escopo1": {"type": "number", "example": 1234.56},
                    "Emissoes_Escopo2": {"type": "number", "example": 789.01},
                    "Emissoes_Total": {"type": "number", "example": 2023.57},
                    "Emissoes_CH4": {"type": "number", "example": 34.5},
                    "Emissoes_CO2": {"type": "number", "example": 1989.07},
                    "Producao_Anual_Liquida": {"type": "number", "example": 1500000.0},
                    "Intensidade_Emissoes": {"type": "number", "example": 1.35}
                },
                "required": [
                    "Ano", "Bacia", "Instalacao", "Operador", "Campo",
                    "Emissoes_Escopo1", "Emissoes_Escopo2", "Emissoes_Total",
                    "Emissoes_CH4", "Emissoes_CO2", "Producao_Anual_Liquida",
                    "Intensidade_Emissoes"
                ]
            }
        }
    }
}

swagger = Swagger(app, template=swagger_template)


app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
