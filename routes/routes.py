from flask import Blueprint, request, jsonify
from model import instalacao
from flasgger.utils import swag_from

main_bp = Blueprint('main', __name__)

# Rotas API


@main_bp.route('/cadastrar_instalacao', methods=['POST'])
@swag_from({
    'tags': ['Instalação'],
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
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
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Instalação cadastrada com sucesso'
        },
        400: {
            'description': 'Erro no cadastro'
        }
    }
})
def cadastrar_instalacao_route():
    data = request.get_json()
    resultado = instalacao.cadastrar_instalacao(data)

    if isinstance(resultado, dict) and "Erro ao cadastrar" in resultado.get("message", ""):
        return jsonify(resultado), 400

    return jsonify({"message": resultado})


@main_bp.route('/buscar_instalacao/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Instalação'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da instalação a ser buscada'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados da instalação encontrada',
            'schema': {
                '$ref': '#/components/schemas/Instalacao'
            }
        },
        404: {
            'description': 'Instalação não encontrada'
        }
    }
})
def buscar_instalacao_route(id):
    inst = instalacao.buscar_instalacao(id)
    if inst is None:
        return jsonify({'error': 'Instalação não encontrada'}), 404
    return jsonify(dict(inst))


@main_bp.route('/listar_instalacoes', methods=['GET'])
@swag_from({
    'tags': ['Instalação'],
    'responses': {
        200: {
            'description': 'Lista de todas as instalações cadastradas',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/components/schemas/Instalacao'
                }
            }
        },
        500: {
            'description': 'Erro interno no servidor'
        }
    }
})
def listar_instalacoes_route():
    try:
        insts = instalacao.listar_instalacoes()
        return jsonify([dict(i) for i in insts])
    except Exception as e:
        print(f"Erro em /listar_instalacoes: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500


@main_bp.route('/deletar_instalacao/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Instalação'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da instalação a ser deletada'
        }
    ],
    'responses': {
        200: {
            'description': 'Instalação deletada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Instalação deletada com sucesso'
                    }
                }
            }
        },
        404: {
            'description': 'Instalação não encontrada'
        }
    }
})
def deletar_instalacao_route(id):
    instalacao.deletar_instalacao(id)
    return jsonify({'message': 'Instalação deletada com sucesso'})
