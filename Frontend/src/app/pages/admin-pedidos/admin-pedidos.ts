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


  estados = [
    'pendiente',
    'confirmado',
    'preparando',
    'enviado',
    'entregado',
    'cancelado'
  ];


  constructor(
    private pedidosService: PedidosService
  ) {}


  ngOnInit(): void {
    this.cargarPedidos();
  }


  cargarPedidos(): void {

    this.pedidosService.obtenerPedidos().subscribe({

      next: (pedidos) => {
        this.pedidos.set(pedidos);
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


  guardarEstado(pedido: PedidoResponse): void {

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
      }

    });
  }

}