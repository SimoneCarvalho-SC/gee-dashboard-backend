from marshmallow import Schema, fields


class InstalacaoSchema(Schema):
    Ano = fields.String(required=True)
    Bacia = fields.String(required=True)
    Instalacao = fields.String(required=True)
    Operador = fields.String(required=True)
    Campo = fields.String(required=True)
    Emissoes_Escopo1 = fields.Float(required=True)
    Emissoes_Escopo2 = fields.Float(required=True)
    Emissoes_Total = fields.Float(required=True)
    Emissoes_CH4 = fields.Float(required=True)
    Emissoes_CO2 = fields.Float(required=True)
    Producao_Anual_Liquida = fields.Float(required=True)
    Intensidade_Emissoes = fields.Float(required=True)
