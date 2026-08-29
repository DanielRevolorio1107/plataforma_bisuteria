import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import {
  Inventario,
  InventarioService
} from '../../services/inventario.service';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-inventario',
  imports: [
    RouterLink,
    FormsModule
  ],
  templateUrl: './admin-inventario.html',
  styleUrl: './admin-inventario.css'
})
export class AdminInventario implements OnInit {

  inventario = signal<Inventario[]>([]);
  productos = signal<Producto[]>([]);

  cargando = signal(true);
  error = signal('');
  mensaje = signal('');


  constructor(
    private inventarioService: InventarioService,
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {

    this.cargarProductos();
    this.cargarInventario();

  }


  cargarProductos(): void {

    this.productosService.obtenerTodosAdmin().subscribe({

      next: (productos) => {
        this.productos.set(productos);
      },

      error: () => {
        this.error.set(
          'No se pudieron cargar los productos'
        );
      }

    });
  }


  cargarInventario(): void {

    this.inventarioService.obtenerInventario().subscribe({

      next: (datos) => {
        this.inventario.set(datos);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set(
          'No se pudo cargar el inventario'
        );

        this.cargando.set(false);
      }

    });
  }


  obtenerNombreProducto(
    idProducto: number
  ): string {

    const producto = this.productos().find(
      item => item.id_producto === idProducto
    );

    return producto
      ? producto.nombre
      : `Producto #${idProducto}`;
  }


  guardar(item: Inventario): void {

    if (
      item.stock_actual < 0 ||
      item.stock_minimo < 0
    ) {

      this.error.set(
        'El stock no puede ser negativo'
      );

      return;
    }


    this.error.set('');
    this.mensaje.set('');


    this.inventarioService.actualizarInventario(
      item.id_producto,
      {
        stock_actual: item.stock_actual,
        stock_minimo: item.stock_minimo
      }
    ).subscribe({

      next: () => {

        this.mensaje.set(
          'Inventario actualizado correctamente'
        );

        this.cargarInventario();
      },

      error: (error) => {

        this.error.set(
          error.error?.detail ||
          'No se pudo actualizar el inventario'
        );
      }

    });
  }

}