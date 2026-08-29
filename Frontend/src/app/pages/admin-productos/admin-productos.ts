import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-productos',
  imports: [RouterLink],
  templateUrl: './admin-productos.html',
  styleUrl: './admin-productos.css'
})
export class AdminProductos implements OnInit {

  productos = signal<Producto[]>([]);

  cargando = signal(true);
  error = signal('');
  mensaje = signal('');


  constructor(
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {
    this.cargarProductos();
  }


  cargarProductos(): void {

    this.productosService
      .obtenerTodosAdmin()
      .subscribe({

        next: (productos) => {
          this.productos.set(productos);
          this.cargando.set(false);
        },

        error: () => {
          this.error.set(
            'No se pudieron cargar los productos'
          );

          this.cargando.set(false);
        }

      });
  }


  desactivar(producto: Producto): void {

    this.error.set('');
    this.mensaje.set('');


    this.productosService
      .desactivarProducto(producto.id_producto)
      .subscribe({

        next: () => {

          this.mensaje.set(
            'Producto desactivado correctamente'
          );

          this.cargarProductos();
        },

        error: (error) => {

          this.error.set(
            error.error?.detail ||
            'No se pudo desactivar el producto'
          );
        }

      });
  }


  activar(producto: Producto): void {

    this.error.set('');
    this.mensaje.set('');


    this.productosService
      .activarProducto(producto.id_producto)
      .subscribe({

        next: () => {

          this.mensaje.set(
            'Producto activado correctamente'
          );

          this.cargarProductos();
        },

        error: (error) => {

          this.error.set(
            error.error?.detail ||
            'No se pudo activar el producto'
          );
        }

      });
  }

}