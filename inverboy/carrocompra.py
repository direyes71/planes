# -*- coding: utf-8 -*-

class Carro:
    def __init__(self):
        self.articulos = {}
        self.metodos={1:'pagosonline',2:'celular',3:'taquilla'}
        self.perfil=None

    def get_perfi(self):
        return self.perfil
    def set_perfil(self,perfilx):
        self.perfil=perfilx

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

    @property
    def total(self):
        # la magia de la programacion funcional si esta usando este framewokr usted sabe programacion funcional
        # por ende es ovio esta linea

        if self.get_perfi()!=None:


            def aplicar_descuento_y_facturar(parametro):
                producto,cantidad=parametro
                descuento=Descuento.objects.obtener_descuento_facturado(producto,self.get_perfi(),cantidad)
                descuento_calculado=0

                if len(descuento)!=0:
                    descuento_calculado=descuento[0].porcentaje
                return (producto.valor_a_pagar-(producto.valor_a_pagar*(descuento_calculado/100)))*cantidad


            return sum (map( aplicar_descuento_y_facturar,self.articulos.items()))

        return sum (map( lambda(producto,cantidad):producto.valor_a_pagar*cantidad,self.articulos.items()))
  