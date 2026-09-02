import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import {
  PedidoResponse,
  PedidosService
} from '../../services/pedidos.service';


@Component({
  selector: 'app-admin-pedidos',
  imports: [
    RouterLink,
    FormsModule
  ],
  templateUrl: './admin-pedidos.html',
  styleUrl: './admin-pedidos.css'
})
export class AdminPedidos implements OnInit {

  pedidos = signal<PedidoResponse[]>([]);

  cargando = signal(true);
  error = signal('');
  mensaje = signal('');

  estadosOriginales: Record<number, string> = {};


  constructor(
    private pedidosService: PedidosService
  ) {}


  ngOnInit(): void {
    this.cargarPedidos();
  }


  cargarPedidos(): void {

    this.cargando.set(true);

    this.pedidosService.obtenerPedidos().subscribe({

      next: (pedidos) => {

        this.pedidos.set(pedidos);

        this.estadosOriginales = {};

        pedidos.forEach(pedido => {

          this.estadosOriginales[
            pedido.id_pedido
          ] = pedido.estado;

        });

        this.cargando.set(false);
      },

      error: () => {

        this.error.set(
          'No se pudieron cargar los pedidos'
        );

        this.cargando.set(false);
      }

    });
  }


  obtenerEstadoOriginal(
    pedido: PedidoResponse
  ): string {

    return this.estadosOriginales[
      pedido.id_pedido
    ] || pedido.estado;
  }


  estadosDisponibles(
    pedido: PedidoResponse
  ): string[] {

    const estadoOriginal =
      this.obtenerEstadoOriginal(pedido);


    const transiciones: Record<
      string,
      string[]
    > = {

      pendiente: [
        'pendiente',
        'confirmado',
        'cancelado'
      ],

      confirmado: [
        'confirmado',
        'preparando',
        'cancelado'
      ],

      preparando: [
        'preparando',
        'enviado',
        'cancelado'
      ],

      enviado: [
        'enviado',
        'entregado'
      ],

      entregado: [
        'entregado'
      ],

      cancelado: [
        'cancelado'
      ]

    };


    return transiciones[
      estadoOriginal
    ] || [
      estadoOriginal
    ];
  }


  estadoFinal(
    pedido: PedidoResponse
  ): boolean {

    const estadoOriginal =
      this.obtenerEstadoOriginal(pedido);

    return (
      estadoOriginal === 'entregado' ||
      estadoOriginal === 'cancelado'
    );
  }


  puedeGuardar(
    pedido: PedidoResponse
  ): boolean {

    if (this.estadoFinal(pedido)) {
      return false;
    }

    return (
      pedido.estado !==
      this.obtenerEstadoOriginal(pedido)
    );
  }


  guardarEstado(
    pedido: PedidoResponse
  ): void {

    if (!this.puedeGuardar(pedido)) {
      return;
    }


    this.error.set('');
    this.mensaje.set('');


    this.pedidosService.actualizarEstado(
      pedido.id_pedido,
      pedido.estado
    ).subscribe({

      next: () => {

        this.mensaje.set(
          `Pedido #${pedido.id_pedido} actualizado correctamente`
        );

        this.cargarPedidos();
      },

      error: (error) => {

        this.error.set(
          error.error?.detail ||
          'No se pudo actualizar el estado'
        );

        this.cargarPedidos();
      }

    });
  }

}