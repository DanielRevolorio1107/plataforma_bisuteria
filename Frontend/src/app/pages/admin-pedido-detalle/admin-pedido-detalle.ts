import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import {
  PedidoDetalleResponse,
  PedidosService
} from '../../services/pedidos.service';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-pedido-detalle',
  imports: [RouterLink],
  templateUrl: './admin-pedido-detalle.html',
  styleUrl: './admin-pedido-detalle.css'
})
export class AdminPedidoDetalle implements OnInit {

  pedido = signal<PedidoDetalleResponse | null>(null);
  productos = signal<Producto[]>([]);

  cargando = signal(true);
  error = signal('');


  constructor(
    private route: ActivatedRoute,
    private pedidosService: PedidosService,
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {

    const idPedido = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.productosService.obtenerTodosAdmin().subscribe({
      next: (productos) => {
        this.productos.set(productos);
      }
    });


    this.pedidosService.obtenerPedido(idPedido).subscribe({

      next: (pedido) => {
        this.pedido.set(pedido);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set(
          'No se pudo cargar el pedido'
        );

        this.cargando.set(false);
      }

    });
  }


  obtenerNombreProducto(idProducto: number): string {

    const producto = this.productos().find(
      p => p.id_producto === idProducto
    );

    return producto
      ? producto.nombre
      : `Producto #${idProducto}`;
  }

}