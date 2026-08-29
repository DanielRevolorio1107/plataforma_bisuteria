import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  CarritoService
} from '../../services/carrito.service';

import {
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-carrito',
  imports: [RouterLink],
  templateUrl: './carrito.html',
  styleUrl: './carrito.css'
})
export class Carrito implements OnInit {

  stocks = signal<Record<number, number>>({});

  mensaje = signal('');


  constructor(
    public carritoService: CarritoService,
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {
    this.cargarDisponibilidades();
  }


  cargarDisponibilidades(): void {

    for (
      const item of this.carritoService.items()
    ) {

      const idProducto =
        item.producto.id_producto;


      this.productosService
        .obtenerDisponibilidad(idProducto)
        .subscribe({

          next: (respuesta) => {

            this.stocks.update(actual => ({
              ...actual,
              [idProducto]:
                respuesta.stock_disponible
            }));
          },

          error: () => {

            this.stocks.update(actual => ({
              ...actual,
              [idProducto]: 0
            }));
          }

        });
    }
  }


  obtenerStock(
    idProducto: number
  ): number {

    return this.stocks()[idProducto] ?? 0;
  }


  aumentar(
    idProducto: number
  ): void {

    const item =
      this.carritoService.items().find(
        item =>
          item.producto.id_producto ===
          idProducto
      );


    if (!item) {
      return;
    }


    const stock =
      this.obtenerStock(idProducto);


    if (item.cantidad >= stock) {

      this.mensaje.set(
        'No hay más unidades disponibles'
      );

      return;
    }


    this.carritoService.aumentar(
      idProducto
    );

    this.mensaje.set('');
  }


  disminuir(
    idProducto: number
  ): void {

    this.carritoService.disminuir(
      idProducto
    );

    this.mensaje.set('');
  }


  eliminar(
    idProducto: number
  ): void {

    this.carritoService.eliminar(
      idProducto
    );

    this.mensaje.set('');
  }


  vaciar(): void {

    this.carritoService.vaciar();

    this.mensaje.set('');
  }

}