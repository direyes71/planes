# -*- coding: utf-8 -*-

class Carro:

    def __init__(self):
        self.articulos = []

    def set_articulo(self, articulo):
        if self.existe_articulo(articulo['id']):
            articulo_existente = self.get_articulo(articulo['id'])
            articulo_existente['cantidad'] = float(articulo['cantidad'])
            articulo_existente['observaciones'] = articulo['observaciones']
        else :
            return self.articulos.append(articulo)

    def del_articulo(self, articulo_id):
        if self.existe_articulo(articulo_id):
            articulo_existente = self.get_articulo(articulo_id)
            self.articulos.remove(articulo_existente)
        return 

    def existe_articulo(self, articulo_id):
        for articulo in self.articulos:
            if int(articulo_id) == articulo['id']:
                return True
        return False

    def items(self):
        return self.articulos

    def get_articulo(self, articulo_id):
        if self.existe_articulo(articulo_id):
            for articulo in self.articulos:
                if int(articulo_id) == articulo['id']:
                    return articulo
        return None

    def get_articulo_cantidad(self, articulo_id):
        articulo = self.get_articulo(articulo_id)
        if articulo != None:
            return float(articulo['cantidad'])
        return None

    """
    def __init__(self):
        self.articulos = {}

    @property
    def items(self):
        return self.articulos.items()

    @property
    def hay_articulos(self):
        return self.articulos.items()!=0

    @property
    def cantidad(self):
        #brujeria ;)
        return sum(self.articulos.values())

    def __str__(self):
        return str(self.articulos)

    def set_articulo(self,dict):
        return self.articulos.update(dict)

    def existe_articulo(self,articulo):
        return self.articulos.has_key(articulo)

    def get_producto_catidad(self,producto):
        return self.articulos[producto]
    """