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

    /* CAMPOS OBLIGATORIOS */

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


    /* VALIDAR NOMBRE */

    const nombreValido =
      /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/;

    if (
      !nombreValido.test(
        this.nombre.trim()
      )
    ) {

      this.error.set(
        'El nombre solo puede contener letras'
      );

      return;
    }


    /* VALIDAR TELÉFONO */

    if (
      !/^\d{8}$/.test(
        this.telefono
      )
    ) {

      this.error.set(
        'El teléfono debe contener exactamente 8 números'
      );

      return;
    }


    /* VALIDAR DIRECCIÓN */

    if (
      this.direccion.trim().length < 5
    ) {

      this.error.set(
        'Ingresa una dirección válida'
      );

      return;
    }


    /* VALIDAR CARRITO */

    if (
      this.carritoService.items().length === 0
    ) {

      this.error.set(
        'El carrito está vacío'
      );

      return;
    }


    /* CREAR PEDIDO */

    const pedido: PedidoCreate = {

      nombre_cliente:
        this.nombre.trim(),

      telefono:
        this.telefono,

      direccion_entrega:
        this.direccion.trim(),

      observaciones:
        this.observaciones.trim() || null,

      productos:
        this.carritoService.items().map(
          item => ({
            id_producto:
              item.producto.id_producto,

            cantidad:
              item.cantidad
          })
        )
    };


    this.enviando.set(true);
    this.error.set('');


    this.pedidosService
      .crearPedido(pedido)
      .subscribe({

        next: (respuesta) => {

          this.carritoService.vaciar();

          this.router.navigate([
            '/pedido-confirmado',
            respuesta.id_pedido
          ]);

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


  validarTelefono(
    event: Event
  ): void {

    const input =
      event.target as HTMLInputElement;


    /* ELIMINA TODO LO QUE NO SEA NÚMERO */

    const soloNumeros =
      input.value.replace(/\D/g, '');


    /* MÁXIMO 8 DÍGITOS */

    const limitado =
      soloNumeros.slice(0, 8);


    input.value = limitado;

    this.telefono = limitado;
  }

}