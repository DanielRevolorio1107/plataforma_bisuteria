import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { CarritoService } from '../../services/carrito.service';
import {
  PedidoCreate,
  PedidosService
} from '../../services/pedidos.service';


@Component({
  selector: 'app-checkout',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './checkout.html',
  styleUrl: './checkout.css'
})
export class Checkout {

  nombre = '';
  telefono = '';
  direccion = '';
  observaciones = '';

  enviando = signal(false);
  error = signal('');

  constructor(
    public carritoService: CarritoService,
    private pedidosService: PedidosService,
    private router: Router
  ) {}


  realizarPedido(): void {

    if (
      !this.nombre.trim() ||
      !this.telefono.trim() ||
      !this.direccion.trim()
    ) {
      this.error.set(
        'Completa nombre, teléfono y dirección'
      );

      return;
    }

    if (this.carritoService.items().length === 0) {
      this.error.set(
        'El carrito está vacío'
      );

      return;
    }

    const pedido: PedidoCreate = {

      nombre_cliente: this.nombre,
      telefono: this.telefono,
      direccion_entrega: this.direccion,

      observaciones:
        this.observaciones.trim() || null,

      productos:
        this.carritoService.items().map(item => ({
          id_producto: item.producto.id_producto,
          cantidad: item.cantidad
        }))
    };

    this.enviando.set(true);
    this.error.set('');

    this.pedidosService.crearPedido(pedido).subscribe({

      next: (respuesta) => {

        this.carritoService.vaciar();

        this.router.navigate(
          ['/pedido-confirmado', respuesta.id_pedido]
        );
      },

      error: (error) => {

        this.enviando.set(false);

        this.error.set(
          error.error?.detail ||
          'No se pudo realizar el pedido'
        );
      }

    });
  }

}